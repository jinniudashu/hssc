from celery import shared_task
from django.utils import timezone
from datetime import timedelta

@shared_task(bind=True)
def test_task(self):
    for i in range(10):
        print(f'{i}')
    return 'Done'