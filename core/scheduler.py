from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed, post_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out
from itertools import product
import traceback

# 导入自定义表单models
from django.contrib.contenttypes.models import ContentType
from registration.signals import user_registered, user_activated, user_approved

# 导入UserSession
from analytics.models import UserSession
from analytics.utils import get_client_ip

# 导入作业事件表、指令表
from core.models import Staff, Customer, Event, Event_instructions, Instruction, OperationProc, Operation
from core.models import SYSTEM_EVENTS
# 导入自定义作业完成信号
from core.signals import operand_finished, operand_started
from core.utils import keyword_replace

# 作业调度器
def operation_scheduler(event, params):
    # 查找指令集，发送任务指令
    event_instructions = Event_instructions.objects.filter(event=event)
    print('查找指令集，发送任务指令:', event, event_instructions)

    # 指令参数
    task_params={'uid': params['uid'], 'cid': params['cid'], 'ppid': params['ppid']}

    for event_instruction in event_instructions:
        task_params['oname'] = event_instruction.params  # 从事件指令参数中获取作业名称

        # 根据每条事件指令和预定义的作业分配策略，确定作业任务的操作员
        operation = Operation.objects.get(name=task_params['oname'])
        task_params['group'] = operation.group.all()

        task_func = event_instruction.instruction.func  # 从事件指令中获取操作函数名

        # 调用函数执行指令
        # 执行task.create_operation_proc
        print('send:', event_instruction.instruction.name, task_func, task_params)
        globals()[task_func](task_params)

        # 调用Celery @task执行指令
        # globals()[task_func].delay(task_params)
        # eval(task_func).delay(oid, '', '')
    return


@receiver(operand_started)
def operand_started_handler(sender, **kwargs):
    operation_proc = kwargs['operation_proc']  # 作业进程
    operation_proc.update_state(kwargs['ocode'])  # 更新作业进程操作码
    
    operator = kwargs['operator']  # 操作员
    operation_proc.operator = Staff.objects.get(customer=operator)  # 设置作业进程的操作员为当前用户
    operation_proc.save()


# ***********************************************************************
# 判断表单字段值包含数组的表达式是否成立。遍历数组字段，构造assignments字典
# ***********************************************************************
def is_event_happened_on_list_fields(list_fields, assignments, expression):
    # 转换list_fields中的字典为数组：{'a': [1, 2, 3]} -> [{'a': 1}, {'a': 2}, {'a': 3}]
    fields = []
    for field in list_fields:
        (key, value), = field.items()
        key_list_pairs = []
        for key_list_pair in value:
            key_list_pairs.append({key: key_list_pair})
        
        fields.append(key_list_pairs)

    # 将fields中元素的每种排列组合逐一添加到assignments中
    for item in list(product(*fields)):
        for key_list_pair in item:
            (key, value), = key_list_pair.items()
            assignments[key] = value

        if eval(keyword_replace(expression, assignments)):  # 把表达式中的变量替换为字典中对应的字段值，判断表达式是否成立
            print(f'True assignments: {assignments}')
            return True  # 任一参数组合成立，则返回True
    
    return False


# *******************************************************************************************
# 业务事件发生器：接收来自作业视图的自定义信号，更新作业进程状态，触发相关业务事件，调度后续作业
# *******************************************************************************************
@receiver(operand_finished)
def operand_finished_handler(sender, **kwargs):
    pid = kwargs['pid']  # 作业进程id

    _field_values = kwargs['field_values']  # POST表单数据
    field_values = _field_values.copy()  # 表单字段拷贝，避免修改原始数据
    field_values.pop('csrfmiddlewaretoken')  # 删除csrf字段

    proc = OperationProc.objects.get(id=pid)  # 获取当前作业进程实例
    proc.update_state(kwargs['ocode'])  # 更新作业进程状态

    print('收到作业完成消息，更新作业进程状态：', pid, kwargs['ocode'], field_values)

    # 2. 检查规则表，判断当前作业有规定业务事件需要检查, 如有取出规则集，逐一检查表达式是否为真，触发业务事件, 决定后续作业
    try:
        events = Event.objects.filter(operation = proc.operation)
        if events:
            event_params={'uid': proc.operator.id, 'cid': proc.customer.id, 'ppid': proc.ppid}  # 构造事件参数
            for event in events:
                if event.name.endswith('_completed'):  # 如果是作业完成事件“completed”，直接调度
                    operation_scheduler(event, event_params)
                else:  # 检查是否发生作业事件
                    # 构造表达式变量和对应值的初始字典
                    assignments = {}  # 表达式变量和对应值的字典
                    field_names = event.parameters.split(', ')  # 获取需要被检查的表单字段名, 转换为数组
                    list_fields = []  # 存储需要被检查的列表类型的表单字段
                    for field_name in field_names:
                        _value = field_values[field_name]  # 获取相应变量的表单字段值（form.field的值）
                        assignments[field_name] = f'{_value}'.replace(' ', '')  # 去除字符串值的空格
                        # 如果有数组，入栈
                        if len(field_values.getlist(field_name))>1:
                            list_fields.append({field_name: field_values.getlist(field_name)})  # # 存储列表类型的表单字段

                    if len(list_fields)>0:  # 如果栈中有数组，用栈中的数组的每个值排列组合，逐一更新字典相应字段值
                        if is_event_happened_on_list_fields(list_fields, assignments, event.expression):
                            print('数组参数表达式为真，触发事件：', event)
                            operation_scheduler(event, event_params)
                    else:  # 栈为空，表示没有数组类型的字段，直接用assignments检查表达式                        
                        if eval(keyword_replace(event.expression, assignments)):  # 把表达式中的变量替换为字典中对应的字段值，调用解释器执行，如果结果为真，说明业务事件发生，调度后续作业
                            print('表达式为真，触发事件：', event)
                            operation_scheduler(event, event_params)

    except:
        print('operand_finished_handler => 无作业进程')


# ******************************************
# 业务事件处理：
# 系统内置业务事件：注册，用户登录，用户退出
# ******************************************
# 收到注册成功信号，生成用户注册事件：registration.signals.user_registered
@receiver(user_registered)
def user_registered_handler(sender, user, request, **kwargs):
    params={'uid': None, 'cid': user.id, 'ppid': 0}
    event = Event.objects.get(name=SYSTEM_EVENTS[0][1])  # 系统内置用户注册事件编码
    operation_scheduler(event, params)  # 把Event和参数发给调度器


# 收到登录信号，生成用户/职员登录事件
@receiver(user_logged_in)
def user_logged_in_handler(sender, user, request, **kwargs):
    # 用户登录Session登记
    ip_address = get_client_ip(request)
    session_key = request.session.session_key
    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key
    )

    # 登录事件调度
    params={'uid': user.id, 'cid': user.id}
    if user.is_staff:  # 系统内置登录事件编码
        event_name = SYSTEM_EVENTS[2][1]   # 职员登录
        params['ppid'] = 0
        print('职员登录', user, event_name)
    else:
        event_name = SYSTEM_EVENTS[1][1]   # 客户登录
        params['ppid'] = 0

    try:
        event = Event.objects.get(name=event_name)
        operation_scheduler(event, params)  # 把Event和参数发给调度器
    except Exception as e:
        traceback.print_exc()
        print('except: user_logged_in_handler.operation_scheduler:', e)


@receiver(post_save, sender=User)
def user_post_save_handler(sender, instance, created, **kwargs):
    if not created:
        if instance.is_staff:
            if Staff.objects.filter(user=instance).exists():
                print('更新员工信息', instance)            
                instance.staff.name = instance.last_name+instance.first_name
                instance.staff.email = instance.email
                instance.staff.save()
            else:
                print('创建员工信息', instance)
                Staff.objects.create(
                    user=instance,
                    name=instance.last_name+instance.first_name,
                    email=instance.email,
                )
        else:
            if Customer.objects.filter(user=instance).exists():
                print('更新客户信息', instance)
                instance.customer.name = instance.last_name+instance.first_name
                instance.customer.save()
            else:
                print('创建客户信息', instance)
                Customer.objects.create(
                    user=instance,
                    name=instance.last_name+instance.first_name,
                )


@receiver(m2m_changed, sender=User.groups.through)
def user_m2m_changed_handler(sender, instance, **kwargs):
    if instance.is_staff:
        instance.staff.role.set(instance.groups.all())


# @receiver(post_delete, sender=User)
# def user_post_delete_handler(sender, instance, **kwargs):
#     if instance.is_staff:
#         instance.staff.delete()
#     else:
#         instance.customer.delete()


# 从app forms里获取所有表单model的名字, 用以判断post_save的sender
# from django.apps import apps
# Forms_models = apps.get_app_config('forms').get_models()
# form_list = []
# for Model in Forms_models:
#     form_list.append(Model.__name__)


# 监视事件表Event变更，变更事件后续作业时，同步变更事件指令表Event_instructions的内容
@receiver(m2m_changed, sender=Event.next.through)
def event_m2m_changed_handler(sender, instance, action, **kwargs):

    # 设定指令为 create_operation_proc
    instruction_create_operation_proc = Instruction.objects.get(name='create_operation_proc')

    # 获取后续作业
    next_operations = []
    if action == 'post_add':
        next_operations = instance.next.all()
        print('!!post_add:', next_operations)
    elif action == 'post_remove':
        next_operations = instance.next.all()
        print('##post_remove:', next_operations)
    
    # 删除原有事件指令
    Event_instructions.objects.filter(event=instance).delete()

    # 新增事件指令
    for operation in next_operations:
        Event_instructions.objects.create(
            event=instance,
            instruction=instruction_create_operation_proc,
            order=1,
            params=operation.name,    # 用后续作业name作为指令参数
        )


# 监视事件表变更，管理员删除事件表Event时，同步删除事件指令表Event_instructions的内容
@receiver(post_delete, sender=Event)
def event_post_delete_handler(sender, instance, **kwargs):
    Event_instructions.objects.filter(event=instance).delete()
