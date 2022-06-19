from celery import shared_task
from django.utils import timezone
from datetime import timedelta


@shared_task(bind=True)
def test_task(self):
    for i in range(10):
        print(f'{i}')
    return 'Done'


@shared_task(bind=True)
# 检查服务进程是否等待安排超时
def check_proc_timeout(self):
    from core.models import OperationProc
    # 获取所有等待中的服务进程
    procs = OperationProc.objects.filter(state=0)
    for proc in procs:
        # 获取进程的计划执行时间
        scheduled_time = proc.scheduled_time
        # 获取受理时限
        awaiting_time_frame = proc.service.awaiting_time_frame
        # 计算超时时间
        timeout_time = scheduled_time + timedelta(seconds=awaiting_time_frame)
        # 如果超时时间小于当前时间，则设置进程为超时状态
        if timeout_time < timezone.now():
            proc.state = 10
            proc.save()
            return '服务进程等待超时'