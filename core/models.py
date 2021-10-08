from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User, Group
from icpc.models import Icpc

'''
作业状态机：

const operationMachine = createMachine<Context>({
  id: "operation",
  initial: "created",
  context: {
    retries: 0,
  },
  states: {
    created: {
      on: {
        RESOURCES_AVAILABLE: "ready",
      },
    },
    ready: {
      on: {
        USER_ENTERED: "running",
      },
    },
    running: {
      on: {
        FORM_SAVED: "finished",
        HANG_UP: "hangup",
      },
    },
    hangup: {
      on: {
        RECOVER: "ready",
      },
    },
    finished: {
      type: "final",
    },
  },
});

'''

# 表单信息表
class Form(models.Model):
	name = models.CharField(max_length=255, verbose_name="表单名称")
	label = models.CharField(max_length=255, verbose_name="显示名称")
	input_style = [
		(0, '详情'),
		(1, '列表'),
	]
	style = models.PositiveSmallIntegerField(choices=input_style, default=0, verbose_name='风格')

	def __str__(self):
		return str(self.label)

	class Meta:
		verbose_name = "表单"
		verbose_name_plural = "表单"
		ordering = ['id']


# 基础作业信息表
class Operation(models.Model):
	name = models.CharField(max_length=255, verbose_name="作业名称")
	icpc = models.OneToOneField(Icpc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="ICPC")
	Operation_priority = [
		(0, '0级'),
		(1, '紧急'),
		(2, '优先'),
		(3, '一般'),
	]
	priority = models.PositiveSmallIntegerField(choices=Operation_priority, default=3, verbose_name='优先级')
	forms = models.ManyToManyField(Form, verbose_name="表单")
	entry = models.CharField(max_length=250, blank=True, null=True, verbose_name="作业入口")
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
		return str(self.name)

	class Meta:
		verbose_name = "作业"
		verbose_name_plural = "作业"
		ordering = ['id']


# 服务类型信息表
class Service(models.Model):
	name = models.CharField(max_length=255, verbose_name="服务名称")
	icpc = models.OneToOneField(Icpc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="ICPC")
	first_operation = models.ForeignKey(Operation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="起始作业")
	
	def __str__(self):
		return str(self.name)

	class Meta:
		verbose_name = "服务"
		verbose_name_plural = "服务"
		ordering = ['id']


# 作业事件表
class Event(models.Model):
	operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name='from_oid', verbose_name="上道作业")
	name = models.CharField(max_length=255, verbose_name="事件名称")
	next = models.ManyToManyField(Operation, verbose_name="后续作业")
	rule = models.CharField(max_length=255, blank=True, null=True, verbose_name="规则描述")

	def __str__(self):
		return str(self.name)

	class Meta:
		verbose_name = "事件"
		verbose_name_plural = "事件"
		ordering = ['id']


# 指令表
class Instruction(models.Model):
	name = models.CharField(max_length=100, verbose_name="指令名称")
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
	event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="事件")
	instruction = models.ForeignKey(Instruction, on_delete=models.CASCADE, verbose_name="指令")
	order = models.PositiveSmallIntegerField(default=1, verbose_name="指令序号")
	params = models.PositiveIntegerField(blank=True, null=True, verbose_name="创建作业")

	def __str__(self):
		return str(self.instruction.name)

	class Meta:
		verbose_name = "事件指令集"
		verbose_name_plural = "事件指令集"
		ordering = ['event', 'order']


# 服务进程表 Service_proc
class Service_proc(models.Model):
	# 服务进程id: spid
	# id 
	
	# 服务id: sid
	service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="服务")
	
	# 服务专员id: uid
	user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='service_uid', verbose_name="服务专员")
	
	# 客户id: cid
	customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='service_cid', verbose_name="客户")
	
	# 工作小组：workgroup
	# workgroup = models.ForeignKey('Workgroup', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="工作组")
	
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
	
	# 作业id: oid
	operation = models.ForeignKey(Operation, on_delete=models.CASCADE, verbose_name="作业id")
	
	# 作业员id: uid
	user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='operation_uid', verbose_name="操作员id")
	
	# 客户id: cid
	customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='operation_cid', verbose_name="客户id")
	
	# 作业状态: state
	Operation_proc_state = [
		(0, '创建'),
		(1, '就绪'),
		(2, '运行'),
		(3, '挂起'),
		(4, '结束'),
	]
	state = models.PositiveSmallIntegerField(choices=Operation_proc_state, verbose_name="作业状态")
	
	# 作业入口
	entry = models.CharField(max_length=250, blank=True, null=True, verbose_name="作业入口")

	# 父作业进程id: ppid
	ppid = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="父进程id")

	# 服务进程id: spid
	service_proc = models.ForeignKey(Service_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="服务id")
	
	def __str__(self):
	# 	# return 作业名称-操作员姓名-客户姓名
		# return f'{self.operation.name}-{self.user.username}-{self.customer.username}'
		return "%s - %s - %s" %(self.operation.name, self.user.username, self.customer.username)

	def get_absolute_url(self):
		# 返回作业入口url
		return self.operation.entry

	class Meta:
		verbose_name = "作业进程"
		verbose_name_plural = "作业进程"
		ordering = ['id']
