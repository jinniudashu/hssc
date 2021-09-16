from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from time import time
from django.utils import timezone

def gen_slug(s):
    slug = slugify(s, allow_unicode=True)
    return slug + f'-{int(time())}'


# 业务事件字典
class Event(models.Model):
	pass


# 基础作业信息表
class Operation(models.Model):
	pass


# 服务信息表
class Service(models.Model):
	pass


# 作业指令表
class Instruction(models.Model):
	pass


# 作业进程表 Operation_proc
class Operation_proc(models.Model):
	name = models.CharField(max_length=60, blank=True, null=True, verbose_name="名称")
	slug = models.SlugField(max_length=150, unique=True, blank=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "作业进程表"
		verbose_name_plural = "作业进程表"
		ordering = ['id']

	def get_absolute_url(self):
		# return 作业入口url
		return reverse("user_registry_detail_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


# 服务进程表 Service_proc
class Service_proc(models.Model):
	pass
