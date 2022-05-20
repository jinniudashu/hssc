# Generated by Django 3.2.6 on 2022-05-20 23:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import rest_framework.utils.encoders


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('icpc', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuessinessForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('description', models.TextField(blank=True, max_length=255, null=True, verbose_name='表单说明')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='icpc.icpc', verbose_name='ICPC编码')),
            ],
            options={
                'verbose_name': '业务表单',
                'verbose_name_plural': '业务表单',
            },
        ),
        migrations.CreateModel(
            name='BuessinessFormsSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('is_list', models.BooleanField(default=False, verbose_name='列表样式')),
                ('buessiness_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.buessinessform', verbose_name='表单')),
            ],
            options={
                'verbose_name': '作业表单设置',
                'verbose_name_plural': '作业表单设置',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ContractService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('is_active', models.BooleanField(default=True, verbose_name='启用')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='删除')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '合约服务',
                'verbose_name_plural': '合约服务',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ContractServiceProc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('priority', models.PositiveSmallIntegerField(choices=[(0, '0级'), (1, '紧急'), (2, '优先'), (3, '一般')], default=3, verbose_name='优先级')),
                ('contract_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.contractservice', verbose_name='合约服务')),
            ],
            options={
                'verbose_name': '合约服务进程',
                'verbose_name_plural': '合约服务进程',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('name', models.CharField(max_length=50, verbose_name='姓名')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='电话')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='地址')),
                ('health_record', models.JSONField(blank=True, null=True, verbose_name='健康记录')),
                ('charge_staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.customer', verbose_name='负责人')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='客户')),
            ],
            options={
                'verbose_name': '客户注册信息',
                'verbose_name_plural': '客户注册信息',
            },
        ),
        migrations.CreateModel(
            name='EventRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('description', models.TextField(blank=True, max_length=255, null=True, verbose_name='表达式')),
                ('detection_scope', models.CharField(blank=True, choices=[('ALL', '所有历史表单'), ('CURRENT_SERVICE', '本次服务表单'), ('LAST_WEEK_SERVICES', '过去7天表单')], default='CURRENT_SERVICE', max_length=100, null=True, verbose_name='检测范围')),
                ('weight', models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='权重')),
                ('expression', models.TextField(blank=True, max_length=1024, null=True, verbose_name='内部表达式')),
                ('expression_fields', models.CharField(blank=True, max_length=1024, null=True, verbose_name='内部表达式字段')),
            ],
            options={
                'verbose_name': '条件事件',
                'verbose_name_plural': '条件事件',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ManagedEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('app_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='所属app名')),
                ('model_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='模型名')),
                ('base_form', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.buessinessform', verbose_name='基础表单')),
            ],
            options={
                'verbose_name': '业务管理实体',
                'verbose_name_plural': '业务管理实体',
            },
        ),
        migrations.CreateModel(
            name='OperationProc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('state', models.PositiveSmallIntegerField(choices=[(0, '创建'), (1, '就绪'), (2, '运行'), (3, '挂起'), (4, '结束')], verbose_name='作业状态')),
                ('priority', models.PositiveSmallIntegerField(choices=[(0, '0级'), (1, '紧急'), (2, '优先'), (3, '一般')], default=3, verbose_name='优先级')),
                ('entry', models.CharField(blank=True, db_index=True, max_length=250, null=True, verbose_name='作业入口')),
                ('form_slugs', models.JSONField(blank=True, null=True, verbose_name='表单索引')),
                ('scheduled_time', models.DateTimeField(blank=True, null=True, verbose_name='计划执行时间')),
                ('created_time', models.DateTimeField(editable=False, null=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(editable=False, null=True, verbose_name='修改时间')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('content_type', models.ForeignKey(blank=True, limit_choices_to=models.Q(('app_label', 'service')), null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('contract_service_proc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.contractserviceproc', verbose_name='服务进程')),
                ('creater', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='operation_proc_creater', to='core.customer', verbose_name='创建者')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='operation_proc_customer', to='core.customer', verbose_name='客户')),
                ('operator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='operation_proc_operator', to='core.customer', verbose_name='操作员')),
                ('parent_proc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.operationproc', verbose_name='父进程')),
            ],
            options={
                'verbose_name': '作业进程',
                'verbose_name_plural': '作业进程',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='岗位描述')),
            ],
            options={
                'verbose_name': '业务岗位',
                'verbose_name_plural': '业务岗位',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('priority', models.PositiveSmallIntegerField(choices=[(0, '0级'), (1, '紧急'), (2, '优先'), (3, '一般')], default=3, verbose_name='优先级')),
                ('is_system_service', models.BooleanField(default=False, verbose_name='系统内置服务')),
                ('history_services_display', models.PositiveBigIntegerField(blank=True, choices=[(0, '所有历史服务'), (1, '当日服务')], default=0, null=True, verbose_name='历史服务默认显示')),
                ('enable_queue_counter', models.BooleanField(default=True, verbose_name='显示队列数量')),
                ('route_to', models.CharField(blank=True, choices=[('INDEX', '任务工作台'), ('CUSTOMER_HOMEPAGE', '客户病例首页')], default='CUSTOMER_HOMEPAGE', max_length=50, null=True, verbose_name='完成跳转至')),
                ('suppliers', models.CharField(blank=True, max_length=255, null=True, verbose_name='供应商')),
                ('not_suitable', models.CharField(blank=True, max_length=255, null=True, verbose_name='不适用对象')),
                ('execution_time_frame', models.DurationField(blank=True, null=True, verbose_name='完成时限')),
                ('awaiting_time_frame', models.DurationField(blank=True, null=True, verbose_name='等待执行时限')),
                ('working_hours', models.DurationField(blank=True, null=True, verbose_name='工时')),
                ('frequency', models.CharField(blank=True, max_length=255, null=True, verbose_name='频次')),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='成本')),
                ('load_feedback', models.BooleanField(default=False, verbose_name='是否反馈负荷数量')),
                ('resource_materials', models.CharField(blank=True, max_length=255, null=True, verbose_name='配套物料')),
                ('resource_devices', models.CharField(blank=True, max_length=255, null=True, verbose_name='配套设备')),
                ('resource_knowledge', models.CharField(blank=True, max_length=255, null=True, verbose_name='服务知识')),
                ('buessiness_forms', models.ManyToManyField(through='core.BuessinessFormsSetting', to='core.BuessinessForm', verbose_name='作业表单')),
                ('managed_entity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.managedentity', verbose_name='管理实体')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='icpc.icpc', verbose_name='ICPC编码')),
                ('role', models.ManyToManyField(blank=True, to='core.Role', verbose_name='服务岗位')),
            ],
            options={
                'verbose_name': '服务',
                'verbose_name_plural': '服务',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ServicePackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('begin_time_setting', models.PositiveSmallIntegerField(choices=[(0, '人工指定'), (1, '出生日期')], default=0, verbose_name='开始时间参考')),
                ('duration', models.DurationField(blank=True, help_text='例如：3 days, 22:00:00', null=True, verbose_name='持续周期')),
                ('execution_time_frame', models.DurationField(blank=True, null=True, verbose_name='执行时限')),
                ('awaiting_time_frame', models.DurationField(blank=True, null=True, verbose_name='等待执行时限')),
                ('name_icpc', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='icpc.icpc', verbose_name='ICPC编码')),
            ],
            options={
                'verbose_name': '服务包',
                'verbose_name_plural': '服务包',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ServiceSpec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
            ],
            options={
                'verbose_name': '服务规格',
                'verbose_name_plural': '服务规格',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('email', models.EmailField(max_length=50)),
                ('title', models.PositiveSmallIntegerField(blank=True, choices=[('主任医师', '主任医师'), ('副主任医师', '副主任医师'), ('主治医师', '主治医师'), ('住院医师', '住院医师'), ('主任护师', '主任护师'), ('副主任护师', '副主任护师'), ('主管护师', '主管护师'), ('护士长', '护士长'), ('护士', '护士'), ('其他', '其他')], null=True, verbose_name='职称')),
                ('is_assistant_physician', models.BooleanField(blank=True, null=True, verbose_name='助理医师')),
                ('resume', models.TextField(blank=True, null=True, verbose_name='简历')),
                ('service_lever', models.PositiveSmallIntegerField(blank=True, choices=[('低', '低'), ('中', '中'), ('高', '高')], null=True, verbose_name='服务级别')),
                ('registration_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='挂号费')),
                ('standardized_workload', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='标化工作量')),
                ('customer', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.customer', verbose_name='员工')),
                ('role', models.ManyToManyField(related_name='staff_role', to='core.Role', verbose_name='角色')),
            ],
            options={
                'verbose_name': '员工基本信息',
                'verbose_name_plural': '员工基本信息',
            },
        ),
        migrations.CreateModel(
            name='SystemOperand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('func', models.CharField(blank=True, max_length=255, null=True, verbose_name='内部实现函数')),
                ('parameters', models.CharField(blank=True, max_length=255, null=True, verbose_name='参数')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='描述')),
                ('applicable', models.PositiveSmallIntegerField(choices=[(0, '作业'), (1, '单元服务'), (2, '服务包'), (3, '全部')], default=1, verbose_name='适用范围')),
            ],
            options={
                'verbose_name': '系统自动作业',
                'verbose_name_plural': '系统自动作业',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Workgroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('leader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workgroup_customer', to='core.staff', verbose_name='组长')),
                ('members', models.ManyToManyField(blank=True, related_name='workgroup_members', to='core.Staff', verbose_name='组员')),
            ],
            options={
                'verbose_name': '服务小组',
                'verbose_name_plural': '服务小组',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='StaffTodo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('scheduled_time', models.DateTimeField(blank=True, null=True, verbose_name='计划执行时间')),
                ('state', models.PositiveSmallIntegerField(choices=[(0, '创建'), (1, '就绪'), (2, '运行'), (3, '挂起'), (4, '结束')], verbose_name='作业状态')),
                ('customer_number', models.CharField(blank=True, max_length=250, null=True, verbose_name='居民档案号')),
                ('customer_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='姓名')),
                ('service_label', models.CharField(blank=True, max_length=250, null=True, verbose_name='服务项目')),
                ('customer_phone', models.CharField(blank=True, max_length=250, null=True, verbose_name='联系电话')),
                ('customer_address', models.CharField(blank=True, max_length=250, null=True, verbose_name='家庭地址')),
                ('priority', models.PositiveSmallIntegerField(choices=[(0, '0级'), (1, '紧急'), (2, '优先'), (3, '一般')], default=3, verbose_name='优先级')),
                ('operation_proc', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.operationproc', verbose_name='作业进程')),
                ('operator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.customer', verbose_name='操作员')),
            ],
            options={
                'verbose_name': '员工任务清单',
                'verbose_name_plural': '员工任务清单',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ServiceRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('passing_data', models.PositiveSmallIntegerField(blank=True, choices=[(0, '否'), (1, '接收，不可编辑'), (2, '接收，可以编辑')], default=0, null=True, verbose_name='接收表单')),
                ('complete_feedback', models.PositiveSmallIntegerField(blank=True, choices=[(0, '否'), (1, '返回完成状态'), (2, '返回表单')], default=0, null=True, verbose_name='完成反馈')),
                ('reminders', models.PositiveSmallIntegerField(blank=True, choices=[(0, '客户'), (1, '服务人员'), (2, '服务小组')], default=0, null=True, verbose_name='提醒对象')),
                ('message', models.CharField(blank=True, max_length=512, null=True, verbose_name='消息内容')),
                ('interval_rule', models.PositiveSmallIntegerField(blank=True, choices=[(0, '等于'), (1, '小于'), (2, '大于')], null=True, verbose_name='间隔条件')),
                ('interval_time', models.DurationField(blank=True, help_text='例如：3 days, 22:00:00', null=True, verbose_name='间隔时间')),
                ('is_active', models.BooleanField(choices=[(False, '否'), (True, '是')], default=True, verbose_name='启用')),
                ('event_rule', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.eventrule', verbose_name='条件事件')),
                ('next_service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_service', to='core.service', verbose_name='后续服务')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.service', verbose_name='服务项目')),
                ('service_spec', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.servicespec', verbose_name='服务规格')),
                ('system_operand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.systemoperand', verbose_name='系统作业')),
            ],
            options={
                'verbose_name': '服务规则',
                'verbose_name_plural': '服务规则',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ServicePackageDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('cycle_option', models.PositiveSmallIntegerField(blank=True, choices=[(0, '总共'), (1, '每天'), (2, '每周'), (3, '每月'), (4, '每季'), (5, '每年')], default=0, null=True, verbose_name='周期')),
                ('cycle_times', models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='次数')),
                ('reference_start_tim', models.DurationField(blank=True, help_text='例如：3 days, 22:00:00', null=True, verbose_name='参考起始时间')),
                ('duration', models.DurationField(blank=True, help_text='例如：3 days, 22:00:00', null=True, verbose_name='持续周期')),
                ('check_awaiting_timeout', models.BooleanField(default=False, verbose_name='检查等待超时')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.service', verbose_name='服务项目')),
                ('servicepackage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.servicepackage', verbose_name='服务包')),
            ],
            options={
                'verbose_name': '服务内容模板',
                'verbose_name_plural': '服务内容模板',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='servicepackage',
            name='services',
            field=models.ManyToManyField(through='core.ServicePackageDetail', to='core.Service', verbose_name='服务项目'),
        ),
        migrations.CreateModel(
            name='RecommendedService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, verbose_name='slug')),
                ('created_time', models.DateTimeField(editable=False, null=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(editable=False, null=True, verbose_name='更新时间')),
                ('cpid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.contractserviceproc', verbose_name='服务进程id')),
                ('creater', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recommended_service_creater', to='core.customer', verbose_name='创建者')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recommended_service_customer', to='core.customer', verbose_name='客户')),
                ('operator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recommended_service_operator', to='core.customer', verbose_name='操作员')),
                ('pid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.operationproc', verbose_name='作业进程id')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.service', verbose_name='推荐服务')),
            ],
            options={
                'verbose_name': '推荐服务',
                'verbose_name_plural': '推荐服务',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='operationproc',
            name='role',
            field=models.ManyToManyField(blank=True, to='core.Role', verbose_name='作业岗位'),
        ),
        migrations.AddField(
            model_name='operationproc',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.service', verbose_name='服务'),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, verbose_name='slug')),
                ('created_time', models.DateTimeField(editable=False, null=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(editable=False, null=True, verbose_name='更新时间')),
                ('message', models.CharField(blank=True, max_length=512, null=True, verbose_name='消息')),
                ('has_read', models.BooleanField(default=False, verbose_name='是否已读')),
                ('cpid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.contractserviceproc', verbose_name='服务进程id')),
                ('creater', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_creater', to='core.customer', verbose_name='创建者')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_customer', to='core.customer', verbose_name='客户')),
                ('operator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_operator', to='core.customer', verbose_name='操作员')),
                ('pid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.operationproc', verbose_name='作业进程id')),
            ],
            options={
                'verbose_name': '消息',
                'verbose_name_plural': '消息',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='HsscBaseFormModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, verbose_name='slug')),
                ('created_time', models.DateTimeField(editable=False, null=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(editable=False, null=True, verbose_name='更新时间')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('cpid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hsscbaseformmodel_sid', to='core.contractserviceproc', verbose_name='服务进程id')),
                ('creater', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hsscbaseformmodel_creater', to='core.customer', verbose_name='创建者')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hsscbaseformmodel_customer', to='core.customer', verbose_name='客户')),
                ('operator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hsscbaseformmodel_operator', to='core.customer', verbose_name='操作员')),
                ('pid', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hsscbaseformmodel_pid', to='core.operationproc', verbose_name='作业进程id')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerServiceLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, verbose_name='slug')),
                ('created_time', models.DateTimeField(editable=False, null=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(editable=False, null=True, verbose_name='更新时间')),
                ('category', models.CharField(blank=True, choices=[('Subjective', '主观资料'), ('ObjectiveO', '客观资料'), ('Assessment', '诊断与评价'), ('Plan', '治疗方案'), ('Management', '管理活动')], max_length=50, null=True, verbose_name='记录类别')),
                ('data', models.JSONField(blank=True, encoder=rest_framework.utils.encoders.JSONEncoder, null=True, verbose_name='服务记录')),
                ('cpid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.contractserviceproc', verbose_name='服务进程id')),
                ('creater', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_service_log_creater', to='core.customer', verbose_name='创建者')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_service_log_customer', to='core.customer', verbose_name='客户')),
                ('operator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_service_log_operator', to='core.customer', verbose_name='操作员')),
                ('pid', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.operationproc', verbose_name='作业进程id')),
            ],
            options={
                'verbose_name': '客户服务记录',
                'verbose_name_plural': '客户服务记录',
                'ordering': ['created_time'],
            },
            managers=[
                ('logs', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='workgroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_workgroup', to='core.workgroup', verbose_name='服务小组'),
        ),
        migrations.AddField(
            model_name='contractserviceproc',
            name='creater',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_proc_creater', to='core.customer', verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='contractserviceproc',
            name='current_service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.service', verbose_name='作业状态'),
        ),
        migrations.AddField(
            model_name='contractserviceproc',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_proc_customer', to='core.customer', verbose_name='客户'),
        ),
        migrations.AddField(
            model_name='buessinessformssetting',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.service', verbose_name='作业'),
        ),
    ]
