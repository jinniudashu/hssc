# from __future__ import absolute_import, unicode_literals

from celery import shared_task
# from celery.decorators import task
# from celery.utils.log import get_task_logger
# logger = get_task_logger(__name__)

# @task(name='operation_proc_create_task')
# def operation_proc_create_task(x, y):
#     logger.info('Create operation process ...')
#     return operation_proc_create(x, y)

@shared_task
def operation_proc_create(x, y):
    print ('operation_proc_create')
    return x * y

@shared_task
def operation_proc_update(x, y):
    print ('operation_proc_update')
    return x + y

@shared_task
def operation_proc_delete(x, y):
    print ('operation_proc_delete')
    return x - y