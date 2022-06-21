from celery import shared_task
from django.utils import timezone


@shared_task(bind=True)
def test_task(self):
    for i in range(10):
        print(f'{i}')
    return 'Done'


# 检查服务进程是否等待安排超时
@shared_task(bind=True)
def check_proc_awaiting_timeout(self):
    from core.models import OperationProc

    # 受理超时检查
    # 获取所有等待中的服务进程
    procs = OperationProc.objects.filter(state=0, acceptance_timeout=False)
    for proc in procs:
        # 获取进程的计划执行时间
        scheduled_time = proc.scheduled_time
        # 获取受理时限
        working_hours = proc.service.working_hours
        if working_hours:
            # 计算超时时间
            timeout_time = scheduled_time + working_hours
            # 如果超时时间小于当前时间，则设置进程为超时状态
            if timeout_time < timezone.now():
                proc.acceptance_timeout = True
                proc.save()
                print('受理超时')

    # 执行超时检查overtime
    # 获取所有已安排的服务进程
    procs = OperationProc.objects.filter(state__in=[1, 2, 3,], completion_timeout=False)
    for proc in procs:
        # 获取进程的计划执行时间
        scheduled_time = proc.scheduled_time
        # 获取超时时限
        overtime = proc.service.overtime
        if overtime:
            # 计算超时时间
            timeout_time = scheduled_time + overtime
            # 如果超时时间小于当前时间，则设置进程为超时状态
            if timeout_time < timezone.now():
                proc.completion_timeout = True
                proc.save()
                print('超期超时')
