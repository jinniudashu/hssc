from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from enum import Enum
from time import time
import datetime

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
    
    class Meta:
        verbose_name = '业务表单'
        verbose_name_plural = verbose_name


# 管理实体定义
class ManagedEntity(HsscPymBase):
    app_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="所属app名")
    model_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="模型名")
    base_form = models.OneToOneField(BuessinessForm, on_delete=models.SET_NULL, null=True, verbose_name="基础表单")

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
    is_system_service = models.BooleanField(default=False, verbose_name='系统内置服务')
    role = models.ManyToManyField(Role, blank=True, verbose_name="服务岗位")
    History_services_display=[(0, '所有历史服务'), (1, '当日服务')]
    history_services_display = models.PositiveBigIntegerField(choices=History_services_display, default=0, blank=True, null=True, verbose_name='历史服务默认显示')
    enable_queue_counter = models.BooleanField(default=True, verbose_name='显示队列数量')
    Route_to = [('INDEX', '任务工作台'), ('CUSTOMER_HOMEPAGE', '客户病例首页')]
    route_to = models.CharField(max_length=50, choices=Route_to, default='CUSTOMER_HOMEPAGE', blank=True, null=True, verbose_name='完成跳转至')
    suppliers = models.CharField(max_length=255, blank=True, null=True, verbose_name="供应商")
    not_suitable = models.CharField(max_length=255, blank=True, null=True, verbose_name='不适用对象')
    execution_time_frame = models.DurationField(blank=True, null=True, verbose_name='完成时限')
    awaiting_time_frame = models.DurationField(blank=True, null=True, verbose_name='等待执行时限')
    working_hours = models.DurationField(blank=True, null=True, verbose_name='工时')
    frequency = models.CharField(max_length=255, blank=True, null=True, verbose_name='频次')
    cost = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2, verbose_name='成本')
    load_feedback = models.BooleanField(default=False, verbose_name='是否反馈负荷数量')
    resource_materials = models.CharField(max_length=255, blank=True, null=True, verbose_name='配套物料')
    resource_devices = models.CharField(max_length=255, blank=True, null=True, verbose_name='配套设备')
    resource_knowledge = models.CharField(max_length=255, blank=True, null=True, verbose_name='服务知识')

    class Meta:
        verbose_name = "服务"
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


# 服务包类型信息表
class ServicePackage(HsscPymBase):
    name_icpc = models.OneToOneField(Icpc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="ICPC编码")
    services = models.ManyToManyField(Service, through='ServicePackageDetail', verbose_name="服务项目")
    Begin_time_setting = [(0, '人工指定'), (1, '出生日期')]
    begin_time_setting = models.PositiveSmallIntegerField(choices=Begin_time_setting, default=0, verbose_name='开始时间参考')
    duration = models.DurationField(blank=True, null=True, verbose_name="持续周期", help_text='例如：3 days, 22:00:00')
    execution_time_frame = models.DurationField(blank=True, null=True, verbose_name='执行时限')
    awaiting_time_frame = models.DurationField(blank=True, null=True, verbose_name='等待执行时限')

    class Meta:
        verbose_name = "服务包"
        verbose_name_plural = verbose_name
        ordering = ['id']

class ServicePackageDetail(HsscPymBase):
    servicepackage = models.ForeignKey(ServicePackage, on_delete=models.CASCADE, verbose_name='服务包')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    Cycle_options = [(0, '总共'), (1, '每天'), (2, '每周'), (3, '每月'), (4, '每季'), (5, '每年')]
    cycle_option = models.PositiveSmallIntegerField(choices=Cycle_options, default=0, blank=True, null=True, verbose_name='周期')
    cycle_times = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="次数")
    reference_start_tim = models.DurationField(blank=True, null=True, verbose_name="参考起始时间", help_text='例如：3 days, 22:00:00')
    duration = models.DurationField(blank=True, null=True, verbose_name="持续周期", help_text='例如：3 days, 22:00:00')
    check_awaiting_timeout = models.BooleanField(default=False, verbose_name='检查等待超时')

    class Meta:
        verbose_name = "服务内容模板"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.service)


# 系统作业指令表
class SystemOperand(HsscBase):
    func = models.CharField(max_length=255, blank=True, null=True, verbose_name="内部实现函数")
    parameters = models.CharField(max_length=255, blank=True, null=True, verbose_name="参数")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="描述")
    Applicable = [(0, '作业'), (1, '单元服务'), (2, '服务包'), (3, '全部')]
    applicable = models.PositiveSmallIntegerField(choices=Applicable, default=1, verbose_name='适用范围')

    class Meta:
        verbose_name = '系统自动作业'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.func


# 事件规则表
class EventRule(HsscBase):
    description = models.TextField(max_length=255, blank=True, null=True, verbose_name="表达式")
    Detection_scope = [('ALL', '所有历史表单'), ('CURRENT_SERVICE', '本次服务表单'), ('LAST_WEEK_SERVICES', '过去7天表单')]
    detection_scope = models.CharField(max_length=100, choices=Detection_scope, default='CURRENT_SERVICE', blank=True, null=True, verbose_name='检测范围')
    weight = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="权重")
    expression = models.TextField(max_length=1024, blank=True, null=True, verbose_name="内部表达式")
    expression_fields = models.CharField(max_length=1024, blank=True, null=True, verbose_name="内部表达式字段")

    class Meta:
        verbose_name = '条件事件'
        verbose_name_plural = verbose_name
        ordering = ['id']


# 服务规格设置
class ServiceSpec(HsscBase):
    class Meta:
        verbose_name = "服务规格"
        verbose_name_plural = verbose_name
        ordering = ['id']


# 服务规则库
class ServiceRule(HsscBase):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    event_rule = models.ForeignKey(EventRule, on_delete=models.CASCADE,  blank=True, null=True, verbose_name='条件事件')
    system_operand = models.ForeignKey(SystemOperand, on_delete=models.CASCADE, blank=True, null=True, verbose_name='系统作业')
    next_service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True, related_name='next_service', verbose_name='后续服务')
    Receive_form = [(0, '否'), (1, '接收，不可编辑'), (2, '接收，可以编辑')]  # 接收表单数据
    passing_data = models.PositiveSmallIntegerField(choices=Receive_form, default=0,  blank=True, null=True, verbose_name='接收表单')
    Complete_feedback = [(0, '否'), (1, '返回完成状态'), (2, '返回表单')]
    complete_feedback = models.PositiveSmallIntegerField(choices=Complete_feedback, default=0,  blank=True, null=True, verbose_name='完成反馈')
    Reminders = [(0, '客户'), (1, '服务人员'), (2, '服务小组')]
    reminders = models.PositiveSmallIntegerField(choices=Reminders, default=0,  blank=True, null=True, verbose_name='提醒对象')
    message = models.CharField(max_length=512, blank=True, null=True, verbose_name='消息内容')
    Interval_rule_options = [(0, '等于'), (1, '小于'), (2, '大于')]
    interval_rule = models.PositiveSmallIntegerField(choices=Interval_rule_options, blank=True, null=True, verbose_name='间隔条件')
    interval_time = models.DurationField(blank=True, null=True, verbose_name="间隔时间", help_text='例如：3 days, 22:00:00')
    is_active = models.BooleanField(choices=[(False, '否'), (True, '是')], default=True, verbose_name='启用')
    service_spec = models.ForeignKey(ServiceSpec, on_delete=models.CASCADE, null=True, verbose_name='服务规格')

    class Meta:
        verbose_name = '服务规则'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.service)


class ContractService(HsscPymBase):
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


# **********************************************************************************************************************
# Service进程管理Model
# **********************************************************************************************************************

# 服务进程表 ServiceProc
class ContractServiceProc(HsscBase):
    contract_service = models.ForeignKey(ContractService, on_delete=models.CASCADE, verbose_name="合约服务")
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='service_proc_customer', verbose_name="客户")  # 客户id: cid
    creater = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='service_proc_creater', verbose_name="创建者")  # 创建者id: cid
    current_service = models.ForeignKey(Service, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业状态")
    Operation_priority = [(0, '0级'), (1, '紧急'), (2, '优先'), (3, '一般')]
    priority = models.PositiveSmallIntegerField(choices=Operation_priority, default=3, verbose_name="优先级")

    class Meta:
        verbose_name = "合约服务进程"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.customer.name


class OperationProcManager(models.Manager):
    def get_service_queue_count(self, service):
        return self.filter(service=service, state__lt=4).count()

    def get_unassigned_proc(self, operator):
	# 获取待分配作业进程: 状态为创建，且未分配操作员，服务岗位为操作员所属岗位，以及用户服务小组为操作员所属服务小组
        return self.filter(state=0, operator=None, service__in=Service.objects.filter(role__in=operator.staff.role.all()),)
    
# 作业进程表 OperationProc
class OperationProc(HsscBase):
    # 作业进程id: pid
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name="服务")  # 作业id: oid
    operator = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='operation_proc_operator', verbose_name="操作员")  # 作业员id: uid
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='operation_proc_customer', verbose_name="客户")  # 客户id: cid
    creater = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='operation_proc_creater', verbose_name="创建者")  # 创建者id: cid
    role = models.ManyToManyField(Role, blank=True, verbose_name="作业岗位")
	# 作业状态: state
    Operation_proc_state = [(0, '创建'), (1, '就绪'), (2, '运行'), (3, '挂起'), (4, '结束')]
    state = models.PositiveSmallIntegerField(choices=Operation_proc_state, verbose_name="作业状态")
    priority = models.PositiveSmallIntegerField(choices=[(0, '0级'), (1, '紧急'), (2, '优先'), (3, '一般')], default=3, verbose_name="优先级")
    entry = models.CharField(max_length=250, blank=True, null=True, db_index=True, verbose_name="作业入口")  # 作业入口: /clinic/service/model_name/model_id/change
    parent_proc = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="父进程")  # 父作业进程id: ppid
    contract_service_proc = models.ForeignKey(ContractServiceProc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="服务进程")  # 服务进程id: spid
    form_slugs = models.JSONField(blank=True, null=True, verbose_name="表单索引")
    scheduled_time = models.DateTimeField(blank=True, null=True, verbose_name="计划执行时间")
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
		# return 作业名称-客户姓名
        return "%s - %s - %s" %(self.id, self.service.label, self.creater.name)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_time = timezone.now()
        self.modified_time = timezone.now()
        if not self.name:
            self.name = self.service.label
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        # 返回作业入口url
        return self.entry

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
    

class StaffTodoManager(models.Manager):
	# 当天常规任务
    def today_todos(self, operator):
        today = datetime.date.today()
        return self.filter(
            operator=operator, 
            priority=3,
            scheduled_time__year=int(today.strftime('%Y')),
            scheduled_time__month=int(today.strftime('%m')),
            scheduled_time__day=int(today.strftime('%d')),
            ).exclude(state=4)
        
	# 紧要任务安排
    def urgent_todos(self, operator):
        return self.filter(operator=operator, priority__lt=3).exclude(state=4).order_by('priority')

	# 未来七天任务
    def week_todos(self, operator):
        # today = datetime.date.today()
        startTime = datetime.datetime.now() + datetime.timedelta(days=1)
        endTime = datetime.datetime.now() + datetime.timedelta(days=7)
        return self.filter(
            operator=operator, 
            priority=3, 
            # scheduled_time__year=int(today.strftime('%Y')),
            # scheduled_time__week=int(today.strftime('%W')),
            scheduled_time__range=(startTime, endTime),
            ).exclude(state=4)

class StaffTodo(HsscBase):
    operation_proc = models.OneToOneField(OperationProc, on_delete=models.CASCADE, verbose_name="作业进程")
    operator = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="操作员")
    scheduled_time = models.DateTimeField(blank=True, null=True, verbose_name="计划执行时间")
    Operation_proc_state = [(0, '创建'), (1, '就绪'), (2, '运行'), (3, '挂起'), (4, '结束')]
    state = models.PositiveSmallIntegerField(choices=Operation_proc_state, verbose_name="作业状态")
    customer_number = models.CharField(max_length=250, blank=True, null=True, verbose_name="居民档案号")
    customer_name = models.CharField(max_length=250, blank=True, null=True, verbose_name="姓名")
    service_label = models.CharField(max_length=250, blank=True, null=True, verbose_name="服务项目")
    customer_phone = models.CharField(max_length=250, blank=True, null=True, verbose_name="联系电话")
    customer_address = models.CharField(max_length=250, blank=True, null=True, verbose_name="家庭地址")
    priority = models.PositiveSmallIntegerField(choices=[(0, '0级'), (1, '紧急'), (2, '优先'), (3, '一般')], default=3, verbose_name="优先级")
    objects = StaffTodoManager()

    class Meta:
        verbose_name = "员工任务清单"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return "%s - %s - %s" %(self.id, self.service_label, self.customer_name)

    def save(self, *args, **kwargs):
        if not self.label:
            self.label = f'{self.customer_name} - {self.service_label}'
        return super().save(*args, **kwargs)


# 用户基本信息
class Customer(HsscBase):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='客户')
    name = models.CharField(max_length=50, verbose_name="姓名")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="电话")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="地址")
    charge_staff = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='负责人')
    workgroup = models.ForeignKey('Workgroup', on_delete=models.SET_NULL, blank=True, null=True, related_name='customer_workgroup', verbose_name='服务小组')
    health_record = models.JSONField(blank=True, null=True, verbose_name="健康记录")
    upload = models.ImageField(upload_to='uploads/', blank=True, null=True, verbose_name="个人照片")

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
        return self.operation_proc_customer.filter(state=4).exclude(service__in=Service.objects.filter(is_system_service=True))

    def get_recommended_services(self) -> 'QuerySet[RecommendedService]':
        '''
        获取客户推荐服务列表
        '''
        return self.recommended_service_customer.all()

    def get_scheduled_services(self) -> 'QuerySet[OperationProc]':
        '''
        获取已安排服务列表
        '''
        return self.operation_proc_customer.filter(state__in = [0, 1, 2, 3])

    def get_absolute_url(self):
        return reverse('customer_homepage', args=[self.id])


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


# 工作组
class Workgroup(HsscBase):
    leader = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='workgroup_customer', null=True, verbose_name='组长')
    members = models.ManyToManyField(Staff, related_name='workgroup_members', blank=True, verbose_name='组员')

    class Meta:
        verbose_name = "服务小组"
        verbose_name_plural = "服务小组"
        ordering = ['id']

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)


class CustomerServiceLogManager(models.Manager):
    def get_customer_service_log(self, customer, period=None):
        # 返回客户的给定时间段的服务日志
        if period:
            return self.filter(customer=customer, created_time__range=period).order_by('created_time')
        return self.filter(customer=customer)

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
    Log_category = [('Subjective', '主观资料'), ('ObjectiveO', '客观资料'), ('Assessment', '诊断与评价'), ('Plan', '治疗方案'), ('Management', '管理活动')]
    category = models.CharField(max_length=50, choices=Log_category , blank=True, null=True, verbose_name="记录类别")
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
    pid = models.ForeignKey(OperationProc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    cpid = models.ForeignKey(ContractServiceProc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="服务进程id")
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
        return str(self.service.label)

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


class HsscFormModel(HsscBase):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='%(class)s_customer', verbose_name="客户")
    operator = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='%(class)s_operator', verbose_name="操作员")
    creater = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='%(class)s_creater', verbose_name="创建者")
    pid = models.OneToOneField(OperationProc, on_delete=models.SET_NULL, blank=True, null=True, related_name='%(class)s_pid', verbose_name="作业进程id")
    cpid = models.ForeignKey(ContractServiceProc, on_delete=models.SET_NULL, blank=True, null=True, related_name='%(class)s_sid', verbose_name="服务进程id")
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

        return super().save(*args, **kwargs)

    def get_autocomplete_fields(self):
        autocompelte_fields_name=[]
        for field in self.__class__._meta.get_fields():
            if (field.one_to_one or field.many_to_one):  # 一对一、多对一字段
                autocompelte_fields_name.append(field.name)
        return autocompelte_fields_name

    def get_absolute_url(self):
        return reverse(f'{self.__class__.__name__}_detail_url', kwargs={'slug':self.slug})


class HsscBaseFormModel(HsscFormModel):
    pym = models.CharField(max_length=255, blank=True, null=True, verbose_name="拼音码")

    def save(self, *args, **kwargs):
        if self.name:
            self.pym = ''.join(lazy_pinyin(self.label, style=Style.FIRST_LETTER))
        super().save(*args, **kwargs)
    
    def natural_key(self):
        return self.name
