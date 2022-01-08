from django.contrib.auth.models import User
from forms.models import *
import json

# from __future__ import absolute_import, unicode_literals
from celery import shared_task
# from celery.decorators import task
# from celery.utils.log import get_task_logger
# logger = get_task_logger(__name__)

from core.models import Operation_proc, Operation, Service_proc

'''
指令字典
    新建作业进程（'cop'）: create_operation_proc,
'''

# 创建作业进程
# @shared_task
def create_operation_proc(task_params):
    oid = task_params['oid']
    operation = Operation.objects.get(id=oid)
    user = User.objects.get(id=task_params['uid'])
    customer = User.objects.get(id=task_params['cid'])

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
        # service_proc=service_proc,
    )

    # 根据Operation.forms创建相关表单实例
    form_slugs = []
    for form in json.loads(operation.forms):
        form_class_name = form['name'].capitalize()
        print('创建表单实例:', form_class_name)
        form = globals()[form_class_name].objects.create(
            user = user,
            customer = customer,
            pid = proc.id
        )
        form_slugs.append((form_class_name, form.slug))

    proc.entry = 'update_view<str:pid>'      # 更新视图URL路径？？？ 
    proc.form_slugs = form_slugs    # 数组转字符串格式转换？？？
    proc.save()

    return proc