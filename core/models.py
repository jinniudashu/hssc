from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
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


# 服务类型信息表
class Service(models.Model):
	name = models.CharField(max_length=255, verbose_name="服务类型名称")
	icpc = models.OneToOneField(Icpc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="ICPC")	
	init_operation = models.ForeignKey('Operation', on_delete=CASCADE, blank=True, null=True, related_name='init_oid', verbose_name="初始作业")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "服务"
		verbose_name_plural = "服务"
		ordering = ['id']


# 基础作业信息表
class Operation(models.Model):
	name = models.CharField(max_length=255, verbose_name="作业名称")
	icpc = models.OneToOneField(Icpc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="ICPC")
	entry = models.CharField(max_length=250, blank=True, null=True, verbose_name="作业入口")
	service = models.ManyToManyField(Service, verbose_name="服务类型")
	group = models.ManyToManyField(Group, verbose_name="作业角色")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "作业"
		verbose_name_plural = "作业"
		ordering = ['id']


# 业务事件字典
class Event(models.Model):
	name = models.CharField(max_length=255, verbose_name="事件名称")
	icpc = models.OneToOneField(Icpc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="ICPC")
	operation = models.ForeignKey(Operation, on_delete=models.CASCADE, verbose_name="事件来源")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "业务事件"
		verbose_name_plural = "业务事件"
		ordering = ['id']


# 作业指令集
class Instruction(models.Model):
	service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="服务类型")
	event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="事件代码")
	next = models.ForeignKey(Operation, on_delete=models.CASCADE, verbose_name="下一项作业")

	class Meta:
		verbose_name = "作业指令"
		verbose_name_plural = "作业指令"
		ordering = ['id']


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
	
	# 当前作业进程: oid
	# current_operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name='oid', verbose_name="当前作业")

	# 工作小组：workgroup
	# workgroup = models.ForeignKey('Workgroup', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="工作组")
	
	def __str__(self):
		# return 服务名称-服务进程号spid
		return f'{self.service.name}-{str(self.id)}'

	# def get_absolute_url(self):
	# 	# 返回作业入口url
	# 	return self.operation.entry

	class Meta:
		verbose_name = "服务进程"
		verbose_name_plural = "服务进程"
		ordering = ['id']


# 作业进程表 Operation_proc
class Operation_proc(models.Model):
	# 作业进程id: opid
	# id 
	
	# 服务进程id: spid
	service_proc = models.ForeignKey(Service_proc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="服务id")
	
	# 作业id: oid
	operation = models.ForeignKey(Operation, on_delete=models.CASCADE, verbose_name="作业id")
	
	# 作业员id: uid
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='operation_uid', verbose_name="操作员id")
	
	# 客户id: cid
	customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='operation_cid', verbose_name="客户id")
	
	# 作业状态: state
	Operation_proc_state = [
		(0, '创建'),
		(1, '就绪'),
		(2, '运行'),
		(3, '挂起'),
		(4, '结束'),
	]
	state = models.SmallIntegerField(choices=Operation_proc_state, verbose_name="作业状态")
	
	# 父作业进程id: ppid
	ppid = models.IntegerField(blank=True, null=True, verbose_name="父进程id")

	def __str__(self):
		# return 作业名称-操作员姓名-客户姓名
		return f'{self.operation.name}-{self.user.username}-{self.customer.username}'

	def get_absolute_url(self):
		# 返回作业入口url
		return self.operation.entry

	class Meta:
		verbose_name = "作业进程"
		verbose_name_plural = "作业进程"
		ordering = ['id']
