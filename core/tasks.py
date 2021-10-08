from django.contrib.auth.models import User

# from __future__ import absolute_import, unicode_literals
from celery import shared_task
# from celery.decorators import task
# from celery.utils.log import get_task_logger
# logger = get_task_logger(__name__)

from core.models import Operation_proc, Operation, Service_proc

'''
指令字典
    'cop': create_operation_proc,
    'mop': update_operation_proc,
    'cfi': create_form_instance,

# 作业状态机操作码
    ('cre', 'CREATE'),
    ('ctr', 'CREATED TO READY'),
    ('rtr', 'READY TO RUNNING'),
    ('rth', 'RUNNING TO HANGUP'),
    ('htr', 'HANGUP TO READY'),
    ('rtc', 'RUNNING TO COMPLETED'),
'''


# 创建作业进程
# @shared_task
def create_operation_proc(task_params):

    # 创建表单实例
    # 获取作业表单
    # forms = operation.forms
    # print('forms:', forms)
    # for form in forms:
    #     Form = globals()[form]
    #     form = Form.objects.create()

    # 获取表单实例入口
    # entry = 

    # 创建作业进程
    operation = Operation.objects.get(id=task_params['oid'])
    user = User.objects.get(id=task_params['uid'])
    customer = User.objects.get(id=task_params['cid'])
    try:
        parent_operation_proc = Operation_proc.objects.get(id=task_params['ppid'])
    except Operation_proc.DoesNotExist:
        parent_operation_proc = None
    # service_proc = Service_proc.objects.get(id=task_params['spid'])

    proc=Operation_proc.objects.create(
        operation=operation,
        user=user,
        customer=customer,
        state=0,
        ppid=parent_operation_proc,
        # entry = entry
        # service_proc=service_proc,
    )


    return proc


# 维护作业进程
# @shared_task
def update_operation_proc(opid, ocode):
    print ('maintenance_operation_proc', opid, ocode)
    proc = Operation_proc.objects.get(id=opid)

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
