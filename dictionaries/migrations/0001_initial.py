# Generated by Django 3.2.6 on 2023-03-26 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='An_pai_que_ren',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '安排确认',
                'verbose_name_plural': '安排确认',
            },
        ),
        migrations.CreateModel(
            name='Blood_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '血型',
                'verbose_name_plural': '血型',
            },
        ),
        migrations.CreateModel(
            name='Chang_yong_zheng_zhuang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '常用症状',
                'verbose_name_plural': '常用症状',
            },
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '性格',
                'verbose_name_plural': '性格',
            },
        ),
        migrations.CreateModel(
            name='Comparative_expression',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '比较表达',
                'verbose_name_plural': '比较表达',
            },
        ),
        migrations.CreateModel(
            name='Convenience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '便捷程度',
                'verbose_name_plural': '便捷程度',
            },
        ),
        migrations.CreateModel(
            name='Dan_bai_zhi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '蛋白质',
                'verbose_name_plural': '蛋白质',
            },
        ),
        migrations.CreateModel(
            name='Dorsal_artery_pulsation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '足背动脉搏动情况',
                'verbose_name_plural': '足背动脉搏动情况',
            },
        ),
        migrations.CreateModel(
            name='Edema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '水肿情况',
                'verbose_name_plural': '水肿情况',
            },
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '文化程度',
                'verbose_name_plural': '文化程度',
            },
        ),
        migrations.CreateModel(
            name='Exercise_time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '运动时长',
                'verbose_name_plural': '运动时长',
            },
        ),
        migrations.CreateModel(
            name='Family_relationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '家庭成员关系',
                'verbose_name_plural': '家庭成员关系',
            },
        ),
        migrations.CreateModel(
            name='Frequency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '频次',
                'verbose_name_plural': '频次',
            },
        ),
        migrations.CreateModel(
            name='Fu_wu_jue_se',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '服务角色',
                'verbose_name_plural': '服务角色',
            },
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '性别',
                'verbose_name_plural': '性别',
            },
        ),
        migrations.CreateModel(
            name='Ji_xu_shi_yong_qing_kuang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '继续使用情况',
                'verbose_name_plural': '继续使用情况',
            },
        ),
        migrations.CreateModel(
            name='Marital_status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '婚姻状况',
                'verbose_name_plural': '婚姻状况',
            },
        ),
        migrations.CreateModel(
            name='Medical_expenses_burden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '医疗费用负担',
                'verbose_name_plural': '医疗费用负担',
            },
        ),
        migrations.CreateModel(
            name='Nationality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '民族',
                'verbose_name_plural': '民族',
            },
        ),
        migrations.CreateModel(
            name='Niao_tang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '尿糖',
                'verbose_name_plural': '尿糖',
            },
        ),
        migrations.CreateModel(
            name='Normality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '正常性判断',
                'verbose_name_plural': '正常性判断',
            },
        ),
        migrations.CreateModel(
            name='Occupational_status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '职业状况',
                'verbose_name_plural': '职业状况',
            },
        ),
        migrations.CreateModel(
            name='Pharynx',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '咽部',
                'verbose_name_plural': '咽部',
            },
        ),
        migrations.CreateModel(
            name='Qian_dao_que_ren',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '签到确认',
                'verbose_name_plural': '签到确认',
            },
        ),
        migrations.CreateModel(
            name='Qian_yue_que_ren',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '签约确认',
                'verbose_name_plural': '签约确认',
            },
        ),
        migrations.CreateModel(
            name='Qin_shu_guan_xi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '亲属关系',
                'verbose_name_plural': '亲属关系',
            },
        ),
        migrations.CreateModel(
            name='Satisfaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '满意度',
                'verbose_name_plural': '满意度',
            },
        ),
        migrations.CreateModel(
            name='Shi_mian_qing_kuang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '失眠情况',
                'verbose_name_plural': '失眠情况',
            },
        ),
        migrations.CreateModel(
            name='Sports_preference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '运动类型',
                'verbose_name_plural': '运动类型',
            },
        ),
        migrations.CreateModel(
            name='State_degree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '状态程度',
                'verbose_name_plural': '状态程度',
            },
        ),
        migrations.CreateModel(
            name='Sui_fang_ping_gu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '血压监测评估',
                'verbose_name_plural': '血压监测评估',
            },
        ),
        migrations.CreateModel(
            name='Tang_niao_bing_kong_zhi_xiao_guo_ping_gu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '糖尿病控制效果评估',
                'verbose_name_plural': '糖尿病控制效果评估',
            },
        ),
        migrations.CreateModel(
            name='Tang_niao_bing_zheng_zhuang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '糖尿病症状',
                'verbose_name_plural': '糖尿病症状',
            },
        ),
        migrations.CreateModel(
            name='Tong_ti',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '酮体',
                'verbose_name_plural': '酮体',
            },
        ),
        migrations.CreateModel(
            name='Type_of_residence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '居住类型',
                'verbose_name_plural': '居住类型',
            },
        ),
        migrations.CreateModel(
            name='Xin_yu_ping_ji',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '信誉评级',
                'verbose_name_plural': '信誉评级',
            },
        ),
        migrations.CreateModel(
            name='Ya_li_qing_kuang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '压力情况',
                'verbose_name_plural': '压力情况',
            },
        ),
        migrations.CreateModel(
            name='Yao_pin_dan_wei',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '药品计量单位',
                'verbose_name_plural': '药品计量单位',
            },
        ),
        migrations.CreateModel(
            name='Yao_pin_fen_lei',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '药品分类',
                'verbose_name_plural': '药品分类',
            },
        ),
        migrations.CreateModel(
            name='Yong_yao_tu_jing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='值')),
                ('icpc', models.CharField(blank=True, max_length=5, null=True, verbose_name='ICPC编码')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '用药途径',
                'verbose_name_plural': '用药途径',
            },
        ),
    ]
