from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from pytz import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hssc.settings')

app = Celery('hssc')
# app = Celery('hssc', backend='redis://localhost', broker='pyamqp://')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Shanghai')

app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'From celery.py, Request: {self.request!r}')