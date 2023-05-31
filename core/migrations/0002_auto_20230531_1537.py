# Generated by Django 3.2.6 on 2023-05-31 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buessinessform',
            name='form_class',
            field=models.PositiveSmallIntegerField(choices=[(1, '调查类'), (2, '诊断类'), (3, '治疗类')], null=True, verbose_name='表单类型'),
        ),
        migrations.AddField(
            model_name='eventrule',
            name='form_class_scope',
            field=models.PositiveSmallIntegerField(choices=[(0, '所有表单'), (1, '调查类'), (2, '诊断类'), (3, '治疗类')], default=0, verbose_name='表单类型范围'),
        ),
    ]
