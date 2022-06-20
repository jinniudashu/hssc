# Generated by Django 3.2.6 on 2022-06-20 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_servicepackagedetail_after_base_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicepackagedetail',
            name='after_base_duration',
        ),
        migrations.AddField(
            model_name='servicepackagedetail',
            name='base_interval',
            field=models.DurationField(blank=True, help_text='例如：3 days, 22:00:00', null=True, verbose_name='基准间隔'),
        ),
    ]