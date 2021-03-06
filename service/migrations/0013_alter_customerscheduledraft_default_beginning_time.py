# Generated by Django 3.2.6 on 2022-06-28 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0012_alter_customerscheduledraft_cycle_times'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerscheduledraft',
            name='default_beginning_time',
            field=models.PositiveSmallIntegerField(choices=[(1, '当前系统时间'), (2, '首个服务开始时间'), (3, '上个服务结束时间'), (4, '客户出生日期')], default=1, verbose_name='执行时间基准'),
        ),
    ]
