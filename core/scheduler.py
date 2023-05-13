from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, datetime
from django.forms import model_to_dict
from enum import Enum
from registration.signals import user_registered, user_activated, user_approved

from core.models import Service, ServiceRule, Staff, Customer, CustomerServiceLog, OperationProc, StaffTodo, RecommendedService, Message, ChengBaoRenYuanQingDan
from core.business_functions import field_name_replace, create_customer_schedule
from core.signals import operand_started, operand_finished  # 自定义作业完成信号


# 数据导入ChengBaoRenYuanQingDan时，自动插入service.models.Ju_min_ji_ben_xin_xi_diao_cha
@receiver(post_save, sender=ChengBaoRenYuanQingDan)
def chengbao_renyuan_qingdan_post_save_handler(sender, instance, created, **kwargs):
    from service.models import Ju_min_ji_ben_xin_xi_diao_cha
    if created:
        # 字段对应关系
        cheng_bao_ren_yuan_qing_dan_map = {
            '序号': 'boolfield_xu_hao',
            '保单号': 'boolfield_bao_dan_hao',
            '被保人姓名': 'boolfield_bei_bao_ren_xing_ming',
            '证件类型': 'boolfield_zheng_jian_lei_xing',
            '身份证号': 'boolfield_zheng_jian_hao_ma',
            '出生日期': 'boolfield_chu_sheng_ri_qi',
            '保险责任': 'boolfield_bao_xian_ze_ren',
            '保险有效期': 'boolfield_bao_xian_you_xiao_qi',
            '联系方式': 'boolfield_lian_xi_dian_hua',
        }

        # 创建User实例
        user = User.objects.create_user(instance.被保人姓名, None, instance.联系方式)

        # # 创建客户档案
        # customer = Customer.objects.create(
        #     user=user,
        #     name=instance.被保人姓名,
        #     phone=instance.联系方式,
        # )
        customer = user.customer

        # 创建参保人员
        ju_min_ji_ben_xin_xi_diao_cha = Ju_min_ji_ben_xin_xi_diao_cha.objects.create(
            customer=customer,
            boolfield_xu_hao=instance.序号,
            boolfield_bao_dan_hao=instance.保单号,
            boolfield_bei_bao_ren_xing_ming=instance.被保人姓名,
            # boolfield_zheng_jian_lei_xing=instance.证件类型,
            boolfield_zheng_jian_hao_ma=instance.身份证号,
            boolfield_chu_sheng_ri_qi=datetime.strptime(instance.出生日期, "%Y-%m-%d"),
            boolfield_bao_xian_ze_ren=instance.保险责任,
            boolfield_bao_xian_you_xiao_qi=datetime.strptime(instance.保险有效期, "%Y-%m-%d"),
            boolfield_lian_xi_dian_hua=instance.联系方式,
        )


@receiver(user_logged_in)
def user_logged_in_handler(sender, user, request, **kwargs):
    '''
    系统内置业务事件的信号处理：用户注册，用户登录，员工登录
    收到登录信号，生成用户/职员登录事件
    '''
    # 用户登录Session登记
    from analytics.models import record_login
    record_login(request, user)

    # 获得登陆作业进程参数
    if user.is_staff:  # 职员登录
        event_name = 'doctor_login'
        customer = None
        operator = creater = user.customer
        print('职员登录', user, event_name)
    else:
        event_name = 'user_login'   # 客户登录
        customer = operator = creater = user.customer
        print('客户登录', user, event_name)

    # 创建一个状态为“已完成”的职员/客户登录作业进程
    new_proc=OperationProc.objects.create(
        service=Service.objects.get(name=event_name),  # 服务
        customer=customer,  # 客户
        operator=operator,  # 作业人员
        creater=creater,  # 创建者
        state=4,  # 进程状态：登录完成
    )

    # 发送登录作业完成信号
    operand_finished.send(sender=user_logged_in_handler, pid=new_proc, request=request, form_data=None)


# 收到注册成功信号，生成用户注册事件：registration.signals.user_registered
@receiver(user_registered)
def user_registered_handler(sender, user, request, **kwargs):
    # 获得注册作业进程参数
    if user.is_staff:  # 职员注册
        event_name = 'staff_registered'
        customer = None
        operator = creater = user.customer
        print('职员注册', user, event_name)
    else:
        event_name = 'Z6201'   # 客户注册
        customer = operator = creater = user.customer
        print('客户注册', user, event_name)

    # 创建一个状态为“已完成”的职员/客户注册作业进程
    new_proc=OperationProc.objects.create(
        service=Service.objects.get(name=event_name),  # 服务
        customer=customer,  # 客户
        operator=operator,  # 作业人员
        creater=creater,  # 创建者
        state=4,  # 进程状态：注册完成
    )

    # 发送注册作业完成信号
    operand_finished.send(sender=user_registered_handler, pid=new_proc, request=request, form_data=None)


@receiver(post_save, sender=User)
def user_post_save_handler(sender, instance, created, **kwargs):
    if created:  # 创建用户
        # 执行init_core_data.py脚本增加员工测试数据会触发以下逻辑
        if instance.is_staff:  # 新建职员
            print('创建员工信息', instance)
            customer = Customer.objects.create(
                user=instance,
                name=instance.last_name+instance.first_name,
            )
            Staff.objects.create(
                customer=customer,
                email=instance.email,
            )
        else:  # 新建客户
            print('创建客户信息', instance)
            Customer.objects.create(
                user=instance,
                name=instance.last_name+instance.first_name if instance.last_name+instance.first_name else instance.username,
            )
    else:   # 更新用户
        # 管理员在admin中新增员工时，要先增加用户，会触发以下逻辑，但此时还没有职员信息，所以要判断
        if instance.is_staff:
            print('更新员工信息', instance)
            customer = instance.customer
            customer.name = instance.last_name+instance.first_name
            customer.save()
            if hasattr(customer, 'staff'):
                customer.staff.email = instance.email
                customer.staff.save()
            else:
                Staff.objects.create(
                    customer=customer,
                    email=instance.email,
                )
        else:   # 客户
            print('更新客户信息', instance)
            customer = instance.customer
            customer.name = instance.last_name+instance.first_name if instance.last_name+instance.first_name else instance.username
            customer.save()


@receiver(post_delete, sender=User)
def user_post_delete_handler(sender, instance, **kwargs):
    '''
    删除用户后同步删除Customer和Staff相关信息
    '''
    if instance.is_staff:
        print('删除员工信息', instance)
        try:
            customer = instance.customer
            customer.staff.delete()
            instance.customer.delete()
        except:
            pass
    else:
        try:
            print('删除客户信息', instance)
            instance.customer.delete()
        except:
            pass


@receiver(post_save, sender=OperationProc)
def operation_proc_post_save_handler(sender, instance, created, **kwargs):
    from core.business_functions import update_unassigned_procs, update_customer_services_list
    # 如果操作员是员工更新职员任务工作台可申领的服务作业
    if instance.operator and instance.operator.user.is_staff:
        update_unassigned_procs(instance.operator)

    # 根据customer过滤出用户的已安排服务和历史服务，发送channel_message给“用户服务组”
    if instance.service.service_type in [1,2]:
        update_customer_services_list(instance.customer)

    # 根据服务进程创建待办事项: sync_proc_todo_list
    if instance.operator and instance.customer and instance.state < 4:
        try :
            todo = instance.stafftodo
            todo.scheduled_time = instance.scheduled_time
            todo.state = instance.state
            todo.priority = instance.priority
            todo.save()
        except StaffTodo.DoesNotExist:
            todo = StaffTodo.objects.create(
                operation_proc=instance,
                operator=instance.operator,
                scheduled_time=instance.scheduled_time,
                state=instance.state,
                customer_number=instance.customer.name,
                customer_name=instance.customer.name,
                service_label=instance.service.label,
                customer_phone=instance.customer.phone,
                customer_address=instance.customer.address,
                priority = instance.priority
            )


@receiver(operand_started)
def operand_started_handler(sender, **kwargs):
    operation_proc = kwargs['operation_proc']  # 作业进程
    operation_proc.update_state(kwargs['ocode'])  # 更新作业进程操作码    
    operation_proc.operator = kwargs['operator']  # 设置当前用户为作业进程操作员
    operation_proc.save()


@receiver(operand_finished)
def operand_finished_handler(sender, **kwargs):
    def _is_rule_satified(event_rule, operation_proc):
        '''
        检查表达式是否满足 return: Boolean
        parameters: form_data, self.expression
		'''
        def _get_scanned_data(event_rule, operation_proc, expression_fields_set):
            print('检测表单范围：', event_rule.detection_scope)
            # 1. 根据detection_scope生成待检测数据集合
            if event_rule.detection_scope == 'CURRENT_SERVICE':
                _scanned_data = operation_proc.customerservicelog.data
            else:
                '''
                获取一个时间段健康记录，按时间从早到晚的顺序合并成一个dict
                '''
                period = None  # 意味着self.detection_scope == 'ALL'表示获取全部健康记录
                if event_rule.detection_scope == 'LAST_WEEK_SERVICES':  # 获取表示指定时间段内的健康记录
                    start_time = timezone.now() + timedelta(days=-7)
                    end_time = timezone.now()
                    period = (start_time, end_time)

                # 取客户健康档案记录构造检测数据dict
                _scanned_data = {}
                logs = CustomerServiceLog.logs.get_customer_service_log(operation_proc.customer, period)            
                for log in logs:
                    _scanned_data = {**_scanned_data, **log.data}
                    
            print('From scheduler._get_scanned_data: 1. _scanned_data:', event_rule.detection_scope, _scanned_data)

            # 2. 根据表达式字段集合剪裁生成待检测数据字典
            scanned_data = {}
            for field_name in expression_fields_set:
                _value = _scanned_data.get(field_name, '')
                scanned_data[field_name] = _value if bool(_value) else '{}'
            print('From scheduler._get_scanned_data: 2. scanned_data:', scanned_data)

            return scanned_data

        if event_rule.expression == 'completed':  # 完成事件直接返回
            return True
        else:  # 判断是否发生其他业务事件
            # 数据预处理
            expression_fields_set = set(event_rule.expression_fields.strip().split(','))  # self.expression_fields: 去除空格，转为数组，再转为集合去重
            scanned_data_dict = _get_scanned_data(event_rule, operation_proc, expression_fields_set)  # 获取待扫描字段数据的字符格式字典，适配field_name_replace()的格式要求
            print('扫描内容:', scanned_data_dict)

            expression_fields_val_dict = {}  # 构造一个仅存储表达式内的字段及值的字典
            for field_name in expression_fields_set:
                expression_fields_val_dict[field_name] = scanned_data_dict.get(field_name, '')            

            print('检查表达式及值:', event_rule.expression, expression_fields_val_dict)
            _expression = field_name_replace(event_rule.expression, expression_fields_val_dict)
            print('eval表达式:', _expression)
            try:
                result = eval(_expression)  # 待检查的字段值带入表达式，并执行返回结果
                return result
            except TypeError:
                result = False

    def _execute_system_operand(system_operand, **kwargs):
        '''
        执行系统自动作业
        '''
        def _create_next_service(**kwargs):
            '''
            生成后续服务
            '''
            from core.business_functions import create_service_proc, dispatch_operator, eval_scheduled_time
            # 准备新的服务作业进程参数
            operation_proc = kwargs['operation_proc']
            service = kwargs['next_service']
            customer = operation_proc.customer
            current_operator = kwargs['operator']
            service_operator = dispatch_operator(customer, service, current_operator)
            content_type = ContentType.objects.get(app_label='service', model=kwargs['next_service'].name.lower())  # 表单类型

            proc_params = {}
            proc_params['service'] = service  # 进程所属服务
            proc_params['customer'] = customer  # 客户
            proc_params['creater'] = current_operator   # 创建者  
            proc_params['operator'] = service_operator  # 操作者 or 根据 责任人 和 服务作业权限判断
            proc_params['priority_operator'] = kwargs['priority_operator'] # 优先操作者
            proc_params['state'] = 0  # or 根据服务作业权限判断

            # 估算计划执行时间
            proc_params['scheduled_time'] = eval_scheduled_time(service, service_operator)
            
            proc_params['parent_proc'] = operation_proc  # 当前进程是被创建进程的父进程
            proc_params['contract_service_proc'] = operation_proc.contract_service_proc  # 所属合约服务进程
            proc_params['content_type'] = content_type
            proc_params['passing_data'] = kwargs['passing_data']  # 传递表单数据：(0, '否'), (1, '接收，不可编辑'), (2, '接收，可以编辑')
            proc_params['form_data'] = kwargs['form_data']  # 表单数据

            print('Debug: _create_next_service(proc_params):', proc_params)

            # 创建新的服务作业进程
            new_proc = create_service_proc(**proc_params)

            # 显示提示消息：开单成功
            from django.contrib import messages
            messages.add_message(kwargs['request'], messages.INFO, f'{service.label}已开单')

            return f'创建服务作业进程: {new_proc}'
        
        def _recommend_next_service(**kwargs):  # 由GPT-4重构的推荐服务函数
            '''
            推荐后续服务
            '''
            # 准备新的服务作业进程参数
            operation_proc = kwargs['operation_proc']
            
            # 创建新的推荐服务条目
            obj = RecommendedService(
                service=kwargs['next_service'],  # 推荐的服务
                customer=operation_proc.customer,  # 客户
                creater=kwargs['operator'],  # 创建者
                pid=operation_proc,  # 当前进程是被推荐服务的父进程
                cpid=operation_proc.contract_service_proc,  # 所属合约服务进程
                passing_data=kwargs['passing_data']
            )
            obj.save()

            return f'推荐服务作业: {obj}'

        def _send_wechat_template_message(**kwargs):
            '''
            发送公众号模板消息
            模板参数格式: {"template_id":"xxxxx", "title":"xxxxxx", "remark":"xxxxxx", "keyword1":"字段名1",  "keyword2":"字段名2", ...}
            '''
            from core.utils import get_wechat_template_message_data, send_wechat_template_message
            # 获取用户微信open_id
            open_id = kwargs['operation_proc'].customer.weixin_openid

            message = eval(kwargs['message'])  # 把kwargs['message']从字符串转换为字典
            form_data = kwargs['form_data']  # 表单数据

            # 用open_id 和 message 构造消息data
            data = get_wechat_template_message_data(open_id, message, form_data)

            # 发送消息
            result = send_wechat_template_message(data)

            print('发送公众号模板消息:', kwargs['message'], '结果:', result)
            return result

        def _send_wecom_message(**kwargs):
            '''
            发送企业微信提醒
            '''
            from core.utils import send_wecom_message
            
            # 获取作业员企业微信id
            wecom_uid = kwargs['operator'].staff.wecom_id

            # 获取消息内容
            message = kwargs['message']

            # 发送消息
            result = send_wecom_message(wecom_uid, message)
            print('发送企业微信提醒:', kwargs['message'])

            return result


        class SystemOperandFunc(Enum):
            CREATE_NEXT_SERVICE = _create_next_service  # 生成后续服务
            RECOMMEND_NEXT_SERVICE = _recommend_next_service  # 推荐后续服务
            SEND_WECHART_TEMPLATE_MESSAGE = _send_wechat_template_message  # 发送公众号消息
            SEND_WECOM_MESSAGE = _send_wecom_message  # 发送企业微信消息

		# 调用OperandFuncMixin中的系统自动作业函数
        return eval(f'SystemOperandFunc.{system_operand}')(**kwargs)

    operation_proc = kwargs['pid']
    request = kwargs['request']

    # 删除当前客户的所有推荐服务条目
    RecommendedService.objects.filter(customer=operation_proc.customer).delete()

    # 根据服务规则检查业务事件是否发生，执行系统作业    
    # 逐一检查service_rule.event_rule.expression是否满足, 只检查规则的触发事件的event_type为SCHEDULE_EVENT的规则
    for service_rule in ServiceRule.objects.filter(service=operation_proc.service, is_active=True, service_rule__event_rule__event_type = "SCHEDULE_EVENT"):
        # 如果event_rule.expression为真，则构造事件参数，生成业务事件
        print('*****************************')
        print('From check_rules 扫描规则：', service_rule.service, service_rule.event_rule)
        if _is_rule_satified(service_rule.event_rule, operation_proc):
            print('From check_rules 满足规则：', service_rule.service, service_rule.event_rule)
            # 构造作业参数
            print('operation_proc.operator:', operation_proc.operator)
            operation_params = {
                'operation_proc': operation_proc,
                'operator': operation_proc.operator,
                'priority_operator': service_rule.priority_operator,
                'service': service_rule.service,
                'next_service': service_rule.next_service,
                'passing_data': service_rule.passing_data,
                'complete_feedback': service_rule.complete_feedback,
                'reminders': service_rule.reminders,
                'message': service_rule.message,
                'interval_rule': service_rule.interval_rule,
                'interval_time': service_rule.interval_time,
                'request': request,
                'form_data': kwargs['form_data'],
            }
            # 执行系统自动作业。传入：作业指令，作业参数；返回：String，描述执行结果
            # 执行前检查系统作业类型是否合法，只执行operand_type为"SCHEDULE_OPERAND"的系统作业
            if service_rule.system_operand.operand_type == "SCHEDULE_OPERAND":
                _result = _execute_system_operand(service_rule.system_operand.func, **operation_params)
                print('From check_rules 执行结果:', _result)
    

    # 执行质控管理逻辑，检查是否需要随访，如需要则按照指定间隔时间添加客户服务日程
    # 1. 检查已完成的服务进程的follow_up_required, follow_up_interval, follow_up_service 这三个字段是否为True
    # 2. 如果为True，构造参数，调用create_customer_schedule函数，创建客户服务日程。传入参数：客户，服务，计划执行时间，服务进程
    current_service = operation_proc.service
    if current_service.follow_up_required and current_service.follow_up_interval and current_service.follow_up_service:
        # 构造参数
        params = {
            'customer': operation_proc.customer,
            'service': current_service.follow_up_service,
            'scheduled_time': timezone.now() + current_service.follow_up_interval,
            'pid': operation_proc,
        }
        # 调用create_customer_schedule函数，创建客户服务日程
        customer_schedule = create_customer_schedule(**params)
        print('质控管理--创建客户服务日程:', customer_schedule)