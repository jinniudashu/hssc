# Generated by Django 3.2.6 on 2023-05-31 07:37

import datetime
from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20230531_1537'),
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerschedule',
            name='reference_operation',
            field=models.ManyToManyField(blank=True, limit_choices_to=models.Q(('created_time__gte', datetime.datetime(2023, 5, 24, 15, 37, 10, 24689)), ('customer', django.db.models.expressions.F('customer')), ('service__service_type', 2)), to='core.OperationProc', verbose_name='引用表单'),
        ),
    ]
