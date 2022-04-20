from django.db import models
from django.db.models.deletion import CASCADE
from django.shortcuts import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.forms.models import model_to_dict
from django.utils import timezone
from django.utils.text import slugify
from enum import Enum
from time import time
import datetime
from itertools import chain
import json
import uuid
from pypinyin import lazy_pinyin
from hssc.hsscbase_class import HsscBase, HsscPymBase
from icpc.models import Icpc

# 系统保留事件(form, event_name)
SYSTEM_EVENTS = [
    ('user_registry', 'user_registry_completed'),     # 用户注册
    ('user_login', 'user_login_completed'),           # 用户登录
    ('doctor_login', 'doctor_login_completed'),       # 医生注册
]

# 系统保留作业
SYSTEM_OPERAND = [
	{'name': 'user_registry', 'label': '用户注册', 'forms': None},     # 用户注册
	{'name': 'user_login', 'label': '用户登录', 'forms': None},        # 用户登录
	{'name': 'doctor_login', 'label': '员工登录', 'forms': None},      # 员工登录
]

def gen_slug(s):
    slug = slugify(s, allow_unicode=True)
    return slug + f'-{int(time())}'

# Role
# BuessinessForm
# ManagedEntity
# Service
# BuessinessFormsSetting
# ServicePackage
# ServicePackageDetail
# EventRule
# SystemOperand
# ServiceSpec
# ServiceProgramSetting


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
    meta_data = models.JSONField(null=True, blank=True, verbose_name="元数据")
    
    class Meta:
        verbose_name = '业务表单'
        verbose_name_plural = verbose_name


# 管理实体定义
class ManagedEntity(HsscPymBase):
    app_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="所属app名")
    model_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="模型名")
    base_form = models.OneToOneField('BuessinessForm', on_delete=models.SET_NULL, null=True, verbose_name="基础表单")

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
    group = models.ManyToManyField(Role, blank=True, verbose_name="服务岗位")
    History_services_display=[(0, '所有历史服务'), (1, '当日服务')]
    history_services_display = models.PositiveBigIntegerField(choices=History_services_display, default=0, blank=True, null=True, verbose_name='历史服务默认显示')
    enable_queue_counter = models.BooleanField(default=True, verbose_name='显示队列数量')
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
    script = models.TextField(blank=True, null=True, verbose_name='运行时脚本', help_text="script['views'] , script['urls'], script['templates']")

    class Meta:
        verbose_name = "服务"
        verbose_name_plural = verbose_name
        ordering = ['id']

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

    def execute(self, **kwargs):
        '''
        执行作业
        '''
        class SystemOperandFunc(Enum):
            CREATE_NEXT_SERVICE = self.create_next_service  # 生成后续服务
            RECOMMEND_NEXT_SERVICE = self.recommend_next_service  # 推荐后续服务
            VIOLATION_ALERT = self.alert_content_violations  # 内容违规提示
            SEND_NOTIFICATION = self.send_notification  # 发送提醒

		# 调用系统自动作业函数
        SystemOperandFunc[self.func].value(**kwargs)

    def create_next_service(self, **kwargs):
        '''
        生成后续服务
        '''
        operation = Operation.objects.get(name=kwargs['oname'])
        if kwargs['uid']:
            user_operater = User.objects.get(id=kwargs['uid'])
            operator = Staff.objects.get(user=user_operater)
        else:
            operator = None
        user_customer = User.objects.get(id=kwargs['cid'])
        customer = Customer.objects.get(user=user_customer)
        operator_groups = kwargs['group']

        # 创建作业进程
        try:
            parent_operation_proc = OperationProc.objects.get(id=kwargs['ppid'])
        except OperationProc.DoesNotExist:
            parent_operation_proc = None
        # service_proc = ServiceProc.objects.get(id=task_params['spid'])
        proc=OperationProc.objects.create(
            operation=operation,
            operator=None,
            customer=customer,
            state=0,
            ppid=parent_operation_proc,
            # service_proc=service_proc,
        )
        proc.group.add(*operator_groups)

        # 根据Operation.forms里的mutate类型的表单创建相关表单实例
        form_slugs = []
        forms = filter(lambda _forms: _forms['mutate_or_inquiry']=='mutate', json.loads(operation.forms))
        for form in forms:
            form_class_name = form['basemodel'].capitalize()
            print('创建表单实例:', form_class_name)
            try:
                form = globals()[form_class_name].objects.create(
                    operator = operator,
                    customer = customer,
                    pid = proc
                )
                form_slugs.append({'form_name': form_class_name, 'slug': form.slug})
            except Exception as e:
                print('创建model失败:', form_class_name, e)

        proc.entry = f'{operation.name}/{proc.id}/update_view'      # 更新作业URL路径 
        proc.form_slugs = json.dumps(form_slugs, ensure_ascii=False, indent=4)
        proc.save()

        return proc

    def recommend_next_service(self, **kwargs):
        '''
        推荐后续服务
        '''
        print('recommend_next_service:', '推荐后续服务' )

    def alert_content_violations(self, **kwargs):
        '''
        内容违规提示
        '''
        print('alert_content_violations:', '内容违规提示')

    def send_notification(self, **kwargs):
        '''
        发送提醒
        '''
        print('send_notification:', '发送提醒')


# 事件规则表
class EventRule(HsscBase):
    description = models.TextField(max_length=255, blank=True, null=True, verbose_name="表达式")
    Detection_scope = [(0, '所有历史表单'), (1, '本次服务表单'), (2, '单元服务表单')]
    detection_scope = models.PositiveSmallIntegerField(choices=Detection_scope, default=1, blank=True, null=True, verbose_name='检测范围')
    weight = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="权重")
    expression = models.TextField(max_length=1024, blank=True, null=True, verbose_name="内部表达式")

    class Meta:
        verbose_name = '条件事件'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def is_satified(self, **kwargs):
        '''
        检查表达式是否满足
        parameters: operation_proc_id
		'''
        from core.utils import keyword_replace
        is_satified = False
        operation_proc_id = kwargs.get('operation_proc_id')
        operation_proc = OperationProc.objects.get(id=operation_proc_id)
		# ...
        return is_satified


# 服务规格设置
class ServiceSpec(HsscBase):
    class Meta:
        verbose_name = "服务规格"
        verbose_name_plural = verbose_name
        ordering = ['id']


class CheckRuleManager(models.Manager):
    '''
    服务表单保存后根据服务规则生成业务事件
    params: operation_proc.hssc_id, service.hssc_id
    return: 
    how:
		0. 获取服务作业完成信号
		1. 根据service.hssc_id获取需要检查的service_rule集合
		2. 逐一检查event_rule.expression是否满足
		3. 若满足则构造事件参数，生成自定义信号“发生业务事件”，传给调度函数。事件参数：{}
    '''
    # 导入自定义作业完成信号
    from core.signals import operand_finished
    @receiver(operand_finished)
    def check_rules(self, sender, **kwargs):
        operation_proc_id = kwargs['operation_proc_id']  # 作业进程id
        # 根据operation_proc_hssc_id获取operation_proc
        operation_proc = OperationProc.objects.get(hssc_id=operation_proc_id)
		# 根据operation_proc.service.hssc_id获取service_rule集合
        service_rules = self.filter(service=operation_proc.service)
		# 逐一检查event_rule.expression是否满足
        for service_rule in service_rules:
			# 如果event_rule.expression为真，则构造事件参数，生成业务事件
            if service_rule.event_rule.is_satified(operation_proc_id):
				# 构造作业参数
                operations_params = {}
				# 执行系统自动作业
                service_rule.system_operand.execute(**operations_params)
        return None
	
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
    message_content = models.CharField(max_length=255, blank=True, null=True, verbose_name='消息内容')
    Interval_rule_options = [(0, '等于'), (1, '小于'), (2, '大于')]
    interval_rule = models.PositiveSmallIntegerField(choices=Interval_rule_options, blank=True, null=True, verbose_name='间隔条件')
    interval_time = models.DurationField(blank=True, null=True, verbose_name="间隔时间", help_text='例如：3 days, 22:00:00')
    Is_active = [(False, '否'), (True, '是')]
    is_active = models.BooleanField(choices=Is_active, default=True, verbose_name='启用')
    service_spec = models.ForeignKey(ServiceSpec, on_delete=models.CASCADE, null=True, verbose_name='服务规格')
    rules = CheckRuleManager()

    class Meta:
        verbose_name = '服务规则'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str(self.service)


# 服务进程表 ServiceProc
class ServiceProc(models.Model):
	# 服务进程id: spid
	service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="服务")  # 服务id: sid
	operator = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='service_proc_operator', verbose_name="服务专员")  # 作业人员id: uid
	customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='service_proc_customer', verbose_name="客户")  # 客户id: cid
	# workgroup = models.ForeignKey('Workgroup', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="工作组")  # 工作小组：workgroup
	
	def __str__(self):
		# return 服务名称-服务进程号spid
		# return f'{self.service.name}-{str(self.id)}'
		return "%s: %s" %(self.service.name, self.id)

	# def get_absolute_url(self):
	# 	# 返回作业入口url
	# 	return self.operation.entry

	class Meta:
		verbose_name = "服务进程"
		verbose_name_plural = "服务进程"
		ordering = ['id']


class OperationProcManager(models.Manager):
	# 当天常规任务, 优先级=2/3
	def current_operations(self, operator):
		procs = self.values('service__name', 'customer__name').filter(operator=operator, priority__in=[2, 3], scheduled_time__gte=datetime.datetime.now().date())
		return procs
	
	# 当天紧急任务, 优先级=1
	def urgent_operations(self, operator):
		procs = self.values('service__name', 'customer__name').filter(operator=operator, priority=1)
		return procs

	# 本周任务
	def week_operations(self, operator):
		today = datetime.date.today()
		this_week = [today + datetime.timedelta(days=1), today + datetime.timedelta(days=7)]
		procs = self.values('service__name', 'customer__name').filter(operator=operator, scheduled_time__range=this_week)
		return procs

#作业进程状态机操作码ocode
class OperationCode(Enum):
	CRE = 0  # CREATE
	CTR = 1  # CREATED TO READY
	RTR = 2  # READY TO RUNNING
	RTH = 3  # RUNNING TO HANGUP
	HTR = 4  # HANGUP TO READY
	RTC = 5  # RUNNING TO COMPLETED

# 作业进程表 OperationProc
class OperationProc(models.Model):
    # 作业进程id: pid
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name="服务")  # 作业id: oid
    operator = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='operation_proc_operator', verbose_name="操作员")  # 作业员id: uid
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='operation_proc_customer', verbose_name="客户")  # 客户id: cid
    group = models.ManyToManyField(Role, blank=True, verbose_name="角色组")  # 角色组：workgroup
	# 作业状态: state
    Operation_proc_state = [(0, '创建'), (1, '就绪'), (2, '运行'), (3, '挂起'), (4, '结束')]
    state = models.PositiveSmallIntegerField(choices=Operation_proc_state, verbose_name="作业状态")
    Operation_priority = [(0, '0级'), (1, '紧急'), (2, '优先'), (3, '一般')]
    priority = models.PositiveSmallIntegerField(choices=Operation_priority, default=3, verbose_name="优先级")
    entry = models.CharField(max_length=250, blank=True, null=True, db_index=True, verbose_name="作业入口")  # 作业入口: operand/<int:id>/update_view
    ppid = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="父进程")  # 父作业进程id: ppid
    service_proc = models.ForeignKey(ServiceProc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="服务进程")  # 服务进程id: spid
    form_slugs = models.JSONField(blank=True, null=True, verbose_name="表单索引")
    scheduled_time = models.DateTimeField(blank=True, null=True, verbose_name="计划时间")
    created_time = models.DateTimeField(editable=False, null=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(editable=False, null=True, verbose_name="修改时间")
    objects = OperationProcManager()

    class Meta:
        verbose_name = "作业进程"
        verbose_name_plural = "作业进程"
        ordering = ['id']

    def __str__(self):
	# 	# return 作业名称-客户姓名
        # return f'{self.operation.name}-{self.user.username}-{self.customer.username}'
        return "%s - %s - %s" %(self.id, self.service.label, self.customer.name)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_time = timezone.now()
        self.modified_time = timezone.now()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        # 返回作业入口url
        return self.entry

    def update_state(self, ocode):
        '''
        通过作业进程操作码维护作业进程状态：
	    	Operation_proc_state = [(0, '创建'), (1, '就绪'), (2, '运行'), (3, '挂起'), (4, '结束')]
        '''
        self.state = OperationCode[ocode].value
        self.save()

# 本段代码用于跟踪调试作业进程状态更新
@receiver(post_save, sender=OperationProc)
def new_operation_proc(instance, created, **kwargs):
    if created: # ctr
        print ('新作业进程被创建，进行资源请求...：new_operation_proc:', instance)
    else:
        if instance.state == 4:  # rtc            
            print('rtc状态, 作业完成事件，进行调度')


class HsscFormModel(HsscBase):
    created_time = models.DateTimeField(editable=False, null=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(editable=False, null=True, verbose_name="更新时间")
    pid = models.ForeignKey(OperationProc, on_delete=models.SET_NULL, blank=True, null=True, related_name='%(class)s_pid', verbose_name="作业进程id")
    sid = models.ForeignKey(ServiceProc, on_delete=models.SET_NULL, blank=True, null=True, related_name='%(class)s_sid', verbose_name="服务进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_time = timezone.now()
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
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

    def get_update_url(self):
        return reverse(f'{self.__class__.__name__}_update_url', kwargs={'slug':self.slug})

    def get_delete_url(self):
        return reverse(f'{self.__class__.__name__}_delete_url', kwargs={'slug':self.slug})


# 用户基本信息
class Customer(HsscFormModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='客户')
    name = models.CharField(max_length=50, verbose_name="姓名")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="电话")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="地址")
    charge_person = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='负责人')
    health_record = models.JSONField(blank=True, null=True, verbose_name="健康记录")

    class Meta:
        verbose_name = "客户注册信息"
        verbose_name_plural = "客户注册信息"

    def __str__(self):
        return str(self.name)

    def update_health_record(self, health_record):
        '''
        设置健康记录
        '''
        pass

    def get_mr_home_page(self):
        '''
        获取客户病案首页
        '''
        pass

    def get_history_services(self):
        pass

    def get_recommanded_services(self):
        pass

    def get_scheduled_services(self):
        pass


# 工作组
class Workgroup(HsscBase):
    leader = models.ForeignKey(Customer, on_delete=CASCADE, null=True, verbose_name='组长')

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


# 职员基本信息
class Staff(HsscFormModel):
	customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=True, verbose_name='员工')
	role = models.ManyToManyField(Role, related_name='staff_role', verbose_name='角色')
	email = models.EmailField(max_length=50)
	Title = [(i, i) for i in ['主任医师', '副主任医师', '主治医师', '住院医师', '主任护师', '副主任护师', '主管护师', '护士长', '护士', '其他']]
	title = models.PositiveSmallIntegerField(choices=Title, blank=True, null=True, verbose_name='职称')
	is_assistant_physician = models.BooleanField(blank=True, null=True, verbose_name='助理医师')
	resume = models.TextField(blank=True, null=True, verbose_name='简历')
	Service_Lever = [(i, i) for i in ['低', '中', '高']]
	service_lever = models.PositiveSmallIntegerField(choices=Service_Lever, blank=True, null=True, verbose_name='服务级别')
	workgroup = models.ManyToManyField(Workgroup, blank=True, verbose_name='服务小组')
	registration_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='挂号费')
	standardized_workload = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='标化工作量')

	def __str__(self):
		return str(self.name)

	class Meta:
		verbose_name = "员工基本信息"
		verbose_name_plural = "员工基本信息"


# # 作业事件表
# # # 默认事件：xx作业完成--系统作业名+"_operation_completed"
# class Event(models.Model):
#     name = models.CharField(max_length=255, db_index=True, unique=True, verbose_name="名称")
#     label = models.CharField(max_length=255, blank=True, null=True, verbose_name="规则")
#     operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name='from_oid', verbose_name="所属作业")
#     next = models.ManyToManyField(Operation, verbose_name="后续作业")
#     description = models.CharField(max_length=255, blank=True, null=True, verbose_name="规则说明")
#     expression = models.TextField(max_length=1024, blank=True, null=True, verbose_name="规则表达式", 
#         help_text='''
#         说明：<br>
#         1. 作业完成事件: completed<br>
#         2. 表达式接受的逻辑运算符：or, and, not, in, >=, <=, >, <, ==, +, -, *, /, ^, ()<br>
#         3. 字段名只允许由小写字母a~z，数字0~9和下划线_组成；字段值接受数字和字符，字符需要放在双引号中，如"A0101"
#         ''')
#     parameters = models.CharField(max_length=1024, blank=True, null=True, verbose_name="检查字段")
#     fields = models.TextField(max_length=1024, blank=True, null=True, verbose_name="可用字段")

#     def __str__(self):
#         return str(self.label)

#     class Meta:
#         verbose_name = "业务规则"
#         verbose_name_plural = "业务规则"
#         ordering = ['id']


# # 指令表
# class Instruction(models.Model):
#     name = models.CharField(max_length=100, db_index=True, unique=True, verbose_name="指令名称")
#     label = models.CharField(max_length=255, blank=True, null=True, verbose_name="显示名称")
#     code = models.CharField(max_length=10, verbose_name="指令代码")
#     func = models.CharField(max_length=100, verbose_name="操作函数")
#     description = models.CharField(max_length=255, blank=True, null=True, verbose_name="指令描述")

#     def __str__(self):
#         return str(self.name)

#     class Meta:
#         verbose_name = "指令"
#         verbose_name_plural = "指令"
#         ordering = ['id']


# # 事件指令程序表
# class Event_instructions(models.Model):
#     event = models.ForeignKey(Event, on_delete=models.CASCADE, db_index=True, verbose_name="事件")
#     instruction = models.ForeignKey(Instruction, on_delete=models.CASCADE, verbose_name="指令")
#     order = models.PositiveSmallIntegerField(default=1, verbose_name="指令序号")
#     params = models.CharField(max_length=255, blank=True, null=True, verbose_name="创建作业")

#     def __str__(self):
#         return self.instruction.name

#     class Meta:
#         verbose_name = "事件指令集"
#         verbose_name_plural = "事件指令集"
#         ordering = ['event', 'order']


