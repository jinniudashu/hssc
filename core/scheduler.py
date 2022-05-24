from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.models import User
from enum import Enum
import datetime
from django.forms import model_to_dict
from registration.signals import user_registered, user_activated, user_approved

from core.models import Service, ServiceRule, Staff, Customer, CustomerServiceLog, OperationProc, StaffTodo, RecommendedService, Message
from core.business_functions import field_name_replace, update_staff_todo_list, update_customer_recommended_service_list
from core.signals import operand_started, operand_finished  # 自定义作业完成信号


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
    operand_finished.send(sender=user_logged_in_handler, pid=new_proc, request=request)


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
    operand_finished.send(sender=user_registered_handler, pid=new_proc, request=request)


@receiver(post_save, sender=User)
def user_post_save_handler(sender, instance, created, **kwargs):
    if created:  # 创建用户
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
            name = instance.last_name+instance.first_name if instance.last_name+instance.first_name else instance.username
            Customer.objects.create(
                user=instance,
                name=name,
            )
    # else:   # 更新用户
    #     if instance.is_staff:
    #         print('更新员工信息', instance)
    #         customer = instance.customer
    #         customer.name = instance.last_name+instance.first_name
    #         customer.save()
    #         customer.staff.email = instance.email
    #         customer.staff.save()
    #     else:   # 客户
    #         print('更新客户信息', instance)
    #         customer = instance.customer
    #         customer.name = instance.last_name+instance.first_name
    #         customer.save()


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

    # 如果state=0, operator=None，通知StaffTodoConsumer更新可申领的服务作业

    
    # 根据customer过滤出用户的已安排服务，发送channel_message给“用户服务组”
    # 根据customer过滤出用户的历史服务，发送channel_message给“用户服务组”


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
                    start_time = datetime.datetime.now() + datetime.timedelta(days=-7)
                    end_time = datetime.datetime.now()
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
            from core.business_functions import create_service_proc, dispatch_operator
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
            proc_params['state'] = 0  # or 根据服务作业权限判断
            proc_params['scheduled_time'] = datetime.datetime.now()  # 创建时间 or 根据服务作业逻辑判断
            proc_params['parent_proc'] = operation_proc  # 当前进程是被创建进程的父进程
            proc_params['contract_service_proc'] = operation_proc.contract_service_proc  # 所属合约服务进程
            proc_params['content_type'] = content_type

            # 创建新的服务作业进程
            new_proc = create_service_proc(**proc_params)

            # 显示提示消息：开单成功
            from django.contrib import messages
            messages.add_message(kwargs['request'], messages.INFO, f'{service.label}已开单')

            return f'创建服务作业进程: {new_proc}'

        def _recommend_next_service(**kwargs):
            '''
            推荐后续服务
            '''
            # 准备新的服务作业进程参数
            operation_proc = kwargs['operation_proc']
            # 创建新的服务作业进程
            _recommended = RecommendedService.objects.create(
                service=kwargs['next_service'],  # 推荐的服务
                customer=operation_proc.customer,  # 客户
                creater=kwargs['operator'],  # 创建者
                pid=operation_proc,  # 当前进程是被推荐服务的父进程
                cpid=operation_proc.contract_service_proc,  # 所属合约服务进程
            )
            return f'推荐服务作业: {_recommended}'

        def _alert_content_violations(self, **kwargs):
            '''
            内容违规提示
            '''
            print('alert_content_violations:', '内容违规提示')
            return '内容违规提示'

        def _send_notification(**kwargs):
            '''
            发送提醒
            '''
            def _get_reminders(_option):
                '''
                用选项值为list.index获取提醒对象列表
                '''
                reminder_option = [
                    operation_proc.customer,  # 0: 发送给当前客户
                    kwargs['operator'],  # 1: 发送给当前作业人员
                    # return workgroup_list,  # 2: 发送给当前作业组成员
                ]
                return [reminder_option[_option]]

            # 准备服务作业进程参数
            operation_proc = kwargs['operation_proc']

            # 获取提醒人员list
            _reminders_option = kwargs['reminders']
            reminders = _get_reminders(_reminders_option)

            # 创建提醒消息
            for customer in reminders:
                _ = Message.objects.create(
                    message=kwargs['message'],  # 消息内容
                    customer=customer,  # 客户
                    creater=kwargs['operator'],  # 创建者
                    pid=operation_proc,  # 当前进程是被推荐服务的父进程
                    cpid=operation_proc.contract_service_proc,  # 所属合约服务进程
                )

            return f'生成提醒消息OK'

        class SystemOperandFunc(Enum):
            CREATE_NEXT_SERVICE = _create_next_service  # 生成后续服务
            RECOMMEND_NEXT_SERVICE = _recommend_next_service  # 推荐后续服务
            VIOLATION_ALERT = _alert_content_violations  # 内容违规提示
            SEND_NOTIFICATION = _send_notification  # 发送提醒

		# 调用OperandFuncMixin中的系统自动作业函数
        return eval(f'SystemOperandFunc.{system_operand}')(**kwargs)

    operation_proc = kwargs['pid']
    request = kwargs['request']

    # 更新作业进程状态为RTC
    operation_proc.update_state('RTC')

    # 根据服务规则检查业务事件是否发生，执行系统作业
    # 逐一检查service_rule.event_rule.expression是否满足
    for service_rule in ServiceRule.objects.filter(service=operation_proc.service, is_active=True):
        # 如果event_rule.expression为真，则构造事件参数，生成业务事件
        print('*****************************')
        print('From check_rules 扫描规则：', service_rule.service, service_rule.event_rule)
        if _is_rule_satified(service_rule.event_rule, operation_proc):
            print('From check_rules 满足规则：', service_rule.service, service_rule.event_rule)
            # 构造作业参数
            operation_params = {
                'operation_proc': operation_proc,
                'operator': operation_proc.operator,
                'service': service_rule.service,
                'next_service': service_rule.next_service,
                'passing_data': service_rule.passing_data,
                'complete_feedback': service_rule.complete_feedback,
                'reminders': service_rule.reminders,
                'message': service_rule.message,
                'interval_rule': service_rule.interval_rule,
                'interval_time': service_rule.interval_time,
                'request': request,
            }
            # 执行系统自动作业。传入：作业指令，作业参数；返回：String，描述执行结果
            _result = _execute_system_operand(service_rule.system_operand, **operation_params)
            print('From check_rules 执行结果:', _result)
    