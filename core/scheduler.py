'''
服务调度器：
1. 事件发生器: 把Django表单Signals转为Icpc编码的业务事件
2. 调度器：根据Icpc业务事件查找任务指令，向Celery发送任务指令

业务事件命名规则: [form_name]_operation_completed

事件参数: 
task_params = {}
oid, 
uid, 
cid, 
ppid, 
spid,
pid, 
ocode, 
form

'''
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.dispatch import receiver, Signal
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.contrib.auth.signals import user_logged_in, user_logged_out
from registration.signals import user_registered, user_activated, user_approved
from django.core import serializers
import json

# 导入作业事件表、指令表
from core.models import Form, Operation, Event, Event_instructions, Instruction, Operation_proc

# 导入自定义表单models
from django.contrib.contenttypes.models import ContentType
from customized_forms.models import CharacterField, NumberField, DTField, ChoiceField, Component

# 导入任务
from core.tasks import create_operation_proc

from core.utils import keyword_replace
from core.interpreter import interpreter

# 从app forms里获取所有表单model的名字, 用以判断post_save的sender
from django.apps import apps
Forms_models = apps.get_app_config('forms').get_models()
form_list = []
for Model in Forms_models:
    form_list.append(Model.__name__)


# 维护作业进程状态：
'''
    作业状态机操作码
    ('cre', 'CREATE'),
    ('ctr', 'CREATED TO READY'),
    ('rtr', 'READY TO RUNNING'),
    ('rth', 'RUNNING TO HANGUP'),
    ('htr', 'HANGUP TO READY'),
    ('rtc', 'RUNNING TO COMPLETED'),
'''
def update_operation_proc(pid, ocode):
    print ('maintenance_operation_proc：', pid, ocode)
    proc = Operation_proc.objects.get(id=pid)

    if ocode == 'ctr': # CREATED TO READY
        proc.state=1
    elif ocode == 'rtr': # READY TO RUNNING
        proc.state=2
    elif ocode == 'rth': # RUNNING TO HANGUP
        proc.state=3
    elif ocode == 'htr': # HANGUP TO READY
        proc.state=2
    elif ocode == 'rtc': # RUNNING TO COMPLETED
        proc.state=4
    else:
        print(f'ERROR: 未定义的操作码 ocode: {ocode}')        
        return f'ERROR: 未定义的操作码 ocode: {ocode}'
    return proc.save()


# 作业调度器
def operation_scheduler(event, params):

    # 查找指令集，发送任务指令
    instructions = Event_instructions.objects.filter(event=event)
    # 指令参数
    task_params={
        'uid': params['uid'],
        'cid': params['cid'],
        'ppid': params['ppid'],
    }  

    print('查找指令集，发送任务指令:', event, instructions)

    for instruction in instructions:
        task_params['oid'] = instruction.params
        task_func = instruction.instruction.func

        # 调用函数执行指令
        print('send:', instruction.instruction.name, task_func)
        globals()[task_func](task_params)

        # 调用Celery @task执行指令
        # globals()[task_func].delay(task_params)
        # eval(task_func).delay(oid, '', '')

    return



# 系统内置事件(form, event_name)
SYSTEM_EVENTS = [
    ('user_registry', 'user_registry_completed'),     # 用户注册
    ('user_login', 'user_login_completed'),           # 用户登录
    ('doctor_login', 'doctor_login_completed'),       # 医生注册
]

# ********************
# 作业进程设置
# ********************
# 监视Form的新增条目，同步新增作业
@receiver(post_save, sender=Form)
def form_post_save_handler(sender, instance, created, **kwargs):
    if created:     # 新增Operation表xx表单作业
        operation = Operation.objects.create(
            name = instance.name,
            label = f'{instance.label}作业',
            form = instance,
        )
        print('create 作业：', instance.label)

        # 如果是系统保留作业，生成系统保留事件SYSTEM_EVENTS
        if any(instance.name == fn[0] for fn in SYSTEM_EVENTS):
            sys_event = Event.objects.create(
                operation = operation,
                name = f'{instance.name}_completed',
                label = f'{instance.label}_完成',
                expression = 'completed',
            )
            print('生成系统保留事件：', sys_event)


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
            params=operation.id,    # 用后续作业id作为指令参数
        )


# 监视事件表变更，管理员删除事件表Event时，同步删除事件指令表Event_instructions的内容
@receiver(post_delete, sender=Event)
def event_post_delete_handler(sender, instance, **kwargs):
    Event_instructions.objects.filter(event=instance).delete()


# ********************
# 作业进程运行时
# ********************
# 维护作业进程状态
'''
作业状态机操作码
    ('cre', 'CREATE'),
    ('ctr', 'CREATED TO READY'),
    ('rtr', 'READY TO RUNNING'),
    ('rth', 'RUNNING TO HANGUP'),
    ('htr', 'HANGUP TO READY'),
    ('rtc', 'RUNNING TO COMPLETED'),
'''

# ctr: 作业进程被创建，资源检查
# rtc: 表单作业完成，查询事件表，调度后续作业进程
@receiver(post_save, sender=Operation_proc)
def new_operation_proc(instance, created, **kwargs):
    if created: # ctr
        print ('新作业进程被创建，进行资源请求...：new_operation_proc:', instance)
    else:
        if instance.state == 4:  # rtc            
            print('rtc状态, 查询表单完成事件，进行调度')


# ******************************************
# 业务事件处理：
# 1. 保存业务表单
# 2. 系统内置业务事件：注册，用户登录，用户退出
# ******************************************
# 收到表单保存信号，更新作业进程状态: rtc
@receiver(post_save, sender=None, weak=True, dispatch_uid=None)
def form_post_save_handler(sender, instance, created, **kwargs):

    # 如果保存customized_forms的字段表，则更新Component表
    if sender in [CharacterField, NumberField, DTField, ChoiceField]:
        charfield_type = ContentType.objects.get(app_label='customized_forms', model=sender.__name__.lower())
        if created:
            Component.objects.create(
                content_type = charfield_type, 
                object_id = instance.id, 
                name = instance.name, 
                label = instance.label, 
                # attribute = json.dumps(serializers.serialize('json',[instance])[1:-1]),
                attribute = serializers.serialize('json',[instance])[1:-1],
            )
        else:
            Component.objects.filter(content_type=charfield_type, object_id=instance.id).update(
                name = instance.name, 
                label = instance.label, 
                # attribute = json.dumps(serializers.serialize('json',[instance])[1:-1]),
                attribute = serializers.serialize('json',[instance])[1:-1],
            )
        
        # j = serializers.serialize('json',[instance])[1:-1]
        # print('json:', j['fields'])


    # 如果sender在Formlist里且非Created，更新作业进程状态
    if not created and instance.__class__.__name__ in form_list:
        slug = instance.slug
        try:
            proc = Operation_proc.objects.get(entry=slug)
            pid = proc.id
            ocode = 'rtc'
            update_operation_proc(pid, ocode)   # 更新作业进程状态: rtc
            print('form_post_save_handler => update_operation_proc', 'pid:', pid, 'ocode:', ocode)

            # 检查规则表，根据规则判断数据变更是否触发业务事件，决定后续作业
            # 1. 检查规则表，判断当前作业有规定业务事件需要检查
            events = Event.objects.filter(operation = proc.operation)
            
            # 2. 如有取出规则集，逐一检查表达式是否为真，触发业务事件
            if events:
                for event in events:
                    # 提取表达式
                    expr = event.expression
                    # 构造事件参数
                    event_params={
                        'uid': instance.user.id,
                        'cid': instance.customer.id,
                        'ppid': pid
                    }
                    # 判断是否为保留事件“completed”
                    if event.name == f'{event.operation.name}_completed':
                        print('保留事件：表单完成 ', event)
                        operation_scheduler(event, event_params)
                    else:   # 检查表单事件
                        # 提取其中的表单字段名, 转换为数组
                        fields = event.parameters.split(', ')

                        # 构造表达式参数字典
                        assignments={}
                        # 获取相应参数表单字段值
                        for field in fields:
                            field_value = instance.__dict__[field]
                            if isinstance(field_value, str):
                                value = f'"{field_value}"'.replace(' ', '')
                            else:
                                value = f'{field_value}'
                            assignments[field]=value

                        print(assignments)

                        # 字段值传入表达式
                        expr_for_calcu = keyword_replace(expr, assignments)

                        # 调用解释器执行表达式，如果结果为真，调度后续作业
                        if interpreter(expr_for_calcu):
                            print('表达式为真，触发事件：', event)
                            operation_scheduler(event, event_params)
        except:
            print('form_post_save_handler => 无作业进程')

# 操作员get表单记录/操作员进入作业入口：rtr



# 收到注册成功信号，生成用户注册事件
# registration.signals.user_registered
@receiver(user_registered)
def user_registered_handler(sender, user, request, **kwargs):

    params={
        'uid': user.id,
        'cid': user.id,
        'ppid': 0,
    }
    # 系统内置用户注册事件编码
    try:
        event = Event.objects.get(name=SYSTEM_EVENTS[0][1])
        # 把Event和参数发给调度器
        operation_scheduler(event, params)
    except:
        print('except: SYSTEM_EVENT: [user_registry_completed] DoesNotExist')



# 收到登录信号，生成用户/职员登录事件
@receiver(user_logged_in)
def user_logged_in_handler(sender, user, request, **kwargs):

    params={
        'uid': user.id,
        'cid': user.id,
    }
    # 系统内置登录事件编码
    if user.is_staff:
        event_name = SYSTEM_EVENTS[2][1]   # 职员登录
        params['ppid'] = 0
        print('职员登录', user, event_name)
    else:
        event_name = SYSTEM_EVENTS[1][1]   # 客户登录
        params['ppid'] = 0

    try:
        event = Event.objects.get(name=event_name)
        print('登录', user, event)
        # 把Event和参数发给调度器
        operation_scheduler(event, params)
    except:
        print('except: SYSTEM_EVENT: [user_login_completed / doctor_login_completed] DoesNotExist')
