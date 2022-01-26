'''
服务调度器：
1. 事件发生器: 根据Signals参数生成业务事件
2. 调度器：根据业务事件查找任务指令，向Celery发送任务指令

业务完成事件命名规则: [form_name]_operation_completed
'''
from django.dispatch import receiver, Signal
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.contrib.auth.signals import user_logged_in, user_logged_out
from registration.signals import user_registered, user_activated, user_approved
import traceback

# 导入作业事件表、指令表
from core.models import Operation, Event, Event_instructions, Instruction, Operation_proc
from core.models import SYSTEM_EVENTS

# 导入自定义表单models
from django.contrib.contenttypes.models import ContentType

# 导入任务
from core.tasks import create_operation_proc

# 导入作业完成信号
from core.signals import operand_finished

from core.utils import keyword_replace
from core.interpreter import interpreter

# 导入UserSession
from analytics.models import UserSession
from analytics.utils import get_client_ip

# 从app forms里获取所有表单model的名字, 用以判断post_save的sender
from django.apps import apps
Forms_models = apps.get_app_config('forms').get_models()
form_list = []
for Model in Forms_models:
    form_list.append(Model.__name__)


# 维护作业进程状态：
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
        # 执行task.create_operation_proc
        print('send:', instruction.instruction.name, task_func)
        globals()[task_func](task_params)

        # 调用Celery @task执行指令
        # globals()[task_func].delay(task_params)
        # eval(task_func).delay(oid, '', '')

    return


# ********************
# 作业进程设置
# ********************

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
            print('rtc状态, 作业完成事件，进行调度')


# ******************************
# 接收来自作业视图的自定义信号
# ******************************
@receiver(operand_finished)
def operand_finished_handler(sender, **kwargs):
    pid = kwargs['pid']
    ocode = kwargs['ocode']
    field_values = kwargs['field_values']

    print('收到作业完成消息：', pid, ocode, field_values.getlist('out_of_hospital_self_report_survey-relatedfield_symptom_list'))

    # 1. 更新作业进程状态: rtc
    try:
        print ('更新作业进程状态：', pid, ocode)
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
        # proc.save()

        # 检查规则表，判断当前作业有规定业务事件需要检查, 如有取出规则集，逐一检查表达式是否为真，触发业务事件, 决定后续作业
        events = Event.objects.filter(operation = proc.operation)
        if events:
            for event in events:
                expr = event.expression     # 提取表达式
                event_params={              # 构造事件参数
                    'uid': proc.operator.id,
                    'cid': proc.customer.id,
                    'ppid': proc.ppid
                }
                # 判断是否为作业完成事件“completed”（保留事件）
                if event.name.endswith('_completed'):
                    pass
                    # operation_scheduler(event, event_params)
                # 检查作业事件
                else:   
                    fields = event.parameters.split(', ')   # 提取其中的表单字段名, 转换为数组
                    assignments={}                          # 构造表达式变量字典

                    i_fields = field_values.lists()
                    while True:
                        try:
                            item = next(i_fields)
                            print(item, len(item[1]))
                        except StopIteration:
                            break

                    for field in fields:
                        value = field_values[field]  # 获取相应变量的表单字段值（form.field的值）
                        assignments[field] = f'{value}'.replace(' ', '')  # 去除字符串值的空格
                    print('assignments', assignments)
                    expr_for_calcu = keyword_replace(expr, assignments)  # 把表达式中的变量替换为值

                    if interpreter(expr_for_calcu):  # 调用解释器执行表达式，如果结果为真，调度后续作业
                        print('表达式为真，触发事件：', event)
                        # operation_scheduler(event, event_params)

    except:
        print('operand_finished_handler => 无作业进程')


# 收到表单保存信号
@receiver(post_save, sender=None, weak=True, dispatch_uid=None)
def form_post_save_handler(sender, instance, created, **kwargs):

    # 如果用户登录，中止该用户其它会话
    if sender == UserSession and created:
        qs = UserSession.objects.filter(user=instance.user, ended=False).exclude(id=instance.id)
        for s in qs:
            s.end_session()

# ******************************************
# 业务事件处理：
# 系统内置业务事件：注册，用户登录，用户退出
# ******************************************

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

    # 用户登录Session登记
    ip_address = get_client_ip(request)
    session_key = request.session.session_key
    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key
    )

    # 登录事件调度
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
    except Exception as e:
        traceback.print_exc()
        print('except: user_logged_in_handler.operation_scheduler:', e)


# request.user会给你一个User对象，表示当前登录用户。
# 如果用户当前未登录，request.user将被设置为AnonymousUser。
# 可以用is_authenticated()：
# if request.user.is_authenticated():
#     # Do something for authenticated users.
# else:
#     # Do something for anonymous users.
