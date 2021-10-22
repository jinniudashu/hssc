# Generated by Django 3.2.6 on 2021-09-21 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20210921_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event_instruction',
            name='rule',
        ),
        migrations.AddField(
            model_name='rule',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.event_instruction', verbose_name='产生事件'),
        ),
    ]