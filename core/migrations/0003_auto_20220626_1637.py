# Generated by Django 3.2.6 on 2022-06-26 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_servicepackagedetail_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicepackagedetail',
            name='cycle_option',
        ),
        migrations.RemoveField(
            model_name='servicepackagedetail',
            name='duration',
        ),
        migrations.AddField(
            model_name='servicepackagedetail',
            name='cycle_frequency',
            field=models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='每周期频次'),
        ),
        migrations.AddField(
            model_name='servicepackagedetail',
            name='cycle_unit',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, '总共'), (1, '每天'), (2, '每周'), (3, '每月'), (4, '每季'), (5, '每年')], default=0, null=True, verbose_name='周期单位'),
        ),
        migrations.AlterField(
            model_name='servicepackagedetail',
            name='cycle_times',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='周期总数'),
        ),
    ]
