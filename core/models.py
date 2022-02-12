from django.db import models
from django.db.models.deletion import CASCADE
from django.shortcuts import reverse
from django.contrib.auth.models import User, Group

from time import time
from django.utils.text import slugify
from pypinyin import lazy_pinyin

import json


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


class Workgroup(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='名称')
    label = models.CharField(max_length=255, verbose_name='服务小组名称')
    group_leader = models.ForeignKey('Staff', on_delete=CASCADE, related_name='group_leader', verbose_name='组长')

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "服务小组"
        verbose_name_plural = "服务小组"
        ordering = ['id']


class Staff(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff', verbose_name='员工')
	name = models.CharField(max_length=50)
	role = models.ManyToManyField(Group, related_name='staff_role', verbose_name='角色')
	email = models.EmailField(max_length=50)
	Title = [(i, i) for i in ['主任医师', '副主任医师', '主治医师', '住院医师', '主任护师', '副主任护师', '主管护师', '护士长', '护士', '其他']]
	title = models.PositiveSmallIntegerField(choices=Title, blank=True, null=True, verbose_name='职称')
	assistant_physician = models.BooleanField(blank=True, null=True, verbose_name='助理医师')
	resume = models.TextField(blank=True, null=True, verbose_name='简历')
	Service_Lever = [(i, i) for i in ['低', '中', '高']]
	service_lever = models.PositiveSmallIntegerField(choices=Service_Lever, blank=True, null=True, verbose_name='服务级别')
	phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='电话')
	workgroup = models.ManyToManyField(Workgroup, verbose_name='服务小组')
	registration_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='挂号费')
	standardized_workload = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='标化工作量')
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.name)

	class Meta:
		verbose_name = "员工基本信息"
		verbose_name_plural = "员工基本信息"

	def get_absolute_url(self):
		return reverse("Staff_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("Staff_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("Staff_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer', verbose_name='客户')
	name = models.CharField(max_length=50)
	phone = models.CharField(max_length=20, blank=True, null=True)
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.name)

	class Meta:
		verbose_name = "客户注册信息"
		verbose_name_plural = "客户注册信息"

	def get_absolute_url(self):
		return reverse("Staff_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("Staff_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("Staff_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


# 作业信息表
class Operation(models.Model):
	name = models.CharField(max_length=255, verbose_name="作业名称")
	label = models.CharField(max_length=255, blank=True, null=True, verbose_name="显示名称")
	forms = models.JSONField(null=True, blank=True, verbose_name="视图元数据")
	# icpc = models.OneToOneField(Icpc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="ICPC")
	Operation_priority = [
		(0, '0级'),
		(1, '紧急'),
		(2, '优先'),
		(3, '一般'),
	]
	priority = models.PositiveSmallIntegerField(choices=Operation_priority, default=3, verbose_name='优先级')
	group = models.ManyToManyField(Group, verbose_name="作业角色")
	suppliers = models.CharField(max_length=255, blank=True, null=True, verbose_name="供应商")
	not_suitable = models.CharField(max_length=255, blank=True, null=True, verbose_name='不适用对象')
	time_limits = models.DurationField(blank=True, null=True, verbose_name='完成时限')
	working_hours = models.DurationField(blank=True, null=True, verbose_name='工时')
	frequency = models.CharField(max_length=255, blank=True, null=True, verbose_name='频次')
	cost = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=2, verbose_name='成本')
	load_feedback = models.BooleanField(default=False, verbose_name='是否反馈负荷数量')
	resource_materials = models.CharField(max_length=255, blank=True, null=True, verbose_name='配套物料')
	resource_devices = models.CharField(max_length=255, blank=True, null=True, verbose_name='配套设备')
	resource_knowledge = models.CharField(max_length=255, blank=True, null=True, verbose_name='服务知识')

	def __str__(self):
		return self.label

	class Meta:
		verbose_name = "作业"
		verbose_name_plural = "作业"
		ordering = ['id']


# 服务类型信息表
class Service(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="名称")
    label = models.CharField(max_length=255, verbose_name="显示名称")
    # icpc = models.OneToOneField(Icpc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="ICPC")
    first_operation = models.ForeignKey(Operation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="起始作业")
	
    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "服务"
        verbose_name_plural = "服务"
        ordering = ['id']


# 作业事件表
# # 默认事件：xx作业完成--系统作业名+"_operation_completed"
class Event(models.Model):
    name = models.CharField(max_length=255, db_index=True, unique=True, verbose_name="名称")
    label = models.CharField(max_length=255, blank=True, null=True, verbose_name="规则")
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name='from_oid', verbose_name="所属作业")
    next = models.ManyToManyField(Operation, verbose_name="后续作业")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="规则说明")
    expression = models.TextField(max_length=1024, blank=True, null=True, verbose_name="规则表达式", 
        help_text='''
        说明：<br>
        1. 作业完成事件: completed<br>
        2. 表达式接受的逻辑运算符：or, and, not, in, >=, <=, >, <, ==, +, -, *, /, ^, ()<br>
        3. 字段名只允许由小写字母a~z，数字0~9和下划线_组成；字段值接受数字和字符，字符需要放在双引号中，如"A0101"
        ''')
    parameters = models.CharField(max_length=1024, blank=True, null=True, verbose_name="检查字段")
    fields = models.TextField(max_length=1024, blank=True, null=True, verbose_name="可用字段")

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "业务规则"
        verbose_name_plural = "业务规则"
        ordering = ['id']


# 指令表
class Instruction(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True, verbose_name="指令名称")
    label = models.CharField(max_length=255, blank=True, null=True, verbose_name="显示名称")
    code = models.CharField(max_length=10, verbose_name="指令代码")
    func = models.CharField(max_length=100, verbose_name="操作函数")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="指令描述")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "指令"
        verbose_name_plural = "指令"
        ordering = ['id']


# 事件指令程序表
class Event_instructions(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_index=True, verbose_name="事件")
    instruction = models.ForeignKey(Instruction, on_delete=models.CASCADE, verbose_name="指令")
    order = models.PositiveSmallIntegerField(default=1, verbose_name="指令序号")
    params = models.CharField(max_length=255, blank=True, null=True, verbose_name="创建作业")

    def __str__(self):
        return self.instruction.name

    class Meta:
        verbose_name = "事件指令集"
        verbose_name_plural = "事件指令集"
        ordering = ['event', 'order']


# 服务进程表 Service_proc
class Service_proc(models.Model):
	# 服务进程id: spid
	service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="服务")  # 服务id: sid
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, related_name='service_uid', verbose_name="服务专员")  # 作业人员id: uid
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name='service_cid', verbose_name="客户")  # 客户id: cid
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


# 作业进程表 Operation_proc
class Operation_proc(models.Model):
	# 作业进程id: pid
	operation = models.ForeignKey(Operation, on_delete=models.CASCADE, verbose_name="作业")  # 作业id: oid
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, related_name='operation_uid', verbose_name="操作员")  # 作业员id: uid
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name='operation_cid', verbose_name="客户")  # 客户id: cid
	group = models.ManyToManyField(Group, blank=True, verbose_name="角色组")  # 角色组：workgroup
	# 维护作业进程状态：
	'''
		作业状态机操作码
		('cre', 'CREATE'),					= 0
		('ctr', 'CREATED TO READY'),		= 1
		('rtr', 'READY TO RUNNING'),		= 2
		('rth', 'RUNNING TO HANGUP'),		= 3
		('htr', 'HANGUP TO READY'),			= 2
		('rtc', 'RUNNING TO COMPLETED'),	= 4
	'''
	# 作业状态: state
	Operation_proc_state = [
		(0, '创建'),
		(1, '就绪'),
		(2, '运行'),
		(3, '挂起'),
		(4, '结束'),
	]
	state = models.PositiveSmallIntegerField(choices=Operation_proc_state, verbose_name="作业状态")
	entry = models.CharField(max_length=250, blank=True, null=True, db_index=True, verbose_name="作业入口")  # 作业入口: operand/<int:id>/update_view
	ppid = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="父进程")  # 父作业进程id: ppid
	service_proc = models.ForeignKey(Service_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="服务进程")  # 服务进程id: spid
	form_slugs = models.JSONField(blank=True, null=True, verbose_name="表单索引")
	
	def __str__(self):
	# 	# return 作业名称-客户姓名
		# return f'{self.operation.name}-{self.user.username}-{self.customer.username}'
		return "%s - %s - %s" %(self.id, self.operation.label, self.customer.name)

	def get_absolute_url(self):
		# 返回作业入口url
		return self.entry

	class Meta:
		verbose_name = "作业进程"
		verbose_name_plural = "作业进程"
		ordering = ['id']
