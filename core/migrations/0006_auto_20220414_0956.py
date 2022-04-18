# Generated by Django 3.2.6 on 2022-04-14 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20220414_0933'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operation_proc',
            name='operation',
        ),
        migrations.AddField(
            model_name='operation_proc',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.service', verbose_name='服务'),
        ),
    ]
