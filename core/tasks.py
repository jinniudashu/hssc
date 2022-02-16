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
    operation = Operation.objects.get(name=task_params['oname'])
    
    if task_params['uid']:
        user_operater = User.objects.get(id=task_params['uid'])
        operator = Staff.objects.get(user=user_operater)
    else:
        operator = None

    user_customer = User.objects.get(id=task_params['cid'])
    customer = Customer.objects.get(user=user_customer)
    
    operator_groups = task_params['group']


    # 创建作业进程
    try:
        parent_operation_proc = Operation_proc.objects.get(id=task_params['ppid'])
    except Operation_proc.DoesNotExist:
        parent_operation_proc = None
    # service_proc = Service_proc.objects.get(id=task_params['spid'])
    proc=Operation_proc.objects.create(
        operation=operation,
        operator=None,
        customer=customer,
        state=0,
        ppid=parent_operation_proc,
        # service_proc=service_proc,
    )
    proc.group.add(*operator_groups)

    # 根据Operation.forms里的mutate类型的表单创建相关表单实例
    form_slugs = []
    forms = filter(lambda _forms: _forms['mutate_or_inquiry']=='mutate', json.loads(operation.forms))
    for form in forms:
        form_class_name = form['basemodel'].capitalize()
        print('创建表单实例:', form_class_name)
        try:
            form = globals()[form_class_name].objects.create(
                operator = operator,
                customer = customer,
                pid = proc
            )
            form_slugs.append({'form_name': form_class_name, 'slug': form.slug})
        except Exception as e:
            print('创建model失败:', form_class_name, e)

    proc.entry = f'{operation.name}/{proc.id}/update_view'      # 更新作业URL路径 
    proc.form_slugs = json.dumps(form_slugs, ensure_ascii=False, indent=4)
    proc.save()

    return proc