# Generated by Django 3.2.6 on 2023-10-03 12:19

import datetime
from django.db import migrations, models
import django.db.models.expressions
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_taskproc'),
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerschedule',
            name='reference_operation',
            field=models.ManyToManyField(blank=True, limit_choices_to=models.Q(('created_time__gte', datetime.datetime(2023, 9, 26, 12, 19, 5, 93832, tzinfo=utc)), ('customer', django.db.models.expressions.F('customer')), ('service__service_type', 2)), to='core.OperationProc', verbose_name='引用表单'),
        ),
    ]
