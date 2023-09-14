from django.db import models
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

from core.models import Service, ServiceRule, Staff, Customer, CustomerServiceLog, OperationProc, RecommendedService, Message, ChengBaoRenYuanQingDan
from core.business_functions import field_name_replace, create_customer_schedule, manage_recommended_service
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

    if request.path == '/admin/login/':  # 后台登录
        return
    
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
    operand_finished.send(sender=user_logged_in_handler, pid=new_proc, request=request, form_data=None, formset_data=None)


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
    operand_finished.send(sender=user_registered_handler, pid=new_proc, request=request, form_data=None, formset_data=None)


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
    from core.business_functions import update_unassigned_procs, update_customer_services_list, update_staff_todo_list
    # 如果操作员是员工，更新职员任务工作台可申领的服务作业
    if instance.operator and instance.operator.user.is_staff:
        update_unassigned_procs(instance.operator)
        # 更新操作员的今日安排、紧要安排、本周安排
        update_staff_todo_list(instance.operator)

    # 根据customer过滤出用户的已安排服务和历史服务，发送channel_message给“用户服务组”
    if instance.service.service_type in [1,2]:
        update_customer_services_list(instance.customer)


@receiver(operand_started)
def operand_started_handler(sender, **kwargs):
    operation_proc = kwargs['operation_proc']  # 作业进程
    operation_proc.update_state(kwargs['ocode'])  # 更新作业进程操作码    
    operation_proc.operator = kwargs['operator']  # 设置当前用户为作业进程操作员
    operation_proc.save()


@receiver(operand_finished)
def operand_finished_handler(sender, **kwargs):
    from django.contrib import messages
    import copy
    import re
    from core.business_functions import create_service_proc, dispatch_operator, eval_scheduled_time, trans_form_to_dict

    def _preprocess_data(proc, event_rule, **kwargs):
        # 1. 整合当前服务进程表单数据的formset部分（如果有）
        form_data = kwargs['form_data']
        formset_data = kwargs.get('formset_data', None)
        if formset_data:
            data_list = [{**form_data, **item} for item in formset_data if item]
        else:
            data_list =[form_data]

        # 2. 准备环境上下文数据：客户历史服务记录
        history_data = {}
        if event_rule.detection_scope != 'CURRENT_SERVICE':
            '''
            获取一个时间段健康记录，按时间从早到晚的顺序合并成一个dict
            '''
            period = event_rule.detection_scope
            form_class_scope = event_rule.form_class_scope
            # 取客户健康档案记录构造检测数据dict
            logs = CustomerServiceLog.logs.get_customer_service_log(proc.customer, period, form_class_scope)
            for log in logs:
                history_data = {**history_data, **log.data}

        return data_list, history_data

    def _detect_business_events(event_rule, form_data, expression_fields_set):
        '''
        检查表达式是否满足 return: Boolean
		'''
        expression_fields_val_dict = {}  # 构造一个仅存储表达式内的字段及其值的字典
        for field_name in expression_fields_set:
            expression_fields_val_dict[field_name] = form_data.get(field_name, '')
        value_expression = field_name_replace(event_rule.expression, expression_fields_val_dict)
        try:
            if eval(value_expression):  # 待检查的字段值带入表达式，并执行返回结果
                print('表达式:', event_rule.expression, '事件：', event_rule, '字段值:', expression_fields_val_dict)
                return True
        except TypeError:
            return False
        return False

    def _schedule(service_rule, **kwargs):
        '''
        调度系统作业
        '''
        def _create_next_service(**kwargs):
            '''
            生成后续服务
            '''
            # 准备新的服务作业进程参数
            operation_proc = kwargs['operation_proc']
            service = kwargs['next_service']
            customer = operation_proc.customer
            current_operator = kwargs['operator']
            service_operator = dispatch_operator(customer, service, current_operator, timezone.now())

            # 区分服务类型是"1 管理调度服务"还是"2 诊疗服务"，获取ContentType
            if service.service_type == 1:
                content_type = ContentType.objects.get(app_label='service', model='customerschedulepackage')
            else:
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

            # 创建新的服务作业进程
            new_proc = create_service_proc(**proc_params)

            # 显示提示消息：开单成功
            messages.add_message(kwargs['request'], messages.INFO, f'{service.label}已开单')

            return f'创建服务作业进程: {new_proc}'
        
        def _recommend_next_service(**kwargs): 
            '''
            推荐后续服务
            '''
            # 准备新的服务作业进程参数
            operation_proc = kwargs['operation_proc']

            # 删除旧的相同推荐服务条目
            RecommendedService.objects.filter(service=kwargs['next_service'], customer=operation_proc.customer).delete()
            
            # 创建新的推荐服务条目
            obj = RecommendedService(
                service=kwargs['next_service'],  # 推荐的服务
                customer=operation_proc.customer,  # 客户
                creater=kwargs['operator'],  # 创建者
                pid=operation_proc,  # 当前进程是被推荐服务的父进程
                age=0,  # 年龄
                cpid=operation_proc.contract_service_proc,  # 所属合约服务进程
                passing_data=kwargs['passing_data']
            )
            obj.save()

            return f'推荐服务作业: {obj}'

        def _create_batch_services(**kwargs):
            def _get_schedule_times(form_data, api_fields):
                def _get_schedule_params(form_data, api_fields):
                    '''
                    返回计算时间计划的表达式：period_number, frequency
                    '''
                    # 从api_fields字典中获取系统API字段的对应表单字段名称
                    duration_field = api_fields.get('hssc_duration', None)
                    frequency_field = api_fields.get('hssc_frequency', None)

                    # 从kwargs['form_data']中的对应字段提取参数信息，生成计划时间列表
                    if duration_field and frequency_field:
                        duration = int(re.search(r'(\d+)', form_data.get(duration_field, '0')).group(1))
                        frequency = int(re.search(r'(\d+)', form_data.get(frequency_field, '0')).group(1))
                    else:
                        duration = 0
                        frequency = 0
                    
                    return duration, frequency
                
                def _get_basetime():
                    '''
                    返回最近整点时间
                    '''
                    # 获取当前时间
                    now = timezone.now()                    
                    # 获取当前小时数并加1
                    next_hour = now.hour + 1
                    # 如果当前小时数为23时，将小时数设置为0，并增加一天
                    if next_hour == 24:
                        next_hour = 0
                        now += timezone.timedelta(days=1)
                    # 使用replace()方法设置新的小时数，并重置分钟、秒和微秒为0
                    nearest_hour = now.replace(hour=next_hour, minute=0, second=0, microsecond=0)
                    return nearest_hour
                
                period_number, frequency = _get_schedule_params(form_data, api_fields)  # 获取计划时间计算参数

                # 获取基准时间
                base_time = _get_basetime()
                schedule_times = []
                for day_x in range(period_number):
                    for batch in range(frequency):
                        schedule_times.append(base_time + timedelta(hours=batch*4))
                    base_time = base_time + timedelta(days=1)
                return schedule_times

            # 准备新的服务作业进程参数
            proc = kwargs['operation_proc']
            service = kwargs['next_service']

            params = {}
            params['service'] = service  # 进程所属服务
            params['customer'] = proc.customer  # 客户
            params['creater'] = kwargs['operator']   # 创建者  
            params['operator'] = None  # 未分配服务作业人员
            params['priority_operator'] = kwargs['priority_operator'] # 优先操作者
            params['state'] = 0  # or 根据服务作业权限判断
            params['parent_proc'] = proc  # 当前进程是被创建进程的父进程
            params['contract_service_proc'] = proc.contract_service_proc  # 所属合约服务进程
            params['passing_data'] = kwargs['passing_data']  # 传递表单数据：(0, '否'), (1, '接收，不可编辑'), (2, '接收，可以编辑')
            params['form_data'] = kwargs['form_data']  # 表单数据
            # 区分服务类型是"1 管理调度服务"还是"2 诊疗服务"，获取ContentType
            if service.service_type == 1:
                params['content_type'] = ContentType.objects.get(app_label='service', model='customerschedulepackage')
            else:
                params['content_type'] = ContentType.objects.get(app_label='service', model=kwargs['next_service'].name.lower())  # 表单类型

            # 获取服务表单的API字段
            api_fields = proc.service.buessiness_forms.all()[0].api_fields
            # 解析表单内容，生成计划时间列表
            schedule_times = _get_schedule_times(kwargs['form_data'], api_fields)
            for schedule_time in schedule_times:
                # 估算计划执行时间
                params['scheduled_time'] = schedule_time            
                # 创建新的服务作业进程
                new_proc = create_service_proc(**params)

            # 显示提示消息：开单成功
            messages.add_message(kwargs['request'], messages.INFO, f'{service.label}已开单{len(schedule_times)}份')
            return f'创建{len(schedule_times)}个服务作业进程: {new_proc}'

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
            CREATE_BATCH_SERVICES = _create_batch_services # 生成批量服务
            SEND_WECHART_TEMPLATE_MESSAGE = _send_wechat_template_message  # 发送公众号消息
            SEND_WECOM_MESSAGE = _send_wecom_message  # 发送企业微信消息

        system_operand = service_rule.system_operand
        # 构造作业参数
        params = {
            'operation_proc': kwargs['pid'],
            'operator': kwargs['pid'].operator,
            'priority_operator': service_rule.priority_operator,
            'service': service_rule.service,
            'next_service': service_rule.next_service,
            'passing_data': service_rule.passing_data,
            'complete_feedback': service_rule.complete_feedback,
            'reminders': service_rule.reminders,
            'message': service_rule.message,
            'interval_rule': service_rule.interval_rule,
            'interval_time': service_rule.interval_time,
            'request': kwargs['request'],
            'form_data': kwargs['form_data'],
            'apply_to_group': service_rule.apply_to_group,
        }
        # 执行系统自动作业。传入：作业指令，作业参数；返回：String，描述执行结果
        # 执行前检查系统作业类型是否合法，只执行operand_type为"SCHEDULE_OPERAND"的系统作业
        if system_operand.operand_type == "SCHEDULE_OPERAND":
            # 调用OperandFuncMixin中的系统自动作业函数
            result = eval(f'SystemOperandFunc.{system_operand.func}')(**params)
            return result 
        return None

    operation_proc = kwargs['pid']
    # 把服务进程状态修改为已完成
    if operation_proc:
        operation_proc.update_state('RTC')


    # 0. 维护推荐服务队列
    manage_recommended_service(operation_proc.customer)

    # *************************************************
    # 1. 根据服务规则检查业务事件是否发生，执行系统作业
    # *************************************************
    # 逐一检查service_rule.event_rule.expression是否满足, 只检查规则的触发事件的event_type为SCHEDULE_EVENT的规则
    for service_rule in ServiceRule.objects.filter(service=operation_proc.service, is_active=True, event_rule__event_type = "SCHEDULE_EVENT"):
        event_rule = service_rule.event_rule
        if event_rule.expression == 'completed':  # 完成事件直接调度系统作业
            result = _schedule(service_rule, **kwargs)
        else:  # 判断是否发生其他业务事件
            # 1. 数据预处理：整合表单数据的formset，准备服务记录环境上下文
            scan_list, history_data = _preprocess_data(operation_proc, event_rule, **kwargs)

            # 2. 获取待检测表达式字段expression_fields集合, 格式预处理：去除空格，转为数组，再转为集合去重
            expression_fields_set = set(event_rule.expression_fields.strip().split(','))
            
            # 3. 按照规则构造检测数据集，并逐一检测是否满足规则
            form_name = operation_proc.content_object.__class__.__name__.lower()  # 表单名称
            for scan_item in scan_list:
                # 1) 转换数据格式，适配field_name_replace的格式要求
                item_copy = copy.copy(scan_item)
                scan_dict = trans_form_to_dict(item_copy, form_name)

                # 2) 整合历史上下文
                scan_data = {**history_data, **scan_dict}
                
                # 3) 根据检测表达式字段集合剪裁生成待检测数据字典
                clipped_scan_data = {}
                for field_name in expression_fields_set:
                    _value = scan_data.get(field_name, '')
                    clipped_scan_data[field_name] = _value if bool(_value) else '{}'

                # 4) 检测是否满足规则
                if _detect_business_events(event_rule, clipped_scan_data, expression_fields_set):
                    # 调度系统作业
                    kwargs['form_data'] = scan_item  # 传递表单数据
                    result = _schedule(service_rule, **kwargs)
                    # print('_detect_business_events --> ', service_rule.service, '满足规则：', event_rule, '调度结果:', result)
    

    # *************************************************
    # 2.执行质控管理逻辑，检查是否需要随访，如需要则按照指定间隔时间添加客户服务日程
    # *************************************************
    # (1) 检查已完成的服务进程的follow_up_required, follow_up_interval, follow_up_service 这三个字段是否为True
    # (2) 如果为True，构造参数，调用create_customer_schedule函数，创建客户服务日程
    current_service = operation_proc.service
    if current_service.follow_up_required and current_service.follow_up_interval and current_service.follow_up_service:
        # 构造参数
        params = {
            'customer': operation_proc.customer,
            'operator': operation_proc.operator,
            'creater': operation_proc.operator,
            'service': current_service.follow_up_service,
            'scheduled_time': timezone.now() + current_service.follow_up_interval,
            'pid': operation_proc,
        }
        # 调用create_customer_schedule函数，创建客户服务日程
        customer_schedule = create_customer_schedule(**params)
