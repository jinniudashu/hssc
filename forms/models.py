from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from time import time
from django.utils import timezone

from icpc.models import *
from dictionaries.enums import *

def gen_slug(s):
    slug = slugify(s, allow_unicode=True)
    return slug + f'-{int(time())}'


class Metadata_follow_up_form(models.Model):
	name = models.CharField(max_length=60, blank=True, null=True, verbose_name="姓名")
	serial_number = models.CharField(max_length=60, blank=True, null=True, verbose_name="编号")
	method = models.ForeignKey(Icpc2_reservation_investigations, db_column="icpc_code", null=True, on_delete=models.SET_NULL, verbose_name="随访方式")
	classification = models.CharField(max_length=60, blank=True, null=True, choices=Follow_up_classificationEnum, verbose_name="随访分类")
	opinion = models.TextField(max_length=1024, blank=True, null=True, verbose_name="随访意见")
	agency = models.CharField(max_length=60, blank=True, null=True, verbose_name="随访机构")
	doctor_signature = models.CharField(max_length=60, blank=True, null=True, verbose_name="随访医生签名")
	date = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name="随访日期")
	next_date = models.DateField(blank=True, null=True, default=timezone.now, verbose_name="下次随访日期")
	slug = models.SlugField(max_length=150, unique=True, blank=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "通用随访表"
		verbose_name_plural = "通用随访表"
		ordering = []

	def get_absolute_url(self):
		return reverse("metadata_follow_up_form_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("metadata_follow_up_form_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("metadata_follow_up_form_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Classification_checklist(models.Model):
	inspection_item = models.CharField(max_length=60, blank=True, null=True, choices=Inspection_itemEnum, verbose_name="检查项目")
	slug = models.SlugField(max_length=150, unique=True, blank=True)

	def __str__(self):
		return self.inspection_item

	class Meta:
		verbose_name = "血液检查"
		verbose_name_plural = "血液检查"
		ordering = []

	def get_absolute_url(self):
		return reverse("classification_checklist_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("classification_checklist_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("classification_checklist_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Routine_physical_examination(models.Model):
	name = models.CharField(max_length=60, blank=True, null=True, verbose_name="姓名")
	gender = models.CharField(max_length=60, blank=True, null=True, choices=GenderEnum, verbose_name="性别")
	age = models.SmallIntegerField(blank=True, null=True, verbose_name="年龄")
	height = models.CharField(max_length=60, blank=True, null=True, verbose_name="身高")
	weight = models.CharField(max_length=60, blank=True, null=True, verbose_name="体重")
	bmi = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="体质指数")
	test_comments = models.ForeignKey(Icpc5_evaluation_and_diagnoses, db_column="icpc_code", null=True, on_delete=models.SET_NULL, verbose_name="评估意见")
	slug = models.SlugField(max_length=150, unique=True, blank=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "常规体格检查表"
		verbose_name_plural = "常规体格检查表"
		ordering = []

	def get_absolute_url(self):
		return reverse("routine_physical_examination_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("routine_physical_examination_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("routine_physical_examination_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Classification_survey_list(models.Model):
	surver_items = models.CharField(max_length=60, blank=True, null=True, choices=Surver_itemsEnum, verbose_name="调查项目")
	slug = models.SlugField(max_length=150, unique=True, blank=True)

	def __str__(self):
		return self.surver_items

	class Meta:
		verbose_name = "调查分类清单"
		verbose_name_plural = "调查分类清单"
		ordering = []

	def get_absolute_url(self):
		return reverse("classification_survey_list_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("classification_survey_list_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("classification_survey_list_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)