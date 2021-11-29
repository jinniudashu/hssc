# Generated by Django 3.2.6 on 2021-11-29 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customized_forms', '0010_auto_20211128_1744'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='numberfield',
            name='display_unit',
        ),
        migrations.AddField(
            model_name='numberfield',
            name='required',
            field=models.BooleanField(default=False, verbose_name='必填'),
        ),
    ]
