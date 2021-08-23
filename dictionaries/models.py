from django.db import models

# Create your models here.



class Nation(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "民族"
		verbose_name_plural = "民族"


class Diabetes_symptoms(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "糖尿病症状"
		verbose_name_plural = "糖尿病症状"


class Prescription(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "处方单"
		verbose_name_plural = "处方单"


class Dorsal_artery_pulsation(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "足背动脉搏动"
		verbose_name_plural = "足背动脉搏动"


class Diploma_level(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "文化程度"
		verbose_name_plural = "文化程度"


class Adverse_reactions(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "不良反应"
		verbose_name_plural = "不良反应"


class Career(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "职业"
		verbose_name_plural = "职业"


class Complianc_behavior(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "遵医行为"
		verbose_name_plural = "遵医行为"


class Marriage(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "婚姻"
		verbose_name_plural = "婚姻"


class Payment_method(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "支付方式"
		verbose_name_plural = "支付方式"


class Allergy_drugs(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "过敏药物"
		verbose_name_plural = "过敏药物"


class Follow_up_method(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "随访方式"
		verbose_name_plural = "随访方式"


class Psychological_guidance(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "心理指导"
		verbose_name_plural = "心理指导"


class Follow_up_classification(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "随访分类"
		verbose_name_plural = "随访分类"


class Reason_previous_transfusion(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "既往输血原因"
		verbose_name_plural = "既往输血原因"


class Kinship(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "亲属关系"
		verbose_name_plural = "亲属关系"


class Hereditary_disease(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "遗传性疾病"
		verbose_name_plural = "遗传性疾病"


class Inspection_item(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "检查项目"
		verbose_name_plural = "检查项目"


class Surver_items(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "调查项目"
		verbose_name_plural = "调查项目"


class Compliance(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "依从性"
		verbose_name_plural = "依从性"


class Hypoglycemic_response(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "低血糖反应"
		verbose_name_plural = "低血糖反应"


class Blood_group(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "血型"
		verbose_name_plural = "血型"


class Gender(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "性别"
		verbose_name_plural = "性别"


class Resident_type(models.Model):
	name = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")
	score = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "户籍类型"
		verbose_name_plural = "户籍类型"