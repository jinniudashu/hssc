# Generated by Django 3.2.6 on 2023-09-09 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Icpc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=5, null=True, unique=True, verbose_name='icpc码')),
                ('icode', models.CharField(blank=True, max_length=3, null=True, verbose_name='分类码')),
                ('iname', models.CharField(blank=True, max_length=255, null=True, verbose_name='名称')),
                ('iename', models.CharField(blank=True, max_length=255, null=True, verbose_name='English Name')),
                ('include', models.CharField(blank=True, max_length=1024, null=True, verbose_name='包含')),
                ('criteria', models.CharField(blank=True, max_length=1024, null=True, verbose_name='准则')),
                ('exclude', models.CharField(blank=True, max_length=1024, null=True, verbose_name='排除')),
                ('consider', models.CharField(blank=True, max_length=1024, null=True, verbose_name='考虑')),
                ('icd10', models.CharField(blank=True, max_length=8, null=True, verbose_name='ICD10')),
                ('icpc2', models.CharField(blank=True, max_length=10, null=True, verbose_name='ICPC2')),
                ('note', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('subclass', models.CharField(blank=True, max_length=255, null=True, verbose_name='ICPC子类')),
            ],
            options={
                'verbose_name': 'ICPC总表',
                'verbose_name_plural': 'ICPC总表',
            },
        ),
        migrations.CreateModel(
            name='Icpc10_test_results_and_statistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=5, null=True, unique=True, verbose_name='icpc码')),
                ('icode', models.CharField(blank=True, max_length=3, null=True, verbose_name='分类码')),
                ('iname', models.CharField(blank=True, max_length=255, null=True, verbose_name='名称')),
                ('iename', models.CharField(blank=True, max_length=255, null=True, verbose_name='English Name')),
                ('include', models.CharField(blank=True, max_length=1024, null=True, verbose_name='包含')),
                ('criteria', models.CharField(blank=True, max_length=1024, null=True, verbose_name='准则')),
                ('exclude', models.CharField(blank=True, max_length=1024, null=True, verbose_name='排除')),
                ('consider', models.CharField(blank=True, max_length=1024, null=True, verbose_name='考虑')),
                ('icd10', models.CharField(blank=True, max_length=8, null=True, verbose_name='ICD10')),
                ('icpc2', models.CharField(blank=True, max_length=10, null=True, verbose_name='ICPC2')),
                ('note', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '检查结果和统计',
                'verbose_name_plural': '检查结果和统计',
            },
        ),
        migrations.CreateModel(
            name='Icpc1_register_logins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=5, null=True, unique=True, verbose_name='icpc码')),
                ('icode', models.CharField(blank=True, max_length=3, null=True, verbose_name='分类码')),
                ('iname', models.CharField(blank=True, max_length=255, null=True, verbose_name='名称')),
                ('iename', models.CharField(blank=True, max_length=255, null=True, verbose_name='English Name')),
                ('include', models.CharField(blank=True, max_length=1024, null=True, verbose_name='包含')),
                ('criteria', models.CharField(blank=True, max_length=1024, null=True, verbose_name='准则')),
                ('exclude', models.CharField(blank=True, max_length=1024, null=True, verbose_name='排除')),
                ('consider', models.CharField(blank=True, max_length=1024, null=True, verbose_name='考虑')),
                ('icd10', models.CharField(blank=True, max_length=8, null=True, verbose_name='ICD10')),
                ('icpc2', models.CharField(blank=True, max_length=10, null=True, verbose_name='ICPC2')),
                ('note', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '注册登录（行政管理）',
                'verbose_name_plural': '注册登录（行政管理）',
            },
        ),
        migrations.CreateModel(
            name='Icpc2_reservation_investigations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=5, null=True, unique=True, verbose_name='icpc码')),
                ('icode', models.CharField(blank=True, max_length=3, null=True, verbose_name='分类码')),
                ('iname', models.CharField(blank=True, max_length=255, null=True, verbose_name='名称')),
                ('iename', models.CharField(blank=True, max_length=255, null=True, verbose_name='English Name')),
                ('include', models.CharField(blank=True, max_length=1024, null=True, verbose_name='包含')),
                ('criteria', models.CharField(blank=True, max_length=1024, null=True, verbose_name='准则')),
                ('exclude', models.CharField(blank=True, max_length=1024, null=True, verbose_name='排除')),
                ('consider', models.CharField(blank=True, max_length=1024, null=True, verbose_name='考虑')),
                ('icd10', models.CharField(blank=True, max_length=8, null=True, verbose_name='ICD10')),
                ('icpc2', models.CharField(blank=True, max_length=10, null=True, verbose_name='ICPC2')),
                ('note', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '预约咨询调查（行政管理）',
                'verbose_name_plural': '预约咨询调查（行政管理）',
            },
        ),
        migrations.CreateModel(
            name='Icpc3_symptoms_and_problems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=5, null=True, unique=True, verbose_name='icpc码')),
                ('icode', models.CharField(blank=True, max_length=3, null=True, verbose_name='分类码')),
                ('iname', models.CharField(blank=True, max_length=255, null=True, verbose_name='名称')),
                ('iename', models.CharField(blank=True, max_length=255, null=True, verbose_name='English Name')),
                ('include', models.CharField(blank=True, max_length=1024, null=True, verbose_name='包含')),
                ('criteria', models.CharField(blank=True, max_length=1024, null=True, verbose_name='准则')),
                ('exclude', models.CharField(blank=True, max_length=1024, null=True, verbose_name='排除')),
                ('consider', models.CharField(blank=True, max_length=1024, null=True, verbose_name='考虑')),
                ('icd10', models.CharField(blank=True, max_length=8, null=True, verbose_name='ICD10')),
                ('icpc2', models.CharField(blank=True, max_length=10, null=True, verbose_name='ICPC2')),
                ('note', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '症状和问题',
                'verbose_name_plural': '症状和问题',
            },
        ),
        migrations.CreateModel(
            name='Icpc4_physical_examination_and_tests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=5, null=True, unique=True, verbose_name='icpc码')),
                ('icode', models.CharField(blank=True, max_length=3, null=True, verbose_name='分类码')),
                ('iname', models.CharField(blank=True, max_length=255, null=True, verbose_name='名称')),
                ('iename', models.CharField(blank=True, max_length=255, null=True, verbose_name='English Name')),
                ('include', models.CharField(blank=True, max_length=1024, null=True, verbose_name='包含')),
                ('criteria', models.CharField(blank=True, max_length=1024, null=True, verbose_name='准则')),
                ('exclude', models.CharField(blank=True, max_length=1024, null=True, verbose_name='排除')),
                ('consider', models.CharField(blank=True, max_length=1024, null=True, verbose_name='考虑')),
                ('icd10', models.CharField(blank=True, max_length=8, null=True, verbose_name='ICD10')),
                ('icpc2', models.CharField(blank=True, max_length=10, null=True, verbose_name='ICPC2')),
                ('note', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '体格和其他检查',
                'verbose_name_plural': '体格和其他检查',
            },
        ),
        migrations.CreateModel(
            name='Icpc5_evaluation_and_diagnoses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=5, null=True, unique=True, verbose_name='icpc码')),
                ('icode', models.CharField(blank=True, max_length=3, null=True, verbose_name='分类码')),
                ('iname', models.CharField(blank=True, max_length=255, null=True, verbose_name='名称')),
                ('iename', models.CharField(blank=True, max_length=255, null=True, verbose_name='English Name')),
                ('include', models.CharField(blank=True, max_length=1024, null=True, verbose_name='包含')),
                ('criteria', models.CharField(blank=True, max_length=1024, null=True, verbose_name='准则')),
                ('exclude', models.CharField(blank=True, max_length=1024, null=True, verbose_name='排除')),
                ('consider', models.CharField(blank=True, max_length=1024, null=True, verbose_name='考虑')),
                ('icd10', models.CharField(blank=True, max_length=8, null=True, verbose_name='ICD10')),
                ('icpc2', models.CharField(blank=True, max_length=10, null=True, verbose_name='ICPC2')),
                ('note', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '评估和诊断',
                'verbose_name_plural': '评估和诊断',
            },
        ),
        migrations.CreateModel(
            name='Icpc6_prescribe_medicines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=5, null=True, unique=True, verbose_name='icpc码')),
                ('icode', models.CharField(blank=True, max_length=3, null=True, verbose_name='分类码')),
                ('iname', models.CharField(blank=True, max_length=255, null=True, verbose_name='名称')),
                ('iename', models.CharField(blank=True, max_length=255, null=True, verbose_name='English Name')),
                ('include', models.CharField(blank=True, max_length=1024, null=True, verbose_name='包含')),
                ('criteria', models.CharField(blank=True, max_length=1024, null=True, verbose_name='准则')),
                ('exclude', models.CharField(blank=True, max_length=1024, null=True, verbose_name='排除')),
                ('consider', models.CharField(blank=True, max_length=1024, null=True, verbose_name='考虑')),
                ('icd10', models.CharField(blank=True, max_length=8, null=True, verbose_name='ICD10')),
                ('icpc2', models.CharField(blank=True, max_length=10, null=True, verbose_name='ICPC2')),
                ('note', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '开药',
                'verbose_name_plural': '开药',
            },
        ),
        migrations.CreateModel(
            name='Icpc7_treatments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=5, null=True, unique=True, verbose_name='icpc码')),
                ('icode', models.CharField(blank=True, max_length=3, null=True, verbose_name='分类码')),
                ('iname', models.CharField(blank=True, max_length=255, null=True, verbose_name='名称')),
                ('iename', models.CharField(blank=True, max_length=255, null=True, verbose_name='English Name')),
                ('include', models.CharField(blank=True, max_length=1024, null=True, verbose_name='包含')),
                ('criteria', models.CharField(blank=True, max_length=1024, null=True, verbose_name='准则')),
                ('exclude', models.CharField(blank=True, max_length=1024, null=True, verbose_name='排除')),
                ('consider', models.CharField(blank=True, max_length=1024, null=True, verbose_name='考虑')),
                ('icd10', models.CharField(blank=True, max_length=8, null=True, verbose_name='ICD10')),
                ('icpc2', models.CharField(blank=True, max_length=10, null=True, verbose_name='ICPC2')),
                ('note', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '治疗',
                'verbose_name_plural': '治疗',
            },
        ),
        migrations.CreateModel(
            name='Icpc8_other_health_interventions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=5, null=True, unique=True, verbose_name='icpc码')),
                ('icode', models.CharField(blank=True, max_length=3, null=True, verbose_name='分类码')),
                ('iname', models.CharField(blank=True, max_length=255, null=True, verbose_name='名称')),
                ('iename', models.CharField(blank=True, max_length=255, null=True, verbose_name='English Name')),
                ('include', models.CharField(blank=True, max_length=1024, null=True, verbose_name='包含')),
                ('criteria', models.CharField(blank=True, max_length=1024, null=True, verbose_name='准则')),
                ('exclude', models.CharField(blank=True, max_length=1024, null=True, verbose_name='排除')),
                ('consider', models.CharField(blank=True, max_length=1024, null=True, verbose_name='考虑')),
                ('icd10', models.CharField(blank=True, max_length=8, null=True, verbose_name='ICD10')),
                ('icpc2', models.CharField(blank=True, max_length=10, null=True, verbose_name='ICPC2')),
                ('note', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '其他健康干预',
                'verbose_name_plural': '其他健康干预',
            },
        ),
        migrations.CreateModel(
            name='Icpc9_referral_consultations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=5, null=True, unique=True, verbose_name='icpc码')),
                ('icode', models.CharField(blank=True, max_length=3, null=True, verbose_name='分类码')),
                ('iname', models.CharField(blank=True, max_length=255, null=True, verbose_name='名称')),
                ('iename', models.CharField(blank=True, max_length=255, null=True, verbose_name='English Name')),
                ('include', models.CharField(blank=True, max_length=1024, null=True, verbose_name='包含')),
                ('criteria', models.CharField(blank=True, max_length=1024, null=True, verbose_name='准则')),
                ('exclude', models.CharField(blank=True, max_length=1024, null=True, verbose_name='排除')),
                ('consider', models.CharField(blank=True, max_length=1024, null=True, verbose_name='考虑')),
                ('icd10', models.CharField(blank=True, max_length=8, null=True, verbose_name='ICD10')),
                ('icpc2', models.CharField(blank=True, max_length=10, null=True, verbose_name='ICPC2')),
                ('note', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
            ],
            options={
                'verbose_name': '转诊会诊',
                'verbose_name_plural': '转诊会诊',
            },
        ),
    ]
