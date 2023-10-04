from django.contrib.contenttypes.models import ContentType
from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from core.models import OperationProc
from service.models import CustomerSchedule
from core.business_functions import create_service_proc, dispatch_operator, eval_scheduled_time

@shared_task(bind=True)
def test_task(self):
    print('这是Celery beat测试!')
    return 'Done'


# 检查服务进程是否等待安排超时
@shared_task(bind=True)
def check_proc_awaiting_timeout(self):
    print('30秒检查一次服务进程是否等待安排超时')

    # 检查任务一：受理超时检查
    # 获取所有等待中的服务进程
    procs = OperationProc.objects.filter(state=0, acceptance_timeout=False)
    for proc in procs:
        # 获取进程的计划执行时间
        scheduled_time = proc.scheduled_time
        # 获取受理时限
        working_hours = proc.working_hours
        if working_hours:
            # 计算超时时间
            timeout_time = scheduled_time + working_hours
            # 如果超时时间小于当前时间，则设置进程为超时状态
            if timeout_time < timezone.now():
                proc.acceptance_timeout = True
                proc.save()
                print('受理超时')


    # 检查任务二：执行超时检查overtime
    # 获取所有已安排的服务进程
    procs = OperationProc.objects.filter(state__in=[1, 2, 3,], completion_timeout=False)
    for proc in procs:
        # 获取进程的计划执行时间
        scheduled_time = proc.scheduled_time
        # 获取超时时限
        overtime = proc.overtime
        if overtime:
            # 计算超时时间
            timeout_time = scheduled_time + overtime
            # 如果超时时间小于当前时间，则设置进程为超时状态
            if timeout_time < timezone.now():
                proc.completion_timeout = True
                proc.save()
                print('超期超时')


    # 检查任务三：7天内的客户日程安排增加到任务队列
    # 从CustomerSchedule表中获取所有7天内应执行的服务进程
    # 检查customer_schedule_list.is_ready=True, 确保从CustomerScheduleList生成CustomerSchedule查询集记录的操作已完成
    schedules = CustomerSchedule.objects.filter(
        scheduled_time__gte=timezone.now(),
        scheduled_time__lte=timezone.now() + timedelta(days=7),
        is_assigned=False,
        customer_schedule_list__is_ready=True
    )
    # if schedules and schedules[0].customer_schedule_list.is_ready:
    if schedules:
        for schedule in schedules:
            '''
            生成后续服务
            '''
            # 准备新的服务作业进程参数
            proc_params = {}
            proc_params['service'] = schedule.service  # 进程所属服务
            proc_params['customer'] = schedule.customer  # 客户
            proc_params['creater'] = schedule.creater   # 创建者
            if schedule.scheduled_operator:
                # 如果有指定执行人，则执行人为指定执行人, 服务进程状态为“就绪”
                service_operator = schedule.scheduled_operator.customer
                state = 1
            else:
                # 如果没有指定执行人，则按照业务规则分配执行人, 服务进程状态为“创建”
                service_operator = dispatch_operator(schedule.customer, schedule.service, schedule.creater, schedule.scheduled_time, None)
                state = 0
            proc_params['operator'] = service_operator  # 操作者 or 根据 责任人 和 服务作业权限判断 
            proc_params['priority_operator'] = schedule.priority_operator  # 优先操作员
            proc_params['state'] = state  # or 根据服务作业权限判断

            # 估算计划执行时间
            # proc_params['scheduled_time'] = eval_scheduled_time(schedule.service, service_operator)
            proc_params['scheduled_time'] = schedule.scheduled_time

            proc_params['parent_proc'] = schedule.pid  # 安排服务/服务包进程是被创建服务进程的父进程
            proc_params['contract_service_proc'] = None  # 所属合约服务进程

            # 区分服务类型是"1 管理调度服务"还是"2 诊疗服务"，获取ContentType
            if schedule.service.service_type == 1:
                content_type = ContentType.objects.get(app_label='service', model='customerschedulepackage')
            else:
                content_type = ContentType.objects.get(app_label='service', model=schedule.service.name.lower())  # 表单类型
            proc_params['content_type'] = content_type

            # 检查是否有引用表单
            if schedule.reference_operation:
                proc_params['passing_data'] = 1  # 传递表单数据：(0, '否'), (1, '接收，不可编辑'), (2, '接收，可以编辑')
            else:
                proc_params['passing_data'] = 0
            
            proc_params['form_data'] = None  # 待复制表单数据不使用
            proc_params['apply_to_group'] = False

            print('客户日程安排增加到服务进程队列:', proc_params)

            # 创建新的服务作业进程
            new_proc = create_service_proc(**proc_params)

            if new_proc:
                schedule.is_assigned = True
                schedule.save()