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

# 导入作业事件表、指令表
from core.models import Form, Operation, Event, Event_instructions, Instruction, Operation_proc

# 导入任务
from core.tasks import create_operation_proc

# 从app forms里获取所有表单model的名字
from django.apps import apps
Forms_models = apps.get_app_config('forms').get_models()
form_list = []
for Model in Forms_models:
    form_list.append(Model.__name__)
print('<来自eventor.py>当前Forms:', form_list)


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


# ********************
# 作业进程设置
# ********************
# 监视Form的新增条目，同步表单作业
@receiver(post_save, sender=Form)
def form_post_save_handler(sender, instance, created, **kwargs):
    if created:     # 新增Operation表xx表单作业
        Operation.objects.create(
            name = instance.name,
            label = f'{instance.label}作业',
            form = instance,
        )
        print('create 作业：', instance.label)


# 监视作业表Operation的新增作业时，同步新增事件表作业完成事件
@receiver(post_save, sender=Operation)
def event_post_save_handler(sender, instance, created, **kwargs):
    if created:     # 新增Event表xx作业完成事件
        name = instance.get_event_name_operation_completed()
        label = instance.get_event_label_operation_completed()
        Event.objects.create(
            operation = instance,
            name = name,
            label = label,
        )
        print('create 事件：', label)


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
# rtc: 表单作业完成，查询事件表，调度后续作业进程
@receiver(post_save, sender=Operation_proc)
def new_operation_proc(instance, created, **kwargs):
    if created: # ctr
        print ('###!!!!!!### New operation_proc:', instance)
    else:
        if instance.state == 4:  # rtc            
            print('rtc状态, 查询表单完成事件，进行调度')

            params={
                'uid': instance.user.id,
                'cid': instance.customer.id,
                'ppid': instance.id
            }
            event_name = instance.operation.get_event_name_operation_completed()
            event = Event.objects.filter(name=event_name)
            operation_scheduler(event[0], params)


# rtc: 收到表单保存信号，更新作业进程状态: rtc
@receiver(post_save, sender=None, weak=True, dispatch_uid=None)
def form_post_save_handler(sender, instance, created, **kwargs):
    print("表单保存：form_post_save_handler")

    # 如果sender在Formlist里且非Created，更新作业进程状态
    if not created:
        print('sender:', instance.__class__.__name__, instance.__class__.__name__ in form_list)
        if instance.__class__.__name__ in form_list:
            slug = instance.slug
            proc = Operation_proc.objects.filter(entry=slug)
            pid = proc[0].id
            ocode = 'rtc'
            update_operation_proc(pid, ocode)
            print('重定向', 'pid:', pid, 'ocode:', ocode)
            # return redirect('http://127.0.0.1:8000/')
            return redirect(reverse('forms:index'))

# rtr: 操作员get表单记录/操作员进入作业入口



# ******************************************
# 内置业务事件处理：注册，用户登录，用户退出
# ******************************************
# 系统内置事件(event_id, event_name)
SYSTEM_EVENTS = {
    'user_registered': 49,
    'customer_logged_in': 51,
    'staff_logged_in': 52,
}


# 收到注册成功信号，生成用户注册事件
# registration.signals.user_registered
@receiver(user_registered)
def user_registered_handler(sender, user, request, **kwargs):

    params={
        'uid': user.id,
        'cid': user.id,
        'ppid': SYSTEM_EVENTS['user_registered']
    }
    # 系统内置用户注册事件编码
    event = Event.objects.get(id=SYSTEM_EVENTS['user_registered'])

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
        event_id = SYSTEM_EVENTS['staff_logged_in']   # 职员登录
        params['ppid'] = SYSTEM_EVENTS['staff_logged_in']
        print('职员登录', user, event_id)
    else:
        event_id = SYSTEM_EVENTS['customer_logged_in']   # 客户登录
        params['ppid'] = SYSTEM_EVENTS['customer_logged_in']

    event = Event.objects.get(id=event_id)
    print('职员登录', user, event)

    # 把Event和参数发给调度器
    operation_scheduler(event, params)
