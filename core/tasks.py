# from __future__ import absolute_import, unicode_literals

from celery import shared_task
# from celery.decorators import task
# from celery.utils.log import get_task_logger
# logger = get_task_logger(__name__)

# @task(name='operation_proc_create_task')
# def operation_proc_create_task(x, y):
#     logger.info('Create operation process ...')
#     return operation_proc_create(x, y)


# 操作码
OPERATING_CODE = [
    ('cre', 'CREATE'),
    ('ctr', 'CREATED TO READY'),
    ('rtr', 'READY TO RUNNING'),
    ('rth', 'RUNNING TO HANGUP'),
    ('htr', 'HANGUP TO READY'),
    ('rtc', 'RUNNING TO COMPLETED'),
]

@shared_task
# 维护作业进程
def maintenance_operation_proc(oid, ocode):
    print ('maintenance_operation_proc', oid, ocode)
    if ocode == 'cre':
        print(OPERATING_CODE[0][1])
        return OPERATING_CODE[0][1]
    elif ocode == 'ctr':
        print(OPERATING_CODE[1][1])
        return OPERATING_CODE[1][1]
    elif ocode == 'rtr':
        print(OPERATING_CODE[2][1])
        return OPERATING_CODE[2][1]
    elif ocode == 'rth':
        print(OPERATING_CODE[3][1])
        return OPERATING_CODE[3][1]
    elif ocode == 'htr':
        print(OPERATING_CODE[4][1])
        return OPERATING_CODE[4][1]
    elif ocode == 'rtc':
        print(OPERATING_CODE[5][1])
        return OPERATING_CODE[5][1]
    else:
        print(f'ERROR: 未定义的操作码 ocode: {ocode}')
    return f'ERROR: 未定义的操作码 ocode: {ocode}'

@shared_task
# 创建作业进程
def operation_proc_create(x, y):
    print ('operation_proc_create')
    return x * y

@shared_task
# 跟新作业进程状态
def operation_proc_update(x, y):
    print ('operation_proc_update')
    return x + y

@shared_task
# 删除作业进程
def operation_proc_delete(x, y):
    print ('operation_proc_delete')
    return x - y


@shared_task
# 创建表单
def form_create():    
    return print('form_create')

@shared_task
# 修改表单
def form_update():
    return print('form_update')