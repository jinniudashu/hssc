# Generated by Django 3.2.6 on 2021-11-29 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customized_forms', '0011_auto_20211129_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numberfield',
            name='max_digits',
            field=models.PositiveSmallIntegerField(blank=True, default=10.23, null=True, verbose_name='最大位数'),
        ),
    ]
