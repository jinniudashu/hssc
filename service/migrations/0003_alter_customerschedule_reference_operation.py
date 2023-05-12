# Generated by Django 3.2.6 on 2023-05-12 09:51

import datetime
from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_eventrule_event_type'),
        ('service', '0002_alter_customerschedule_reference_operation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerschedule',
            name='reference_operation',
            field=models.ManyToManyField(blank=True, limit_choices_to=models.Q(('created_time__gte', datetime.datetime(2023, 5, 5, 17, 51, 34, 190747)), ('customer', django.db.models.expressions.F('customer')), ('service__service_type', 2)), to='core.OperationProc', verbose_name='引用表单'),
        ),
    ]