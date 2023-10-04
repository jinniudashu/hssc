from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from time import time
from enum import Enum

from rest_framework.utils.encoders import JSONEncoder
from pypinyin import lazy_pinyin

from icpc.models import *
from core.hsscbase_class import HsscBase, HsscPymBase


# **********************************************************************************************************************
# Service配置 Model
# **********************************************************************************************************************
# 角色表
class Role(HsscPymBase):
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="岗位描述")

    class Meta:
        verbose_name = "业务岗位"
        verbose_name_plural = verbose_name
        ordering = ['id']


# 业务表单定义
class BuessinessForm(HsscPymBase):
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    description = models.TextField(max_length=255, null=True, blank=True, verbose_name="表单说明")
    Form_class = [(1, '调查类'), (2, '诊断类'), (3, '治疗类')]
    form_class = models.PositiveSmallIntegerField(choices=Form_class, null=True, verbose_name="表单类型")
    api_fields = models.JSONField(null=True, blank=True, verbose_name="API字段")
    
    class Meta:
        verbose_name = '业务表单'
        verbose_name_plural = verbose_name


# 管理实体定义
class ManagedEntity(HsscPymBase):
    app_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="所属app名")
    model_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="模型名")
    base_form = models.OneToOneField(BuessinessForm, on_delete=models.SET_NULL, null=True, verbose_name="基础表单")
    header_fields_json = models.JSONField(null=True, blank=True, verbose_name="表头字段json")

    class Meta:
        verbose_name = "业务管理实体"
        verbose_name_plural = verbose_name


# 作业基础信息表
class Service(HsscPymBase):
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    buessiness_forms = models.ManyToManyField(BuessinessForm, through='BuessinessFormsSetting', verbose_name="作业表单")
    managed_entity = models.ForeignKey(ManagedEntity, on_delete=models.CASCADE, null=True, verbose_name="管理实体")
    Operation_priority = [(0, '0级'), (1, '紧急'), (2, '优先'), (3, '一般')]
    priority = models.PositiveSmallIntegerField(choices=Operation_priority, default=3, verbose_name='优先级')
    Service_type = [(0, '系统服务'), (1, '管理调度服务'), (2, '诊疗服务')]
    service_type = models.PositiveSmallIntegerField(choices=Service_type, default=2, verbose_name='服务类型')
    role = models.ManyToManyField(Role, blank=True, verbose_name="服务岗位")
    History_services_display=[(0, '所有历史服务'), (1, '当日服务')]
    history_services_display = models.PositiveBigIntegerField(choices=History_services_display, default=0, blank=True, null=True, verbose_name='历史服务默认显示')
    enable_queue_counter = models.BooleanField(default=True, verbose_name='显示队列数量')
    Route_to = [('INDEX', '任务工作台'), ('CUSTOMER_HOMEPAGE', '客户病例首页')]
    route_to = models.CharField(max_length=50, choices=Route_to, default='CUSTOMER_HOMEPAGE', blank=True, null=True, verbose_name='完成跳转至')
    follow_up_required = models.BooleanField(default=False, verbose_name='需要随访')
    follow_up_interval = models.DurationField(blank=True, null=True, verbose_name='随访间隔')
    follow_up_service = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='follow_up_services', verbose_name='随访服务')
    suppliers = models.CharField(max_length=255, blank=True, null=True, verbose_name="供应商")
    not_suitable = models.CharField(max_length=255, blank=True, null=True, verbose_name='不适用对象')
    overtime = models.DurationField(blank=True, null=True, verbose_name='超期时限')
    working_hours = models.DurationField(blank=True, null=True, verbose_name='工时')
    frequency = models.CharField(max_length=255, blank=True, null=True, verbose_name='频次')
    cost = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2, verbose_name='成本')
    load_feedback = models.BooleanField(default=False, verbose_name='是否反馈负荷数量')
    resource_materials = models.CharField(max_length=255, blank=True, null=True, verbose_name='配套物料')
    resource_devices = models.CharField(max_length=255, blank=True, null=True, verbose_name='配套设备')
    resource_knowledge = models.CharField(max_length=255, blank=True, null=True, verbose_name='服务知识')
    arrange_service_package = models.OneToOneField('ServicePackage', blank=True, null=True, on_delete=models.CASCADE, verbose_name='安排服务包')    
    arrange_service = models.OneToOneField('self', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='安排服务')    

    class Meta:
        verbose_name = "服务作业"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if self.name_icpc is not None:
            self.name = self.name_icpc.icpc_code
            self.label = self.name_icpc.iname
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)
    

class BuessinessFormsSetting(HsscBase):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="作业")
    buessiness_form = models.ForeignKey(BuessinessForm, on_delete=models.CASCADE, verbose_name="表单")
    is_list = models.BooleanField(default=False, verbose_name="列表样式")

    class Meta:
        verbose_name = '作业表单设置'
        verbose_name_plural = verbose_name
        ordering = ['id']


# 基础作业信息表
class L1Service(HsscPymBase):
    start_service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True, related_name='start_service', verbose_name='起始作业')
    end_service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True, related_name='end_service', verbose_name='结束作业')
    include_services = models.ManyToManyField(Service, blank=True, related_name='include_services', verbose_name='包含作业')
    role = models.ManyToManyField(Role, blank=True, verbose_name="服务岗位")

    class Meta:
        verbose_name = "服务任务"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.name is None or self.name == '':
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)


# 服务包类型信息表
class ServicePackage(HsscPymBase):
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")

    class Meta:
        verbose_name = "服务包"
        verbose_name_plural = verbose_name
        ordering = ['id']

class CycleUnit(HsscPymBase):
    cycle_unit = models.CharField(max_length=255, blank=True, null=True, verbose_name='周期单位')
    days = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='天数')
    class Meta:
        verbose_name = "服务周期单位"
        verbose_name_plural = verbose_name

class ServicePackageDetail(HsscPymBase):
    order = models.PositiveSmallIntegerField(default=100, verbose_name='顺序')
    servicepackage = models.ForeignKey(ServicePackage, on_delete=models.CASCADE, verbose_name='服务包')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    cycle_unit = models.ForeignKey(CycleUnit, on_delete=models.CASCADE, default=1, blank=True, null=True, verbose_name='周期单位')
    cycle_frequency = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="每周期频次")
    cycle_times = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="天数")
    Default_beginning_time = [(0, '指定开始时间'), (1, '当前系统时间'), (2, '首个服务开始时间'), (3, '上个服务结束时间'), (4, '客户出生日期')]
    default_beginning_time = models.PositiveSmallIntegerField(choices=Default_beginning_time, default=1, verbose_name='执行时间基准')
    base_interval = models.DurationField(blank=True, null=True, verbose_name='基准间隔', help_text='例如：3 days, 22:00:00')

    class Meta:
        verbose_name = "服务内容模板"
        verbose_name_plural = verbose_name
        ordering = ['order']

    def __str__(self):
        return str(self.service)


# 系统作业指令表
class SystemOperand(HsscBase):
    func = models.CharField(max_length=255, blank=True, null=True, verbose_name="内部实现函数")
    parameters = models.CharField(max_length=255, blank=True, null=True, verbose_name="参数")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="描述")
    Operand_type = [('SCHEDULE_OPERAND', '调度作业'), ('FORM_OPERAND', '表单作业')]
    operand_type = models.CharField(max_length=100, choices=Operand_type, default='SCHEDULE_OPERAND', verbose_name="系统作业类型")
    Applicable = [(0, '作业'), (1, '单元服务'), (2, '服务包'), (3, '全部')]
    applicable = models.PositiveSmallIntegerField(choices=Applicable, default=1, verbose_name='适用范围')

    class Meta:
        verbose_name = '系统自动作业'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.label


# 事件规则表
class EventRule(HsscBase):
    description = models.TextField(max_length=255, blank=True, null=True, verbose_name="表达式")
    Detection_scope = [('ALL', '所有历史表单'), ('CURRENT_SERVICE', '本次服务表单'), ('LAST_WEEK_SERVICES', '过去7天表单')]
    detection_scope = models.CharField(max_length=100, choices=Detection_scope, default='CURRENT_SERVICE', blank=True, null=True, verbose_name='检测范围')
    Form_class = [(0, '所有类型'), (1, '调查类'), (2, '诊断类'), (3, '治疗类')]
    form_class_scope = models.PositiveSmallIntegerField(choices=Form_class, default=0, verbose_name='表单类型范围')
    Event_type = [('FORM_EVENT', '表单事件'), ('SCHEDULE_EVENT', '调度事件')]
    event_type = models.CharField(max_length=100, choices=Event_type, default='SCHEDULE_EVENT', verbose_name="事件类型")
    weight = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="权重")
    expression = models.TextField(max_length=1024, blank=True, null=True, verbose_name="内部表达式")
    expression_fields = models.CharField(max_length=1024, blank=True, null=True, verbose_name="内部表达式字段")

    class Meta:
        verbose_name = '条件事件'
        verbose_name_plural = verbose_name
        ordering = ['id']


# 服务规则库
class ServiceRule(HsscBase):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    event_rule = models.ForeignKey(EventRule, on_delete=models.CASCADE,  blank=True, null=True, verbose_name='条件事件')
    system_operand = models.ForeignKey(SystemOperand, on_delete=models.CASCADE, blank=True, null=True, verbose_name='系统作业')
    next_service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True, related_name='next_service', verbose_name='后续服务')
    priority_operator = models.ForeignKey('VirtualStaff', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="优先操作员")    
    Receive_form = [(0, '否'), (1, '接收，不可编辑'), (2, '接收，可以编辑')]  # 接收表单数据
    passing_data = models.PositiveSmallIntegerField(choices=Receive_form, default=0,  blank=True, null=True, verbose_name='接收表单')
    apply_to_group = models.BooleanField(choices=[(False, '否'), (True, '是')], default=False, verbose_name='应用于分组')
    Complete_feedback = [(0, '否'), (1, '返回完成状态'), (2, '返回表单')]
    complete_feedback = models.PositiveSmallIntegerField(choices=Complete_feedback, default=0,  blank=True, null=True, verbose_name='完成反馈')
    Reminders = [(0, '客户'), (1, '服务人员'), (2, '服务小组')]
    reminders = models.PositiveSmallIntegerField(choices=Reminders, default=0,  blank=True, null=True, verbose_name='提醒对象')
    message = models.CharField(max_length=512, blank=True, null=True, verbose_name='消息内容')
    Interval_rule_options = [(0, '等于'), (1, '小于'), (2, '大于')]
    interval_rule = models.PositiveSmallIntegerField(choices=Interval_rule_options, blank=True, null=True, verbose_name='间隔条件')
    interval_time = models.DurationField(blank=True, null=True, verbose_name="间隔时间", help_text='例如：3 days, 22:00:00')
    is_active = models.BooleanField(choices=[(False, '否'), (True, '是')], default=True, verbose_name='启用')

    class Meta:
        verbose_name = '服务规则'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.service)


class ContractService(HsscPymBase):
    start_l1_service = models.ForeignKey(L1Service, on_delete=models.CASCADE, blank=True, null=True, related_name='start_l1_service', verbose_name='起始任务')
    end_l1_service = models.ForeignKey(L1Service, on_delete=models.CASCADE, blank=True, null=True, related_name='end_l1_service', verbose_name='结束任务')
    is_active = models.BooleanField(default=True, verbose_name='启用')
    is_deleted = models.BooleanField(default=False, verbose_name='删除')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '合约服务'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.label)


class ExternalServiceMapping(HsscBase):
    external_form_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="外部表单标识")
    external_form_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="外部表单名称")
    Form_source = [('jinshuju', '金数据'), ('other', '其它')]
    form_source = models.CharField(max_length=50, choices=Form_source, null=True, blank=True, verbose_name="来源名称")
    service = models.OneToOneField(Service, on_delete=models.CASCADE, null=True, blank=True, verbose_name="对应服务")
    fields_mapping = models.JSONField(null=True, blank=True, verbose_name="字段映射")

    class Meta:
        verbose_name = '外部服务映射'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.external_form_name)

# **********************************************************************************************************************
# Service进程管理Model
# **********************************************************************************************************************
Operation_priority = [(1, '紧急'), (2, '优先'), (3, '一般')]

# 服务进程表 ServiceProc
class ContractServiceProc(HsscBase):
    contract_service = models.ForeignKey(ContractService, on_delete=models.CASCADE, verbose_name="合约服务")
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")  # 客户id: cid
    state = models.ForeignKey(L1Service, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="当前任务")
    priority = models.PositiveSmallIntegerField(choices=Operation_priority, default=3, verbose_name="优先级")

    class Meta:
        verbose_name = "合约服务进程"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.customer.name


# 任务进程表
class TaskProc(HsscBase):
    label = models.CharField(max_length=255, blank=True, null=True, verbose_name="名称")
    l1_service = models.ForeignKey(L1Service, on_delete=models.CASCADE, null=True, verbose_name="任务")
    state = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name="服务")  # 作业id: oid
    operator = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='task_proc_operator', verbose_name="操作员")  # 作业员id: uid
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='task_proc_customer', verbose_name="客户")  # 客户id: cid
    parent_proc = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="父进程")  # 父作业进程id: ppid
    created_time = models.DateTimeField(editable=False, null=True, verbose_name="创建时间")
    completed_time = models.DateTimeField(editable=False, null=True, verbose_name="修改时间")
    priority = models.PositiveSmallIntegerField(choices=Operation_priority, default=3, verbose_name="优先级")

    class Meta:
        verbose_name = "任务进程"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
		# 任务进程名称=任务名称 + '_' + id
        return self.l1_service.label + '_' + str(self.id)


class OperationProcManager(models.Manager):
    def get_service_queue_count(self, service):
        return self.filter(service=service).exclude(state=4).count()

    def get_unassigned_proc(self, operator):
	# 获取待分配作业进程: 状态为创建，且未分配操作员，服务岗位为操作员所属岗位，以及用户服务小组为操作员所属服务小组
        return self.filter(state=0, operator=None, service__in=Service.objects.filter(role__in=operator.staff.role.all()),)

	# 员工当天常规任务
    def staff_todos_today(self, operator):
        today = timezone.now().date()
        return self.filter(
            operator=operator, 
            priority=3,
            scheduled_time__year=int(today.strftime('%Y')),
            scheduled_time__month=int(today.strftime('%m')),
            scheduled_time__day=int(today.strftime('%d')),
            ).exclude(state__in=[4, 5])
        
	# 员工紧要任务安排
    def staff_todos_urgent(self, operator):
        return self.filter(operator=operator, priority__lt=3).exclude(state__in=[4, 5]).order_by('priority')

	# 员工未来七天任务
    def staff_todos_week(self, operator):
        startTime = timezone.now() + timedelta(days=1)
        endTime = timezone.now() + timedelta(days=7)
        return self.filter(
            operator=operator, 
            priority=3, 
            scheduled_time__range=(startTime, endTime),
            ).exclude(state__in=[4, 5])

# 作业进程表 OperationProc
class OperationProc(HsscBase):
    task_proc = models.ForeignKey(TaskProc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="任务进程")
    label = models.CharField(max_length=255, blank=True, null=True, verbose_name="名称")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name="服务")  # 作业id: oid
    operator = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='operation_proc_operator', verbose_name="操作员")  # 作业员id: uid
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='operation_proc_customer', verbose_name="客户")  # 客户id: cid
    creater = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='operation_proc_creater', verbose_name="创建者")  # 创建者id: cid
    priority_operator = models.ForeignKey('VirtualStaff', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="优先操作员")    
    role = models.ManyToManyField(Role, blank=True, verbose_name="作业岗位")
	# 作业状态: state
    Operation_proc_state = [(0, '创建'), (1, '就绪'), (2, '运行'), (3, '挂起'), (4, '结束'), (5, '撤销'), (10, '等待超时')]
    state = models.PositiveSmallIntegerField(choices=Operation_proc_state, verbose_name="作业状态")
    priority = models.PositiveSmallIntegerField(choices=Operation_priority, default=3, verbose_name="优先级")
    entry = models.CharField(max_length=250, blank=True, null=True, db_index=True, verbose_name="作业入口")  # 作业入口: /clinic/service/model_name/model_id/change
    parent_proc = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="父进程")  # 父作业进程id: ppid
    contract_service_proc = models.ForeignKey(ContractServiceProc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="服务进程")  # 服务进程id: spid
    form_slugs = models.JSONField(blank=True, null=True, verbose_name="表单索引")
    scheduled_time = models.DateTimeField(blank=True, null=True, verbose_name="计划执行时间")
    overtime = models.DurationField(blank=True, null=True, verbose_name='超期时限')
    working_hours = models.DurationField(blank=True, null=True, verbose_name='工时')
    acceptance_timeout = models.BooleanField(default=False, blank=True, null=True, verbose_name="受理超时")
    completion_timeout = models.BooleanField(default=False, blank=True, null=True, verbose_name="完成超时")
    created_time = models.DateTimeField(editable=False, null=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(editable=False, null=True, verbose_name="修改时间")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=Q(app_label='service') , null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    objects = OperationProcManager()

    class Meta:
        verbose_name = "作业进程"
        verbose_name_plural = "作业进程"
        ordering = ['id']

    def __str__(self):
		# return 作业名称
        return self.service.label

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_time = timezone.now()
        self.modified_time = timezone.now()
        if not self.name:
            self.name = self.service.label
        if not self.label:
            self.label = self.name
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        # 返回作业入口url
        return self.entry
    
    def receive_task(self, operator):
        # 接收作业进程
        self.operator = operator
        self.state = 1
        self.save()

    def rollback_task(self):
        # 作业进程回退
        self.operator = None
        self.state = 0
        self.save()

    def cancel_task(self, operator):
        # 作业进程撤销
        self.operator = operator
        self.state = 5
        self.save()

    def suspend_or_resume_task(self):
        # 作业进程挂起或恢复
        if self.state == 3:
            self.state = 0
        else:
            self.state = 3
        self.save()

    def shift_task(self, operator):
        # 作业进程转移操作员
        self.operator = operator
        self.state = 1
        self.save()

    def set_operator(self, operator):
        # 设置作业进程操作员
        self.operator = operator
        self.save()

    def update_state(self, ocode):
        #作业进程状态机操作码ocode
        class OperationCode(Enum):
            CRE = 0  # CREATE
            CTR = 1  # CREATED TO READY
            RTR = 2  # READY TO RUNNING
            RTH = 3  # RUNNING TO HANGUP
            HTR = 1  # HANGUP TO READY
            RTC = 4  # RUNNING TO COMPLETED
        self.state = OperationCode[ocode].value
        self.save()


# 用户基本信息
class Customer(HsscBase):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='客户')
    name = models.CharField(max_length=50, verbose_name="姓名")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="电话")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="地址")
    charge_staff = models.ForeignKey('VirtualStaff', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='负责人')
    health_record = models.JSONField(blank=True, null=True, verbose_name="健康记录")
    weixin_openid = models.CharField(max_length=255, blank=True, null=True, verbose_name="微信openid")

    class Meta:
        verbose_name = "客户注册信息"
        verbose_name_plural = "客户注册信息"

    def __str__(self):
        return str(self.name)

    def natural_key(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.label:
            self.label = self.name
        super().save(*args, **kwargs)

    def get_history_services(self) -> 'QuerySet[OperationProc]':
        '''
        获取客户历史服务列表
        '''
        return self.operation_proc_customer.filter(state=4).exclude(service__in=Service.objects.filter(service_type=0))

    def get_scheduled_services(self, date) -> 'QuerySet[OperationProc]':
        '''
        获取已安排服务列表
        '''
        if date == 'TODAY':
            return self.operation_proc_customer.filter(scheduled_time__date=timezone.now().date(), state__in = [0, 1, 2, 3])
        elif date == 'RECENT':  # 今天以后的服务
            return self.operation_proc_customer.filter(scheduled_time__date__gt=timezone.now().date(), state__in = [0, 1, 3])
        else:
            return self.operation_proc_customer.filter(state__in = [0, 1, 2, 3])

    def get_absolute_url(self):
        return reverse('customer_homepage', args=[self.id])


class Institution(HsscBase):
    class Meta:
        verbose_name = "机构"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)


# 职员基本信息
class Staff(HsscBase):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=True, verbose_name='员工')
    role = models.ManyToManyField(Role, related_name='staff_role', verbose_name='角色')
    email = models.EmailField(max_length=50)
    Title = [(i, i) for i in ['主任医师', '副主任医师', '主治医师', '住院医师', '主任护师', '副主任护师', '主管护师', '护士长', '护士', '其他']]
    title = models.PositiveSmallIntegerField(choices=Title, blank=True, null=True, verbose_name='职称')
    is_assistant_physician = models.BooleanField(blank=True, null=True, verbose_name='助理医师')
    resume = models.TextField(blank=True, null=True, verbose_name='简历')
    Service_Lever = [(i, i) for i in ['低', '中', '高']]
    service_lever = models.PositiveSmallIntegerField(choices=Service_Lever, blank=True, null=True, verbose_name='服务级别')
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='挂号费')
    standardized_workload = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='标化工作量')
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="隶属机构")
    wecom_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="企业微信id")

    class Meta:
        verbose_name = "员工基本信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.label:
            self.label = self.customer.label
        if not self.name:
            self.name = self.customer.name
        super().save(*args, **kwargs)
        VirtualStaff.objects.get_or_create(staff=self)

    def delete(self, *args, **kwargs):
        virtual_staff = VirtualStaff.objects.filter(staff=self)
        virtual_staff.delete()
        super().delete(*args, **kwargs)


# 工作小组
class Workgroup(HsscBase):
    leader = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='workgroup_customer', null=True, verbose_name='组长')
    members = models.ManyToManyField(Staff, related_name='workgroup_members', verbose_name='组员')

    class Meta:
        verbose_name = "服务小组"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.label:
            self.label = self.leader.customer.label + '小组'
        if not self.name:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)
        VirtualStaff.objects.get_or_create(workgroup=self, is_workgroup=True)
    
    def delete(self, *args, **kwargs):
        virtual_staff = VirtualStaff.objects.filter(workgroup=self)
        virtual_staff.delete()
        super().delete(*args, **kwargs)


# 虚拟职员数据结构定义：
class VirtualStaff(HsscBase):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, blank=True, null=True, verbose_name='职员')
    workgroup = models.OneToOneField(Workgroup, on_delete=models.CASCADE, blank=True, null=True, verbose_name='工作小组')
    is_workgroup = models.BooleanField(default=False, verbose_name='是否为工作小组')

    class Meta:
        verbose_name = "虚拟职员"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def clean(self):
        if not (self.staff or self.workgroup):
            raise ValidationError('一个虚拟职员实例必须关联一个职员或工作小组。')
        if self.staff and self.workgroup:
            raise ValidationError('一个虚拟职员实例不能同时关联职员和工作小组。')

    def save(self, *args, **kwargs):
        self.clean()
        if not self.label:
            if self.is_workgroup:
                self.label = self.workgroup.label
            else:
                self.label = self.staff.label
        if not self.name:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super(VirtualStaff, self).save(*args, **kwargs)


class CustomerServiceLogManager(models.Manager):
    def get_customer_service_log(self, customer, period='ALL', form_class=0):
        # 返回客户的给定时间段的服务日志
        if period == 'ALL':  # 获取全部健康记录
            logs = self.filter(customer=customer)
        elif period == 'LAST_WEEK_SERVICES':  # 获取表示指定时间段内的健康记录
            start_time = timezone.now() + timedelta(days=-7)
            end_time = timezone.now()
            logs= self.filter(customer=customer, created_time__range=(start_time, end_time)).order_by('created_time')
            
        # 返回指定表单类别的服务日志
        if form_class > 0:
            logs = logs.filter(form_class=form_class)
        return logs

# 客户健康记录
class CustomerServiceLog(HsscBase):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='customer_service_log_customer', verbose_name="客户")
    operator = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='customer_service_log_operator', verbose_name="操作员")
    creater = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='customer_service_log_creater', verbose_name="创建者")
    pid = models.OneToOneField(OperationProc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    cpid = models.ForeignKey(ContractServiceProc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="服务进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")
    created_time = models.DateTimeField(editable=False, null=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(editable=False, null=True, verbose_name="更新时间")
    Form_class = [(1, '调查类'), (2, '诊断类'), (3, '治疗类')]
    form_class = models.PositiveSmallIntegerField(choices=Form_class, null=True, verbose_name="表单类型")
    data = models.JSONField(blank=True, null=True, encoder=JSONEncoder, verbose_name="服务记录")

    logs = CustomerServiceLogManager()

    class Meta:
        verbose_name = "客户服务记录"
        verbose_name_plural = verbose_name
        ordering = ['created_time']

    def __str__(self):
        return f'{self.name}--{self.created_time}'

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.created_time:
            self.created_time = timezone.now()
        self.updated_time = timezone.now()

        return super().save(*args, **kwargs)


# 推荐服务
class RecommendedService(HsscBase):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='recommended_service_customer', verbose_name="客户")
    operator = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='recommended_service_operator', verbose_name="操作员")
    creater = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='recommended_service_creater', verbose_name="创建者")
    pid = models.ForeignKey(OperationProc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="推荐进程")
    age = models.SmallIntegerField(blank=True, null=True, verbose_name="年龄")
    cpid = models.ForeignKey(ContractServiceProc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="上层服务进程")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")
    created_time = models.DateTimeField(editable=False, null=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(editable=False, null=True, verbose_name="更新时间")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name="推荐服务")
    counter = models.PositiveSmallIntegerField(default=0, verbose_name="推荐次数")
    Receive_form = [(0, '否'), (1, '接收，不可编辑'), (2, '接收，可以编辑')]  # 接收表单数据
    passing_data = models.PositiveSmallIntegerField(choices=Receive_form, default=0,  blank=True, null=True, verbose_name='接收表单')

    class Meta:
        verbose_name = "推荐服务"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        if self.service:
            return str(self.service.label)
        else:
            return ''

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.created_time:
            self.created_time = timezone.now()
        self.updated_time = timezone.now()

        return super().save(*args, **kwargs)


class Message(HsscBase):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='message_customer', verbose_name="客户")
    operator = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='message_operator', verbose_name="操作员")
    creater = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='message_creater', verbose_name="创建者")
    pid = models.ForeignKey(OperationProc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    cpid = models.ForeignKey(ContractServiceProc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="服务进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")
    created_time = models.DateTimeField(editable=False, null=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(editable=False, null=True, verbose_name="更新时间")
    message = models.CharField(max_length=512, blank=True, null=True, verbose_name="消息")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")

    class Meta:
        verbose_name = "消息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.message)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.created_time:
            self.created_time = timezone.now()
        self.updated_time = timezone.now()

        return super().save(*args, **kwargs)


# 药品基本信息表
class Medicine(HsscPymBase):
    yp_code = models.CharField(max_length=10, null=True, verbose_name="药品编码")
    specification = models.CharField(max_length=100, null=True, verbose_name="规格")
    cf_measure = models.CharField(max_length=30, null=True, verbose_name="处方剂量单位")
    dosage = models.CharField(max_length=60, null=True, verbose_name="常用剂量")
    usage = models.CharField(max_length=60, null=True, verbose_name="用药途径")
    fypc = models.CharField(max_length=255, null=True, verbose_name="用药频次")
    fyzysxhbz = models.CharField(max_length=255, null=True, verbose_name="用药备注")
    type = models.CharField(max_length=40, null=True, verbose_name="药剂类型")
    yp_sort = models.CharField(max_length=60, null=True, verbose_name="药品分类")
    ypglsx = models.CharField(max_length=60, null=True, verbose_name="药品管理属性")
    ypty_name = models.CharField(max_length=200, null=True, verbose_name="药品通用名称")
    gjjbyp = models.CharField(max_length=100, null=True, verbose_name="国家基本药品目录名称")
    ybypbm = models.CharField(max_length=100, null=True, verbose_name="医保药品目录对应药品编码")
    ybyplb = models.CharField(max_length=2, null=True, verbose_name="医保报销类别")
    syz = models.CharField(max_length=255, null=True, verbose_name="适应症")
    bsyz = models.CharField(max_length=255, null=True, verbose_name="不适应症")
    blfy = models.CharField(max_length=255, null=True, verbose_name="不良反应")
    mz_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="门诊参考单价")

    class Meta:
        verbose_name = "药品基本信息表"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.label


class HsscFormModel(HsscBase):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='%(class)s_customer', verbose_name="客户")
    operator = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='%(class)s_operator', verbose_name="操作员")
    creater = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='%(class)s_creater', verbose_name="创建者")
    pid = models.ForeignKey(OperationProc, on_delete=models.SET_NULL, blank=True, null=True, related_name='%(class)s_pid', verbose_name="作业进程")
    cpid = models.ForeignKey(ContractServiceProc, on_delete=models.SET_NULL, blank=True, null=True, related_name='%(class)s_sid', verbose_name="服务进程")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")
    created_time = models.DateTimeField(editable=False, null=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(editable=False, null=True, verbose_name="更新时间")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        if not self.created_time:
            self.created_time = timezone.now()
        self.updated_time = timezone.now()

        # 检查label字段，如果为空，则将label赋值为verbose_name和customer.name的组合，以'-'分隔
        if not self.label:
            self.label = f"{self._meta.verbose_name}-{self.customer.name}"
        if not self.name:
            self.name = f"{type(self).__name__}-{self.hssc_id}"

        return super().save(*args, **kwargs)

    def get_autocomplete_fields(self):
        autocompelte_fields_name=[]
        for field in self.__class__._meta.get_fields():
            if (field.one_to_one or field.many_to_one):  # 一对一、多对一字段
                autocompelte_fields_name.append(field.name)
        return autocompelte_fields_name

    def get_absolute_url(self):
        return reverse(f'{self.__class__.__name__}_detail_url', kwargs={'slug':self.slug})


# 保险服务专用
# 承保人员清单
class ChengBaoRenYuanQingDan(models.Model):
    序号=models.CharField(max_length=255, blank=True, null=True, verbose_name="序号")
    保单号=models.CharField(max_length=255, blank=True, null=True, verbose_name="保单号")
    被保人姓名=models.CharField(max_length=255, blank=True, null=True, verbose_name="被保人姓名")
    证件类型=models.CharField(max_length=255, blank=True, null=True, verbose_name="证件类型")
    身份证号=models.CharField(max_length=255, blank=True, null=True, verbose_name="身份证号")
    出生日期=models.CharField(max_length=255, blank=True, null=True, verbose_name="出生日期")
    保险责任=models.CharField(max_length=255, blank=True, null=True, verbose_name="保险责任")
    保险有效期=models.CharField(max_length=255, blank=True, null=True, verbose_name="保险有效期")
    联系方式=models.CharField(max_length=255, blank=True, null=True, verbose_name="联系方式")

    class Meta:
        verbose_name = "导入表-承保人员清单"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.被保人姓名)


# **********************************************************************************************************************
# 业务数据备份
# **********************************************************************************************************************
class BackupData(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True, verbose_name="版本")
    label = models.CharField(max_length=255, null=True, blank=True, verbose_name="版本名称")
    code = models.TextField(null=True, verbose_name="源代码")
    description = models.TextField(max_length=255, verbose_name="描述", null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")  

    class Meta:
        verbose_name = "业务数据备份"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.create_time)
