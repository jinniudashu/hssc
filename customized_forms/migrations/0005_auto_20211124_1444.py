# Generated by Django 3.2.6 on 2021-11-24 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customized_forms', '0004_auto_20211124_1438'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='charfield',
            options={'verbose_name': '字符字段', 'verbose_name_plural': '字符字段'},
        ),
        migrations.AlterModelOptions(
            name='datetimefield',
            options={'verbose_name': '日期字段', 'verbose_name_plural': '日期字段'},
        ),
        migrations.AlterModelOptions(
            name='numberfield',
            options={'verbose_name': '数值字段', 'verbose_name_plural': '数值字段'},
        ),
    ]
