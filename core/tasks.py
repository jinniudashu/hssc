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
    procs = OperationProc.objects.filter(state=0)
    for proc in procs:
        # 获取进程的计划执行时间
        scheduled_time = proc.scheduled_time
        # 获取受理时限
        awaiting_timeout = proc.service.awaiting_time_frame
        if awaiting_timeout:
            # 计算超时时间
            timeout_time = scheduled_time + awaiting_timeout
            # 如果超时时间小于当前时间，则设置进程为超时状态
            if timeout_time < timezone.now():
                proc.state = 10
                proc.save()
                print('服务进程等待超时')

    # 执行超时检查execution_time_frame
    # 获取所有已安排的服务进程
    procs = OperationProc.objects.filter(state__in=[1, 2, 3,])
    for proc in procs:
        # 获取进程的计划执行时间
        scheduled_time = proc.scheduled_time
        # 获取执行时限
        execution_timeout = proc.service.execution_time_frame
        if execution_timeout:
            # 计算超时时间
            timeout_time = scheduled_time + execution_timeout
            # 如果超时时间小于当前时间，则设置进程为超时状态
            if timeout_time < timezone.now():
                # proc.state = 20
                # proc.save()
                print('服务进程执行超时')
