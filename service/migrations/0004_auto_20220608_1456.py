# Generated by Django 3.2.6 on 2022-06-08 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_auto_20220608_1136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fen_zhen_que_ren',
            name='boolfield_shen_fen_zheng_jian_fu_jian',
        ),
        migrations.AddField(
            model_name='fen_zhen_que_ren',
            name='boolfield_shen_fen_xin_xi_yan_zheng',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='身份信息验证'),
        ),
    ]
