'''
服务调度器：
1. 事件发生器: 把Django表单Signals转为Icpc编码的业务事件
2. 调度器：根据Icpc业务事件查找任务指令，向Celery发送任务指令
'''
# 导入作业事件表、指令表
from core.models import Event, Event_instructions, Instruction, Operation_proc

from django.contrib.auth.models import User

from django.dispatch import receiver, Signal
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.contrib.auth.signals import user_logged_in, user_logged_out
from registration.signals import user_registered, user_activated, user_approved

# 导入任务
from core.tasks import create_operation_proc, update_operation_proc

# 从app forms里获取所有表单model的名字
# from django.apps import apps
# Forms_models = apps.get_app_config('forms').get_models()
# print('<来自eventor.py>当前Forms:')
# for Model in Forms_models:
#     print(Model.__name__)


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


'''
业务事件编码规则：form_name + create

事件参数: 
task_params = {}
oid, 
uid, 
cid, 
ppid, 
spid,
opid, 
ocode, 
form
'''

# ****************************************
# 系统内置作业事件：注册，用户登录，用户退出
# ****************************************
# 系统内置事件(event_id, event_name)
SYSTEM_EVENTS = [
    (1,"用户注册"), 
    (4,"客户登录"), 
    (5,"职员登录"),
    (7,"客户退出"), 
    (8,"职员退出"),
]


# 收到注册成功信号，生成用户注册事件
# registration.signals.user_registered
@receiver(user_registered)
def user_registered_handler(sender, user, request, **kwargs):

    params={
        'uid': user.id,
        'cid': user.id,
        'ppid': SYSTEM_EVENTS[0][0]
    }
    # 系统内置用户注册事件编码
    event = Event.objects.get(id=SYSTEM_EVENTS[0][0])

    # 把Event和参数发给调度器
    operation_scheduler(event, params)


# 收到登录信号，生成用户/职员登录事件
@receiver(user_logged_in)
def user_logged_in_handler(sender, user, request, **kwargs):

    params={
        'uid': user.id,
        'cid': user.id,
    }
    # 系统内置登录事件编码
    if user.is_staff:
        event_id = SYSTEM_EVENTS[2][0]   # 职员登录
        params['ppid'] = SYSTEM_EVENTS[2][0]
    else:
        event_id = SYSTEM_EVENTS[1][0]   # 客户登录
        params['ppid'] = SYSTEM_EVENTS[1][0]

    event = Event.objects.get(id=event_id)

    # 把Event和参数发给调度器
    operation_scheduler(event, params)


# 收到logout信号，生成用户/职员退出事件
@receiver(user_logged_out)
def user_logged_out_handler(sender, user, request, **kwargs):

    params={
        'uid': user.id,
        'cid': user.id,
    }
    # 系统内置退出事件编码
    if user.is_staff:   # user是职员或用户
        event_id = SYSTEM_EVENTS[4][0]    # 职员退出
        params['ppid'] = SYSTEM_EVENTS[4][0]
    else:
        event_id = SYSTEM_EVENTS[3][0]    # 客户退出
        params['ppid'] = SYSTEM_EVENTS[3][0]

    event = Event.objects.get(id=event_id)

    # 把Event和参数发给调度器
    operation_scheduler(event, params)


# ********************
# 作业进程设置
# ********************
# 监视事件表Event变更，新增事件时，同步新增事件指令表Event_instructions的内容
# @receiver(post_save, sender=Event)
# def event_post_save_handler(sender, instance, created, **kwargs):
#     if created:     # 新增Event_instructions指令
#         print('create event instance', instance)
#         print('from:', instance.operation)


# 监视事件表Event变更，变更事件后续作业时，同步变更事件指令表Event_instructions的内容
@receiver(m2m_changed, sender=Event.next.through)
def event_m2m_changed_handler(sender, instance, action, **kwargs):

    # 设定指令为 create_operation_proc, 在指令表中id=1
    instruction_create_operation_proc = Instruction.objects.get(id=1)

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
@receiver(post_save, sender=Operation_proc)
def new_operation_proc(instance, created, **kwargs):
    if created:
        print ('###!!!!!!### New operation_proc:', instance)


# rtc: 收到表单保存信号, 生成表单作业完成事件
@receiver(post_save, sender=None, weak=True, dispatch_uid=None)
def form_post_save_handler(sender, instance, created, **kwargs):
    print("表单保存：form_post_save_handler")
    print('sender:', sender)
    print('instance name:', instance.__class__.__name__)    
    if not created:
        params={}
        params['form']=instance.__class__.__name__
        params['ocode']='rtc'
        # 发送业务事件编码
        # event = SYSTEM_EVENTS[0]
        # operation_scheduler(event, params)


# rtr: 操作员get表单记录/操作员进入作业入口
