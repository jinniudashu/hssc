# Generated by Django 3.2.6 on 2021-10-14 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_auto_20211010_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='instruction',
            name='label',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='显示名称'),
        ),
        migrations.AlterField(
            model_name='instruction',
            name='name',
            field=models.CharField(db_index=True, max_length=100, unique=True, verbose_name='指令名称'),
        ),
    ]