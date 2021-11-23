from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from django.contrib.auth.models import Group, User

from time import time
from django.utils import timezone

from icpc.models import *
from dictionaries.enums import *
from core.models import Staff, Customer


def gen_slug(s):
    slug = slugify(s, allow_unicode=True)
    return slug + f'-{int(time())}'


class History_of_trauma(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	choose = models.CharField(max_length=60, blank=True, null=True, choices=ChooseEnum, verbose_name="选择")
	diseases_name = models.ForeignKey(Icpc5_evaluation_and_diagnoses, db_column="icpc_code", null=True, on_delete=models.SET_NULL, verbose_name="病名")
	date = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name="日期")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "外伤史"
		verbose_name_plural = "外伤史"
		ordering = []

	def get_absolute_url(self):
		return reverse("history_of_trauma_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("history_of_trauma_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("history_of_trauma_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Out_of_hospital_self_report_survey(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	symptom_list = models.TextField(max_length=1024, blank=True, null=True, verbose_name="症状")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "院外症状自述调查"
		verbose_name_plural = "院外症状自述调查"
		ordering = []

	def get_absolute_url(self):
		return reverse("out_of_hospital_self_report_survey_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("out_of_hospital_self_report_survey_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("out_of_hospital_self_report_survey_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Personal_comprehensive_psychological_quality_survey(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	personality_tendency = models.CharField(max_length=60, blank=True, null=True, verbose_name="性格倾向")
	is_life_fun = models.CharField(max_length=60, blank=True, null=True, choices=FrequencyEnum, verbose_name="您觉得生活有乐趣吗")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "个人心理综合素质调查"
		verbose_name_plural = "个人心理综合素质调查"
		ordering = []

	def get_absolute_url(self):
		return reverse("personal_comprehensive_psychological_quality_survey_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("personal_comprehensive_psychological_quality_survey_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("personal_comprehensive_psychological_quality_survey_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Personal_health_assessment(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	do_you_feel_healthy = models.CharField(max_length=60, blank=True, null=True, choices=Degree_expressionEnum, verbose_name="觉得自己身体健康吗")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "个人身体健康评估"
		verbose_name_plural = "个人身体健康评估"
		ordering = []

	def get_absolute_url(self):
		return reverse("personal_health_assessment_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("personal_health_assessment_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("personal_health_assessment_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Allergies_history(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	drug_name = models.CharField(max_length=60, blank=True, null=True, choices=Drug_listEnum, verbose_name="药品名称")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "过敏史"
		verbose_name_plural = "过敏史"
		ordering = []

	def get_absolute_url(self):
		return reverse("allergies_history_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("allergies_history_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("allergies_history_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Personal_health_behavior_survey(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	is_the_diet_regular = models.CharField(max_length=60, blank=True, null=True, choices=ChooseEnum, verbose_name="饮食是否规律")
	is_the_diet_proportion_healthy = models.CharField(max_length=60, blank=True, null=True, choices=ChooseEnum, verbose_name="饮食比例是否健康")
	whether_the_bowel_movements_are_regular = models.CharField(max_length=60, blank=True, null=True, choices=ChooseEnum, verbose_name="大便是否规律")
	whether_to_drink_alcohol = models.CharField(max_length=60, blank=True, null=True, choices=ChooseEnum, verbose_name="是否饮酒")
	drinking_frequency = models.CharField(max_length=60, blank=True, null=True, choices=FrequencyEnum, verbose_name="饮酒频次")
	do_you_smoke = models.CharField(max_length=60, blank=True, null=True, choices=FrequencyEnum, verbose_name="是否吸烟")
	smoking_frequency = models.CharField(max_length=60, blank=True, null=True, choices=FrequencyEnum, verbose_name="吸烟频次")
	average_sleep_duration = models.CharField(max_length=60, blank=True, null=True, verbose_name="平均睡眠时长")
	insomnia = models.CharField(max_length=60, blank=True, null=True, choices=ChooseEnum, verbose_name="有无失眠情况")
	duration_of_insomnia = models.CharField(max_length=60, blank=True, null=True, verbose_name="持续失眠时间")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "个人健康行为调查"
		verbose_name_plural = "个人健康行为调查"
		ordering = []

	def get_absolute_url(self):
		return reverse("personal_health_behavior_survey_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("personal_health_behavior_survey_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("personal_health_behavior_survey_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class History_of_blood_transfusion(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	date = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name="日期")
	blood_transfusion = models.SmallIntegerField(blank=True, null=True, verbose_name="输血量")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "输血史"
		verbose_name_plural = "输血史"
		ordering = []

	def get_absolute_url(self):
		return reverse("history_of_blood_transfusion_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("history_of_blood_transfusion_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("history_of_blood_transfusion_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Social_environment_assessment(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	is_the_living_environment_satisfactory = models.CharField(max_length=60, blank=True, null=True, choices=SatisfactionEnum, verbose_name="您对居住环境满意吗")
	is_the_transportation_convenient = models.CharField(max_length=60, blank=True, null=True, choices=Degree_expressionEnum, verbose_name="您所在的社区交通方便吗")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "社会环境评估"
		verbose_name_plural = "社会环境评估"
		ordering = []

	def get_absolute_url(self):
		return reverse("social_environment_assessment_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("social_environment_assessment_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("social_environment_assessment_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Medical_history(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	disease_name = models.ForeignKey(Icpc5_evaluation_and_diagnoses, db_column="icpc_code", null=True, on_delete=models.SET_NULL, verbose_name="疾病名称")
	time_of_diagnosis = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name="确诊时间")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "疾病史"
		verbose_name_plural = "疾病史"
		ordering = []

	def get_absolute_url(self):
		return reverse("medical_history_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("medical_history_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("medical_history_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Major_life_events(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	major_life = models.CharField(max_length=60, blank=True, null=True, choices=Life_eventEnum, verbose_name="生活事件")
	date = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name="日期")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "重大生活事件调查"
		verbose_name_plural = "重大生活事件调查"
		ordering = []

	def get_absolute_url(self):
		return reverse("major_life_events_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("major_life_events_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("major_life_events_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Physical_examination_vision(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	left_eye_vision = models.CharField(max_length=60, blank=True, null=True, verbose_name="左眼视力")
	right_eye_vision = models.CharField(max_length=60, blank=True, null=True, verbose_name="右眼视力")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "查体视力"
		verbose_name_plural = "查体视力"
		ordering = []

	def get_absolute_url(self):
		return reverse("physical_examination_vision_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("physical_examination_vision_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("physical_examination_vision_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Family_survey(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	diseases = models.ForeignKey(Icpc5_evaluation_and_diagnoses, db_column="icpc_code", null=True, on_delete=models.SET_NULL, verbose_name="病名")
	family_relationship = models.CharField(max_length=60, blank=True, null=True, choices=Family_relationshipEnum, verbose_name="家庭成员关系")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "家庭情况调查"
		verbose_name_plural = "家庭情况调查"
		ordering = []

	def get_absolute_url(self):
		return reverse("family_survey_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("family_survey_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("family_survey_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class History_of_surgery(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	name_of_operation = models.ForeignKey(Icpc7_treatments, db_column="icpc_code", null=True, on_delete=models.SET_NULL, verbose_name="手术名称")
	date = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name="日期")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "手术史"
		verbose_name_plural = "手术史"
		ordering = []

	def get_absolute_url(self):
		return reverse("history_of_surgery_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("history_of_surgery_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("history_of_surgery_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Blood_pressure_monitoring(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	systolic_blood_pressure = models.SmallIntegerField(blank=True, null=True, verbose_name="收缩压")
	diastolic_blood_pressure = models.SmallIntegerField(blank=True, null=True, verbose_name="舒张压")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "血压监测"
		verbose_name_plural = "血压监测"
		ordering = []

	def get_absolute_url(self):
		return reverse("blood_pressure_monitoring_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("blood_pressure_monitoring_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("blood_pressure_monitoring_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class User_registry(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	name = models.CharField(max_length=60, blank=True, null=True, verbose_name="姓名")
	gender = models.CharField(max_length=60, blank=True, null=True, verbose_name="性别")
	date_of_birth = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name="出生日期")
	age = models.CharField(max_length=60, blank=True, null=True, verbose_name="年龄")
	identification_number = models.CharField(max_length=60, blank=True, null=True, verbose_name="身份证号码")
	contact_information = models.CharField(max_length=60, blank=True, null=True, verbose_name="联系方式")
	contact_address = models.CharField(max_length=60, blank=True, null=True, verbose_name="联系地址")
	password_setting = models.CharField(max_length=60, blank=True, null=True, verbose_name="密码设置")
	confirm_password = models.CharField(max_length=60, blank=True, null=True, verbose_name="确认密码")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

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


class Doctor_registry(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
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
	expertise = models.CharField(max_length=60, blank=True, null=True, verbose_name="专长")
	practice_time = models.CharField(max_length=60, blank=True, null=True, verbose_name="执业时间")
	affiliation = models.CharField(max_length=60, blank=True, null=True, choices=Institutions_listEnum, verbose_name="所属机构")
	date_of_birth = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name="出生日期")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

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


class User_login(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	username = models.CharField(max_length=60, blank=True, null=True, verbose_name="用户名")
	password = models.CharField(max_length=60, blank=True, null=True, verbose_name="密码")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

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


class Doctor_login(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	service_role = models.CharField(max_length=60, blank=True, null=True, verbose_name="服务角色")
	username = models.CharField(max_length=60, blank=True, null=True, verbose_name="用户名")
	password = models.CharField(max_length=60, blank=True, null=True, verbose_name="密码")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

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


class Vital_signs_check(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	body_temperature = models.SmallIntegerField(blank=True, null=True, verbose_name="体温")
	pulse = models.SmallIntegerField(blank=True, null=True, verbose_name="脉搏")
	respiratory_rate = models.SmallIntegerField(blank=True, null=True, verbose_name="呼吸频率")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "生命体征检查"
		verbose_name_plural = "生命体征检查"
		ordering = []

	def get_absolute_url(self):
		return reverse("vital_signs_check_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("vital_signs_check_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("vital_signs_check_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Physical_examination_hearing(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	left_ear_hearing = models.CharField(max_length=60, blank=True, null=True, choices=HearingEnum, verbose_name="左耳听力")
	rightearhearing = models.CharField(max_length=60, blank=True, null=True, choices=HearingEnum, verbose_name="右耳听力")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "查体听力"
		verbose_name_plural = "查体听力"
		ordering = []

	def get_absolute_url(self):
		return reverse("physical_examination_hearing_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("physical_examination_hearing_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("physical_examination_hearing_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Basic_personal_information(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
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
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

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


class History_of_infectious_diseases(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	diseases = models.ForeignKey(Icpc5_evaluation_and_diagnoses, db_column="icpc_code", null=True, on_delete=models.SET_NULL, verbose_name="病名")
	family_relationship = models.CharField(max_length=60, blank=True, null=True, choices=Family_relationshipEnum, verbose_name="家庭成员关系")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

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


class Physical_examination(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	hight = models.SmallIntegerField(blank=True, null=True, verbose_name="身高")
	weight = models.SmallIntegerField(blank=True, null=True, verbose_name="体重")
	body_mass_index = models.SmallIntegerField(blank=True, null=True, verbose_name="体质指数")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "体格检查"
		verbose_name_plural = "体格检查"
		ordering = []

	def get_absolute_url(self):
		return reverse("physical_examination_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("physical_examination_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("physical_examination_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Personal_adaptability_assessment(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	do_you_feel_pressured_at_work = models.CharField(max_length=60, blank=True, null=True, choices=ChooseEnum, verbose_name="是否感觉到工作压力大")
	do_you_often_work_overtime = models.CharField(max_length=60, blank=True, null=True, choices=ChooseEnum, verbose_name="是否经常加班")
	working_hours_per_day = models.TextField(max_length=1024, blank=True, null=True, verbose_name="每天工作及工作往返总时长")
	are_you_satisfied_with_the_job = models.CharField(max_length=60, blank=True, null=True, choices=SatisfactionEnum, verbose_name="对目前生活和工作满意吗")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "个人适应能力评估"
		verbose_name_plural = "个人适应能力评估"
		ordering = []

	def get_absolute_url(self):
		return reverse("personal_adaptability_assessment_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("personal_adaptability_assessment_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("personal_adaptability_assessment_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Physical_examination_abdomen(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	tenderness = models.CharField(max_length=60, blank=True, null=True, choices=ChooseEnum, verbose_name="压痛")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "查体腹部"
		verbose_name_plural = "查体腹部"
		ordering = []

	def get_absolute_url(self):
		return reverse("physical_examination_abdomen_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("physical_examination_abdomen_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("physical_examination_abdomen_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Physical_examination_athletic_ability(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	athletic_ability = models.CharField(max_length=60, blank=True, null=True, choices=Athletic_abilityEnum, verbose_name="运动能力")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "查体运动能力"
		verbose_name_plural = "查体运动能力"
		ordering = []

	def get_absolute_url(self):
		return reverse("physical_examination_athletic_ability_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("physical_examination_athletic_ability_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("physical_examination_athletic_ability_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Physical_examination_oral_cavity(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	lips = models.CharField(max_length=60, blank=True, null=True, choices=LipsEnum, verbose_name="口唇")
	dentition = models.CharField(max_length=60, blank=True, null=True, choices=DentitionEnum, verbose_name="齿列")
	pharynx = models.CharField(max_length=60, blank=True, null=True, choices=PharynxEnum, verbose_name="咽部")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "查体口腔"
		verbose_name_plural = "查体口腔"
		ordering = []

	def get_absolute_url(self):
		return reverse("physical_examination_oral_cavity_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("physical_examination_oral_cavity_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("physical_examination_oral_cavity_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Physical_examination_lungs(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	barrel_chest = models.CharField(max_length=60, blank=True, null=True, choices=ChooseEnum, verbose_name="桶状胸")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "查体肺部"
		verbose_name_plural = "查体肺部"
		ordering = []

	def get_absolute_url(self):
		return reverse("physical_examination_lungs_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("physical_examination_lungs_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("physical_examination_lungs_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Physical_examination_limbs(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "查体四肢"
		verbose_name_plural = "查体四肢"
		ordering = []

	def get_absolute_url(self):
		return reverse("physical_examination_limbs_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("physical_examination_limbs_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("physical_examination_limbs_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Physical_examination_skin(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	skin = models.ForeignKey(Icpc3_symptoms_and_problems, db_column="icpc_code", null=True, on_delete=models.SET_NULL, verbose_name="皮肤")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "查体皮肤"
		verbose_name_plural = "查体皮肤"
		ordering = []

	def get_absolute_url(self):
		return reverse("physical_examination_skin_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("physical_examination_skin_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("physical_examination_skin_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Physical_examination_sclera(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	sclera = models.ForeignKey(Icpc3_symptoms_and_problems, db_column="icpc_code", null=True, on_delete=models.SET_NULL, verbose_name="巩膜")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "查体巩膜"
		verbose_name_plural = "查体巩膜"
		ordering = []

	def get_absolute_url(self):
		return reverse("physical_examination_sclera_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("physical_examination_sclera_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("physical_examination_sclera_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Physical_examination_lymph_nodes(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	lymph_nodes = models.ForeignKey(Icpc3_symptoms_and_problems, db_column="icpc_code", null=True, on_delete=models.SET_NULL, verbose_name="淋巴结")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "查体淋巴结"
		verbose_name_plural = "查体淋巴结"
		ordering = []

	def get_absolute_url(self):
		return reverse("physical_examination_lymph_nodes_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("physical_examination_lymph_nodes_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("physical_examination_lymph_nodes_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Physical_examination_spine(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "查体脊柱"
		verbose_name_plural = "查体脊柱"
		ordering = []

	def get_absolute_url(self):
		return reverse("physical_examination_spine_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("physical_examination_spine_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("physical_examination_spine_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Dorsal_artery_pulsation_examination(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	left_foot = models.CharField(max_length=60, blank=True, null=True, choices=Dorsal_artery_pulsationEnum, verbose_name="左脚")
	right_foot = models.CharField(max_length=60, blank=True, null=True, choices=Dorsal_artery_pulsationEnum, verbose_name="右脚")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "足背动脉搏动检查"
		verbose_name_plural = "足背动脉搏动检查"
		ordering = []

	def get_absolute_url(self):
		return reverse("dorsal_artery_pulsation_examination_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("dorsal_artery_pulsation_examination_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("dorsal_artery_pulsation_examination_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Routine_blood_test(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	wbc = models.SmallIntegerField(blank=True, null=True, verbose_name="白细胞")
	rbc = models.SmallIntegerField(blank=True, null=True, verbose_name="红细胞")
	hgb = models.SmallIntegerField(blank=True, null=True, verbose_name="血红蛋白")
	hct = models.SmallIntegerField(blank=True, null=True, verbose_name="红细胞压积")
	mcv = models.SmallIntegerField(blank=True, null=True, verbose_name="红细胞平均体积")
	mch = models.SmallIntegerField(blank=True, null=True, verbose_name="平均血红蛋白量")
	mcmc = models.SmallIntegerField(blank=True, null=True, verbose_name="平均血红蛋白浓度")
	plt = models.SmallIntegerField(blank=True, null=True, verbose_name="血小板")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "血常规化验"
		verbose_name_plural = "血常规化验"
		ordering = []

	def get_absolute_url(self):
		return reverse("routine_blood_test_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("routine_blood_test_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("routine_blood_test_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Fundus_examination(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	fundus = models.CharField(max_length=60, blank=True, null=True, choices=NormalityEnum, verbose_name="眼底")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "眼底检查"
		verbose_name_plural = "眼底检查"
		ordering = []

	def get_absolute_url(self):
		return reverse("fundus_examination_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("fundus_examination_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("fundus_examination_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)


class Lower_extremity_edema_examination(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
	lower_extremity_edema = models.CharField(max_length=60, blank=True, null=True, choices=EdemaEnum, verbose_name="下肢水肿")
	operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
	slug = models.SlugField(max_length=150, blank=True)

	def __str__(self):
		return str(self.customer)

	class Meta:
		verbose_name = "下肢水肿检查"
		verbose_name_plural = "下肢水肿检查"
		ordering = []

	def get_absolute_url(self):
		return reverse("lower_extremity_edema_examination_detail_url", kwargs={"slug":self.slug})

	def get_update_url(self):
		return reverse("lower_extremity_edema_examination_update_url", kwargs={"slug":self.slug})

	def get_delete_url(self):
		return reverse("lower_extremity_edema_examination_delete_url", kwargs={"slug":self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self._meta.model_name)
		super().save(*args, **kwargs)