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


class User_registry(models.Model):
	name = models.CharField(max_length=60, blank=True, null=True, verbose_name="姓名")
	gender = models.CharField(max_length=60, blank=True, null=True, verbose_name="性别")
	age = models.CharField(max_length=60, blank=True, null=True, verbose_name="年龄")
	identification_number = models.CharField(max_length=60, blank=True, null=True, verbose_name="身份证号码")
	contact_information = models.CharField(max_length=60, blank=True, null=True, verbose_name="联系方式")
	contact_address = models.CharField(max_length=60, blank=True, null=True, verbose_name="联系地址")
	password_setting = models.CharField(max_length=60, blank=True, null=True, verbose_name="密码设置")
	confirm_password = models.CharField(max_length=60, blank=True, null=True, verbose_name="确认密码")
	slug = models.SlugField(max_length=150, unique=True, blank=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "用户注册表"
		verbose_name_plural = "用户注册表"
		ordering = []

	def get_absolute_url(self):
		return reverse("user_registry_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("user_registry_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("user_registry_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Doctor_login(models.Model):
	service_role = models.CharField(max_length=60, blank=True, null=True, verbose_name="服务角色")
	username = models.CharField(max_length=60, blank=True, null=True, verbose_name="用户名")
	password = models.CharField(max_length=60, blank=True, null=True, verbose_name="密码")
	slug = models.SlugField(max_length=150, unique=True, blank=True)

	def __str__(self):
		return self.service_role

	class Meta:
		verbose_name = "医生登陆"
		verbose_name_plural = "医生登陆"
		ordering = []

	def get_absolute_url(self):
		return reverse("doctor_login_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("doctor_login_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("doctor_login_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class User_login(models.Model):
	username = models.CharField(max_length=60, blank=True, null=True, verbose_name="用户名")
	password = models.CharField(max_length=60, blank=True, null=True, verbose_name="密码")
	slug = models.SlugField(max_length=150, unique=True, blank=True)

	def __str__(self):
		return self.username

	class Meta:
		verbose_name = "用户登录"
		verbose_name_plural = "用户登录"
		ordering = []

	def get_absolute_url(self):
		return reverse("user_login_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("user_login_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("user_login_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Doctor_registry(models.Model):
	name = models.CharField(max_length=60, blank=True, null=True, verbose_name="姓名")
	gender = models.CharField(max_length=60, blank=True, null=True, verbose_name="性别")
	age = models.CharField(max_length=60, blank=True, null=True, verbose_name="年龄")
	identification_number = models.CharField(max_length=60, blank=True, null=True, verbose_name="身份证号码")
	contact_information = models.CharField(max_length=60, blank=True, null=True, verbose_name="联系电话")
	contact_address = models.CharField(max_length=60, blank=True, null=True, verbose_name="联系地址")
	service_role = models.CharField(max_length=60, blank=True, null=True, choices=Service_roleEnum, verbose_name="服务角色")
	practice_qualification = models.CharField(max_length=60, blank=True, null=True, verbose_name="执业资质")
	password_setting = models.CharField(max_length=60, blank=True, null=True, verbose_name="密码设置")
	confirm_password = models.CharField(max_length=60, blank=True, null=True, verbose_name="确认密码")
	slug = models.SlugField(max_length=150, unique=True, blank=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "医生注册"
		verbose_name_plural = "医生注册"
		ordering = []

	def get_absolute_url(self):
		return reverse("doctor_registry_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("doctor_registry_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("doctor_registry_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)




class Basic_personal_information(models.Model):
	family_id = models.ForeignKey(Icpc1_register_logins, db_column="icpc_code", null=True, on_delete=models.SET_NULL, verbose_name="家庭编号")
	family_relationship = models.CharField(max_length=60, blank=True, null=True, choices=Family_relationshipEnum, verbose_name="家庭成员关系")
	resident_file_number = models.CharField(max_length=60, blank=True, null=True, verbose_name="居民档案号")
	name = models.CharField(max_length=60, blank=True, null=True, verbose_name="姓名")
	gender = models.CharField(max_length=60, blank=True, null=True, choices=GenderEnum, verbose_name="性别")
	date_of_birth = models.DateField(blank=True, null=True, default=timezone.now, verbose_name="出生日期")
	nationality = models.CharField(max_length=60, blank=True, null=True, choices=NationalityEnum, verbose_name="民族")
	marital_status = models.CharField(max_length=60, blank=True, null=True, choices=Marital_statusEnum, verbose_name="婚姻状况")
	education = models.CharField(max_length=60, blank=True, null=True, choices=EducationEnum, verbose_name="文化程度")
	occupational_status = models.CharField(max_length=60, blank=True, null=True, choices=Occupational_statusEnum, verbose_name="职业状况")
	identification_number = models.CharField(max_length=60, blank=True, null=True, verbose_name="身份证号码")
	family_address = models.CharField(max_length=60, blank=True, null=True, verbose_name="家庭地址")
	contact_number = models.CharField(max_length=60, blank=True, null=True, verbose_name="联系电话")
	medical_ic_card_number = models.CharField(max_length=60, blank=True, null=True, verbose_name="医疗ic卡号")
	medical_expenses_burden = models.CharField(max_length=60, blank=True, null=True, choices=Medical_expenses_burdenEnum, verbose_name="医疗费用负担")
	type_of_residence = models.CharField(max_length=60, blank=True, null=True, choices=Type_of_residenceEnum, verbose_name="居住类型")
	blood_type = models.CharField(max_length=60, blank=True, null=True, choices=Blood_typeEnum, verbose_name="血型")
	contract_signatory = models.CharField(max_length=60, blank=True, null=True, choices=Contract_signatoryEnum, verbose_name="合同签约户")
	signed_family_doctor = models.CharField(max_length=60, blank=True, null=True, choices=Employee_listEnum, verbose_name="签约家庭医生")
	slug = models.SlugField(max_length=150, unique=True, blank=True)

	def __str__(self):
		return self.family_id

	class Meta:
		verbose_name = "个人基本情况"
		verbose_name_plural = "个人基本情况"
		ordering = []

	def get_absolute_url(self):
		return reverse("basic_personal_information_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("basic_personal_information_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("basic_personal_information_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Family_history(models.Model):
	diseases = models.ForeignKey(Icpc5_evaluation_and_diagnoses, db_column="icpc_code", null=True, on_delete=models.SET_NULL, verbose_name="病名")
	family_relationship = models.CharField(max_length=60, blank=True, null=True, choices=Family_relationshipEnum, verbose_name="家庭成员关系")
	slug = models.SlugField(max_length=150, unique=True, blank=True)

	def __str__(self):
		return self.diseases

	class Meta:
		verbose_name = "家族病史"
		verbose_name_plural = "家族病史"
		ordering = []

	def get_absolute_url(self):
		return reverse("family_history_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("family_history_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("family_history_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class History_of_infectious_diseases(models.Model):
	diseases = models.ForeignKey(Icpc5_evaluation_and_diagnoses, db_column="icpc_code", null=True, on_delete=models.SET_NULL, verbose_name="病名")
	slug = models.SlugField(max_length=150, unique=True, blank=True)

	def __str__(self):
		return self.diseases

	class Meta:
		verbose_name = "遗传病史"
		verbose_name_plural = "遗传病史"
		ordering = []

	def get_absolute_url(self):
		return reverse("history_of_infectious_diseases_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("history_of_infectious_diseases_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("history_of_infectious_diseases_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)