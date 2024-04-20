# Generated by Django 3.2.6 on 2024-04-09 12:35

import datetime
from django.db import migrations, models
import django.db.models.expressions
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_recommendedservice_receive_data_from'),
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerschedule',
            name='reference_operation',
            field=models.ManyToManyField(blank=True, limit_choices_to=models.Q(('created_time__gte', datetime.datetime(2024, 4, 2, 12, 35, 46, 244987, tzinfo=utc)), ('customer', django.db.models.expressions.F('customer')), ('service__service_type', 2)), to='core.OperationProc', verbose_name='引用表单'),
        ),
    ]
