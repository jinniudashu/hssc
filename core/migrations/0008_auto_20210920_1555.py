# Generated by Django 3.2.6 on 2021-09-20 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_instruction_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instruction',
            name='name',
        ),
        migrations.RemoveField(
            model_name='operation',
            name='service',
        ),
        migrations.RemoveField(
            model_name='service',
            name='init_operation',
        ),
        migrations.AddField(
            model_name='service',
            name='Operation',
            field=models.ManyToManyField(to='core.Operation', verbose_name='作业'),
        ),
    ]