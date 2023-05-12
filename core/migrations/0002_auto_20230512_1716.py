# Generated by Django 3.2.6 on 2023-05-12 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='bsyz',
            field=models.CharField(max_length=255, null=True, verbose_name='不适应症'),
        ),
        migrations.AddField(
            model_name='medicine',
            name='fypc',
            field=models.CharField(max_length=255, null=True, verbose_name='服用频次'),
        ),
        migrations.AddField(
            model_name='medicine',
            name='fytj',
            field=models.CharField(max_length=255, null=True, verbose_name='服用途径'),
        ),
        migrations.AddField(
            model_name='medicine',
            name='fyzysxhbz',
            field=models.CharField(max_length=255, null=True, verbose_name='服用注意事项和备注'),
        ),
        migrations.AddField(
            model_name='medicine',
            name='syz',
            field=models.CharField(max_length=255, null=True, verbose_name='适应症'),
        ),
    ]