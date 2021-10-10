from django.contrib.auth.models import User
from forms.models import *

# from __future__ import absolute_import, unicode_literals
from celery import shared_task
# from celery.decorators import task
# from celery.utils.log import get_task_logger
# logger = get_task_logger(__name__)

from core.models import Operation_proc, Operation, Service_proc

'''
指令字典
    'cop': create_operation_proc,
'''

# 创建作业进程
# @shared_task
def create_operation_proc(task_params):
    operation = Operation.objects.get(id=task_params['oid'])
    user = User.objects.get(id=task_params['uid'])
    customer = User.objects.get(id=task_params['cid'])

    # 创建表单实例
    # 获取作业表单
    form_class_name = operation.form.name.capitalize()
    print('创建表单实例:', form_class_name)
    form = globals()[form_class_name].objects.create(
        user = user,
        customer = customer,
    )
    entry = form.slug

    # 创建作业进程
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
        entry = entry
        # service_proc=service_proc,
    )

    return proc