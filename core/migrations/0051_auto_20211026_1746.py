# Generated by Django 3.2.6 on 2021-10-26 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_alter_rule_expression'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rule',
            name='event',
        ),
        migrations.AddField(
            model_name='event',
            name='rule',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.rule', verbose_name='规则'),
        ),
    ]