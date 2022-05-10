from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


# 导入自定义作业完成信号
from core.signals import operand_started
@receiver(operand_started)
def operand_started_handler(sender, **kwargs):
    operation_proc = kwargs['operation_proc']  # 作业进程
    operation_proc.update_state(kwargs['ocode'])  # 更新作业进程操作码    
    operation_proc.operator = kwargs['operator']  # 设置当前用户为作业进程操作员
    operation_proc.save()


# 导入自定义作业完成信号
from core.signals import operand_finished
from core.models import Staff, Customer, OperationProc, Service, ServiceRule, StaffTodo
from service.models import get_form_instance
@receiver(operand_finished)
def operand_finished_handler(sender, **kwargs):
    # 从信号参数pid获取operation_proc
    operation_proc = OperationProc.objects.get(id=kwargs['pid'])

    # 1. 更新作业进程状态为RTC
    operation_proc.update_state(kwargs['ocode'])

    # 2. 非系统内置服务，则为客户表单作业，保存表单记录
    if not operation_proc.service.is_system_service:
        form_instance = get_form_instance(operation_proc)  # 获取表单实例
        operation_proc.customer.add_health_record(operation_proc, form_instance) # 存入客户健康记录

    # 3. 检查服务规则
    ServiceRule.objects.check_rules(operation_proc)


from service.models import create_form_instance
@receiver(post_save, sender=OperationProc)
def operation_proc_post_save_handler(sender, instance, created, **kwargs):
    # 创建服务进程里使用的表单实例, 将form_slugs保存到进程实例中
    if created and instance.state == 0:  # 系统保留作业(state=4)不创建model进程
        form = create_form_instance(instance)
        # 更新OperationProc服务进程的入口url
        instance.entry = f'/clinic/service/{instance.service.name.lower()}/{form.id}/change'
        instance.save()

    # 根据服务进程创建待办事项: sync_proc_todo_list
    if instance.operator and instance.customer:
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


from django.contrib.auth.signals import user_logged_in, user_logged_out
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
    operand_finished.send(sender=user_logged_in_handler, pid=new_proc.id, ocode='RTC', uid=user.id, form_data=None)


# 收到注册成功信号，生成用户注册事件：registration.signals.user_registered
from registration.signals import user_registered, user_activated, user_approved
@receiver(user_registered)
def user_registered_handler(sender, user, request, **kwargs):
    # 获得注册作业进程参数
    if user.is_staff:  # 职员注册
        service_name = 'staff_registered'
        customer = None
        operator = creater = user.customer
        print('职员注册', user, service_name)
    else:
        service_name = 'Z6201'   # 客户注册
        customer = operator = creater = user.customer
        print('客户注册', user, service_name)

    # 创建一个状态为“已完成”的职员/客户注册作业进程
    new_proc=OperationProc.objects.create(
        service=Service.objects.get(name=service_name),  # 服务
        customer=customer,  # 客户
        operator=operator,  # 作业人员
        creater=creater,  # 创建者
        state=4,  # 进程状态：注册完成
    )

    # 发送注册作业完成信号
    operand_finished.send(sender=user_registered_handler, pid=new_proc.id, ocode='RTC', uid=user.id, form_data=None)
    print('operand_finished sended')


from django.contrib.auth.models import User
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
