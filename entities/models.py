from django.db import models
from django.forms import CharField

class Medicine(models.Model):
	name = models.CharField(max_length=255, verbose_name="药品名称")
	label = models.CharField(max_length=255, blank=True, null=True, verbose_name="显示名称")

	def __str__(self):
		return self.label

	class Meta:
		verbose_name = "药品"
		verbose_name_plural = "药品"
		ordering = ['id']


class Institution(models.Model):
	name = models.CharField(max_length=255, verbose_name="机构名称")
	label = models.CharField(max_length=255, blank=True, null=True, verbose_name="显示名称")

	def __str__(self):
		return self.label

	class Meta:
		verbose_name = "机构"
		verbose_name_plural = "机构"
		ordering = ['id']
