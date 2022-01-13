from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from time import time
from datetime import date
from django.utils import timezone

from icpc.models import *
from dictionaries.models import *
from core.models import Staff, Customer, Operation_proc

class Allergies_history(models.Model):
    relatedfield_drug_name = models.ForeignKey(Drug_list, related_name='drug_list_for_relatedfield_drug_name_allergies_history', on_delete=models.CASCADE, null=True, blank=True, verbose_name='药品名称')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '过敏史'
        verbose_name_plural = '过敏史'

    def get_absolute_url(self):
        return reverse('allergies_history_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('allergies_history_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('allergies_history_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Out_of_hospital_self_report_survey(models.Model):
    relatedfield_symptom_list = models.ForeignKey(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_relatedfield_symptom_list_out_of_hospital_self_report_survey', on_delete=models.CASCADE, null=True, blank=True, verbose_name='症状')
    characterfield_supplementary_description_of_the_condition = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '院外症状自述调查'
        verbose_name_plural = '院外症状自述调查'

    def get_absolute_url(self):
        return reverse('out_of_hospital_self_report_survey_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('out_of_hospital_self_report_survey_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('out_of_hospital_self_report_survey_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Personal_comprehensive_psychological_quality_survey(models.Model):
    relatedfield_personality_tendency = models.ForeignKey(Character, related_name='character_for_relatedfield_personality_tendency_personal_comprehensive_psychological_quality_survey', on_delete=models.CASCADE, null=True, blank=True, verbose_name='性格倾向')
    boolfield_is_life_fun = models.BooleanField(null=True, blank=True, verbose_name='您觉得生活是否有乐趣吗')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '个人心理综合素质调查'
        verbose_name_plural = '个人心理综合素质调查'

    def get_absolute_url(self):
        return reverse('personal_comprehensive_psychological_quality_survey_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('personal_comprehensive_psychological_quality_survey_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('personal_comprehensive_psychological_quality_survey_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Personal_adaptability_assessment(models.Model):
    boolfield_do_you_feel_pressured_at_work = models.BooleanField(null=True, blank=True, verbose_name='是否感觉到工作压力大')
    boolfield_do_you_often_work_overtime = models.BooleanField(null=True, blank=True, verbose_name='是否经常加班')
    characterfield_working_hours_per_day = models.TextField(max_length=255, null=True, blank=True, verbose_name='每天工作及工作往返总时长')
    relatedfield_are_you_satisfied_with_the_job_and_life = models.ForeignKey(Satisfaction, related_name='satisfaction_for_relatedfield_are_you_satisfied_with_the_job_and_life_personal_adaptability_assessment', on_delete=models.CASCADE, null=True, blank=True, verbose_name='对目前生活和工作满意吗')
    relatedfield_are_you_satisfied_with_your_adaptability = models.ForeignKey(Satisfaction, related_name='satisfaction_for_relatedfield_are_you_satisfied_with_your_adaptability_personal_adaptability_assessment', on_delete=models.CASCADE, null=True, blank=True, verbose_name='对自己的适应能力满意吗')
    relatedfield_can_you_get_encouragement_and_support_from_family_and_friends = models.ForeignKey(Frequency, related_name='frequency_for_relatedfield_can_you_get_encouragement_and_support_from_family_and_friends_personal_adaptability_assessment', on_delete=models.CASCADE, null=True, blank=True, verbose_name='是否能得到家人朋友的鼓励和支持')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '个人适应能力评估'
        verbose_name_plural = '个人适应能力评估'

    def get_absolute_url(self):
        return reverse('personal_adaptability_assessment_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('personal_adaptability_assessment_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('personal_adaptability_assessment_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Personal_health_behavior_survey(models.Model):
    boolfield_is_the_diet_regular = models.BooleanField(null=True, blank=True, verbose_name='饮食是否规律')
    boolfield_is_the_diet_proportion_healthy = models.BooleanField(null=True, blank=True, verbose_name='饮食比例是否健康')
    boolfield_whether_the_bowel_movements_are_regular = models.BooleanField(null=True, blank=True, verbose_name='大便是否规律')
    boolfield_whether_to_drink_alcohol = models.BooleanField(null=True, blank=True, verbose_name='是否饮酒')
    relatedfield_drinking_frequency = models.ForeignKey(Frequency, related_name='frequency_for_relatedfield_drinking_frequency_personal_health_behavior_survey', on_delete=models.CASCADE, null=True, blank=True, verbose_name='饮酒频次')
    boolfield_do_you_smoke = models.BooleanField(null=True, blank=True, verbose_name='是否吸烟')
    relatedfield_smoking_frequency = models.ForeignKey(Frequency, related_name='frequency_for_relatedfield_smoking_frequency_personal_health_behavior_survey', on_delete=models.CASCADE, null=True, blank=True, verbose_name='吸烟频次')
    characterfield_average_sleep_duration = models.CharField(max_length=255, null=True, blank=True, verbose_name='平均睡眠时长')
    boolfield_insomnia = models.BooleanField(null=True, blank=True, verbose_name='是否有失眠情况')
    characterfield_duration_of_insomnia = models.CharField(max_length=255, null=True, blank=True, verbose_name='持续失眠时间')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '个人健康行为调查'
        verbose_name_plural = '个人健康行为调查'

    def get_absolute_url(self):
        return reverse('personal_health_behavior_survey_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('personal_health_behavior_survey_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('personal_health_behavior_survey_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Personal_health_assessment(models.Model):
    relatedfield_own_health = models.ForeignKey(State_degree, related_name='state_degree_for_relatedfield_own_health_personal_health_assessment', on_delete=models.CASCADE, null=True, blank=True, verbose_name='觉得自身健康状况如何')
    relatedfield_compared_to_last_year = models.ForeignKey(Comparative_expression, related_name='comparative_expression_for_relatedfield_compared_to_last_year_personal_health_assessment', on_delete=models.CASCADE, null=True, blank=True, verbose_name='较之过去一年状态如何')
    relatedfield_sports_preference = models.ForeignKey(Sports_preference, related_name='sports_preference_for_relatedfield_sports_preference_personal_health_assessment', on_delete=models.CASCADE, null=True, blank=True, verbose_name='运动偏好')
    relatedfield_exercise_time = models.ForeignKey(Exercise_time, related_name='exercise_time_for_relatedfield_exercise_time_personal_health_assessment', on_delete=models.CASCADE, null=True, blank=True, verbose_name='运动时长')
    boolfield_is_it_easy_to_get_sick = models.BooleanField(null=True, blank=True, verbose_name='是否比别人容易生病')
    relatedfield_have_any_recent_symptoms_of_physical_discomfort = models.ForeignKey(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_relatedfield_have_any_recent_symptoms_of_physical_discomfort_personal_health_assessment', on_delete=models.CASCADE, null=True, blank=True, verbose_name='近来有无身体不适症状')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '个人身体健康评估'
        verbose_name_plural = '个人身体健康评估'

    def get_absolute_url(self):
        return reverse('personal_health_assessment_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('personal_health_assessment_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('personal_health_assessment_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Social_environment_assessment(models.Model):
    relatedfield_is_the_living_environment_satisfactory = models.ForeignKey(Satisfaction, related_name='satisfaction_for_relatedfield_is_the_living_environment_satisfactory_social_environment_assessment', on_delete=models.CASCADE, null=True, blank=True, verbose_name='您对居住环境满意吗')
    relatedfield_is_the_transportation_convenient = models.ForeignKey(Convenience, related_name='convenience_for_relatedfield_is_the_transportation_convenient_social_environment_assessment', on_delete=models.CASCADE, null=True, blank=True, verbose_name='您所在的社区交通方便吗')
    boolfield_whether_the_living_environment_is_clean_and_hygienic = models.BooleanField(null=True, blank=True, verbose_name='居住环境是否干净卫生')
    boolfield_is_drinking_water_healthy = models.BooleanField(null=True, blank=True, verbose_name='饮水是否健康')
    boolfield_whether_there_is_noise_pollution = models.BooleanField(null=True, blank=True, verbose_name='是否有噪声污染')
    boolfield_whether_there_is_air_pollution = models.BooleanField(null=True, blank=True, verbose_name='是否有空气污染')
    boolfield_whether_there_is_other_pollution = models.BooleanField(null=True, blank=True, verbose_name='是否有其他污染')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '社会环境评估'
        verbose_name_plural = '社会环境评估'

    def get_absolute_url(self):
        return reverse('social_environment_assessment_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('social_environment_assessment_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('social_environment_assessment_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Vital_signs_check(models.Model):
    numberfield_body_temperature = models.IntegerField(null=True, blank=True, verbose_name='体温')
    numberfield_body_temperature_standard_value = models.IntegerField(null=True, blank=True, verbose_name='体温标准值')
    numberfield_body_temperature_up_limit = models.IntegerField(default=37.4, null=True, blank=True, verbose_name='体温上限')
    numberfield_body_temperature_down_limit = models.IntegerField(default=36.0, null=True, blank=True, verbose_name='体温下限')
    numberfield_pulse = models.IntegerField(null=True, blank=True, verbose_name='脉搏')
    numberfield_pulse_standard_value = models.IntegerField(null=True, blank=True, verbose_name='脉搏标准值')
    numberfield_pulse_up_limit = models.IntegerField(default=100.0, null=True, blank=True, verbose_name='脉搏上限')
    numberfield_pulse_down_limit = models.IntegerField(default=60.0, null=True, blank=True, verbose_name='脉搏下限')
    numberfield_respiratory_rate = models.IntegerField(null=True, blank=True, verbose_name='呼吸频率')
    numberfield_respiratory_rate_standard_value = models.IntegerField(null=True, blank=True, verbose_name='呼吸频率标准值')
    numberfield_respiratory_rate_up_limit = models.IntegerField(default=20.0, null=True, blank=True, verbose_name='呼吸频率上限')
    numberfield_respiratory_rate_down_limit = models.IntegerField(default=10.0, null=True, blank=True, verbose_name='呼吸频率下限')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '生命体征检查'
        verbose_name_plural = '生命体征检查'

    def get_absolute_url(self):
        return reverse('vital_signs_check_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('vital_signs_check_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('vital_signs_check_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Family_history_of_illness(models.Model):
    relatedfield_diseases = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_relatedfield_diseases_family_history_of_illness', on_delete=models.CASCADE, null=True, blank=True, verbose_name='病名')
    relatedfield_family_relationship = models.ForeignKey(Family_relationship, related_name='family_relationship_for_relatedfield_family_relationship_family_history_of_illness', on_delete=models.CASCADE, null=True, blank=True, verbose_name='家庭成员关系')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '家族病史'
        verbose_name_plural = '家族病史'

    def get_absolute_url(self):
        return reverse('family_history_of_illness_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('family_history_of_illness_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('family_history_of_illness_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Physical_examination(models.Model):
    numberfield_hight = models.IntegerField(null=True, blank=True, verbose_name='身高')
    numberfield_hight_standard_value = models.IntegerField(null=True, blank=True, verbose_name='身高标准值')
    numberfield_hight_up_limit = models.IntegerField(null=True, blank=True, verbose_name='身高上限')
    numberfield_hight_down_limit = models.IntegerField(null=True, blank=True, verbose_name='身高下限')
    numberfield_weight = models.IntegerField(null=True, blank=True, verbose_name='体重')
    numberfield_weight_standard_value = models.IntegerField(null=True, blank=True, verbose_name='体重标准值')
    numberfield_weight_up_limit = models.IntegerField(null=True, blank=True, verbose_name='体重上限')
    numberfield_weight_down_limit = models.IntegerField(null=True, blank=True, verbose_name='体重下限')
    numberfield_body_mass_index = models.IntegerField(null=True, blank=True, verbose_name='体质指数')
    numberfield_body_mass_index_standard_value = models.IntegerField(null=True, blank=True, verbose_name='体质指数标准值')
    numberfield_body_mass_index_up_limit = models.IntegerField(default=23.9, null=True, blank=True, verbose_name='体质指数上限')
    numberfield_body_mass_index_down_limit = models.IntegerField(default=18.5, null=True, blank=True, verbose_name='体质指数下限')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '体格检查'
        verbose_name_plural = '体格检查'

    def get_absolute_url(self):
        return reverse('physical_examination_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('physical_examination_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('physical_examination_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class History_of_blood_transfusion(models.Model):
    datetimefield_date = models.DateTimeField(null=True, blank=True, verbose_name='日期')
    numberfield_blood_transfusion = models.IntegerField(null=True, blank=True, verbose_name='输血量')
    numberfield_blood_transfusion_standard_value = models.IntegerField(null=True, blank=True, verbose_name='输血量标准值')
    numberfield_blood_transfusion_up_limit = models.IntegerField(default=400.0, null=True, blank=True, verbose_name='输血量上限')
    numberfield_blood_transfusion_down_limit = models.IntegerField(null=True, blank=True, verbose_name='输血量下限')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '输血史'
        verbose_name_plural = '输血史'

    def get_absolute_url(self):
        return reverse('history_of_blood_transfusion_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('history_of_blood_transfusion_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('history_of_blood_transfusion_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class History_of_trauma(models.Model):
    datetimefield_date = models.DateTimeField(null=True, blank=True, verbose_name='日期')
    relatedfield_diseases_name = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_relatedfield_diseases_name_history_of_trauma', on_delete=models.CASCADE, null=True, blank=True, verbose_name='病名')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '外伤史'
        verbose_name_plural = '外伤史'

    def get_absolute_url(self):
        return reverse('history_of_trauma_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('history_of_trauma_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('history_of_trauma_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Fundus_examination(models.Model):
    relatedfield_fundus = models.ForeignKey(Normality, related_name='normality_for_relatedfield_fundus_fundus_examination', on_delete=models.CASCADE, null=True, blank=True, verbose_name='眼底')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '眼底检查'
        verbose_name_plural = '眼底检查'

    def get_absolute_url(self):
        return reverse('fundus_examination_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('fundus_examination_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('fundus_examination_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Medical_history(models.Model):
    relatedfield_disease_name = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_relatedfield_disease_name_medical_history', on_delete=models.CASCADE, null=True, blank=True, verbose_name='疾病名称')
    datetimefield_time_of_diagnosis = models.DateTimeField(null=True, blank=True, verbose_name='确诊时间')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '疾病史'
        verbose_name_plural = '疾病史'

    def get_absolute_url(self):
        return reverse('medical_history_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('medical_history_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('medical_history_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Doctor_registry(models.Model):
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    characterfield_identification_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='身份证号码')
    characterfield_contact_information = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    relatedfield_service_role = models.ForeignKey(Service_role, related_name='service_role_for_relatedfield_service_role_doctor_registry', on_delete=models.CASCADE, null=True, blank=True, verbose_name='服务角色')
    characterfield_practice_qualification = models.CharField(max_length=255, null=True, blank=True, verbose_name='执业资质')
    characterfield_password_setting = models.CharField(max_length=255, null=True, blank=True, verbose_name='密码设置')
    characterfield_confirm_password = models.CharField(max_length=255, null=True, blank=True, verbose_name='确认密码')
    characterfield_expertise = models.CharField(max_length=255, null=True, blank=True, verbose_name='专长')
    characterfield_practice_time = models.CharField(max_length=255, null=True, blank=True, verbose_name='执业时间')
    relatedfield_affiliation = models.ForeignKey(Institutions_list, related_name='institutions_list_for_relatedfield_affiliation_doctor_registry', on_delete=models.CASCADE, null=True, blank=True, verbose_name='所属机构')
    datetimefield_date_of_birth = models.DateTimeField(null=True, blank=True, verbose_name='出生日期')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '医生注册'
        verbose_name_plural = '医生注册'

    def get_absolute_url(self):
        return reverse('doctor_registry_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('doctor_registry_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('doctor_registry_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class User_login(models.Model):
    characterfield_username = models.CharField(max_length=255, null=True, blank=True, verbose_name='用户名')
    characterfield_password = models.CharField(max_length=255, null=True, blank=True, verbose_name='密码')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '用户登录'
        verbose_name_plural = '用户登录'

    def get_absolute_url(self):
        return reverse('user_login_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('user_login_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('user_login_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Doctor_login(models.Model):
    characterfield_username = models.CharField(max_length=255, null=True, blank=True, verbose_name='用户名')
    characterfield_password = models.CharField(max_length=255, null=True, blank=True, verbose_name='密码')
    characterfield_service_role = models.CharField(max_length=255, null=True, blank=True, verbose_name='服务角色')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '医生登陆'
        verbose_name_plural = '医生登陆'

    def get_absolute_url(self):
        return reverse('doctor_login_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('doctor_login_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('doctor_login_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Dorsal_artery_pulsation_examination(models.Model):
    relatedfield_left_foot = models.ForeignKey(Dorsal_artery_pulsation, related_name='dorsal_artery_pulsation_for_relatedfield_left_foot_dorsal_artery_pulsation_examination', on_delete=models.CASCADE, null=True, blank=True, verbose_name='左脚')
    relatedfield_right_foot = models.ForeignKey(Dorsal_artery_pulsation, related_name='dorsal_artery_pulsation_for_relatedfield_right_foot_dorsal_artery_pulsation_examination', on_delete=models.CASCADE, null=True, blank=True, verbose_name='右脚')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '足背动脉搏动检查'
        verbose_name_plural = '足背动脉搏动检查'

    def get_absolute_url(self):
        return reverse('dorsal_artery_pulsation_examination_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('dorsal_artery_pulsation_examination_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('dorsal_artery_pulsation_examination_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Physical_examination_hearing(models.Model):
    relatedfield_left_ear_hearing = models.ForeignKey(Hearing, related_name='hearing_for_relatedfield_left_ear_hearing_physical_examination_hearing', on_delete=models.CASCADE, null=True, blank=True, verbose_name='左耳听力')
    relatedfield_right_ear_hearing = models.ForeignKey(Hearing, related_name='hearing_for_relatedfield_right_ear_hearing_physical_examination_hearing', on_delete=models.CASCADE, null=True, blank=True, verbose_name='右耳听力')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '查体听力'
        verbose_name_plural = '查体听力'

    def get_absolute_url(self):
        return reverse('physical_examination_hearing_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('physical_examination_hearing_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('physical_examination_hearing_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class History_of_infectious_diseases(models.Model):
    relatedfield_diseases = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_relatedfield_diseases_history_of_infectious_diseases', on_delete=models.CASCADE, null=True, blank=True, verbose_name='病名')
    relatedfield_family_relationship = models.ForeignKey(Family_relationship, related_name='family_relationship_for_relatedfield_family_relationship_history_of_infectious_diseases', on_delete=models.CASCADE, null=True, blank=True, verbose_name='家庭成员关系')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '遗传病史'
        verbose_name_plural = '遗传病史'

    def get_absolute_url(self):
        return reverse('history_of_infectious_diseases_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('history_of_infectious_diseases_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('history_of_infectious_diseases_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class History_of_surgery(models.Model):
    datetimefield_date = models.DateTimeField(null=True, blank=True, verbose_name='日期')
    relatedfield_name_of_operation = models.ForeignKey(Icpc7_treatments, related_name='icpc7_treatments_for_relatedfield_name_of_operation_history_of_surgery', on_delete=models.CASCADE, null=True, blank=True, verbose_name='手术名称')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '手术史'
        verbose_name_plural = '手术史'

    def get_absolute_url(self):
        return reverse('history_of_surgery_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('history_of_surgery_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('history_of_surgery_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Physical_examination_oral_cavity(models.Model):
    relatedfield_lips = models.ForeignKey(Lips, related_name='lips_for_relatedfield_lips_physical_examination_oral_cavity', on_delete=models.CASCADE, null=True, blank=True, verbose_name='口唇')
    relatedfield_dentition = models.ForeignKey(Dentition, related_name='dentition_for_relatedfield_dentition_physical_examination_oral_cavity', on_delete=models.CASCADE, null=True, blank=True, verbose_name='齿列')
    relatedfield_pharynx = models.ForeignKey(Pharynx, related_name='pharynx_for_relatedfield_pharynx_physical_examination_oral_cavity', on_delete=models.CASCADE, null=True, blank=True, verbose_name='咽部')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '查体口腔'
        verbose_name_plural = '查体口腔'

    def get_absolute_url(self):
        return reverse('physical_examination_oral_cavity_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('physical_examination_oral_cavity_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('physical_examination_oral_cavity_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Blood_pressure_monitoring(models.Model):
    numberfield_systolic_blood_pressure = models.IntegerField(null=True, blank=True, verbose_name='收缩压')
    numberfield_systolic_blood_pressure_standard_value = models.IntegerField(null=True, blank=True, verbose_name='收缩压标准值')
    numberfield_systolic_blood_pressure_up_limit = models.IntegerField(default=139.0, null=True, blank=True, verbose_name='收缩压上限')
    numberfield_systolic_blood_pressure_down_limit = models.IntegerField(default=90.0, null=True, blank=True, verbose_name='收缩压下限')
    numberfield_diastolic_blood_pressure = models.IntegerField(null=True, blank=True, verbose_name='舒张压')
    numberfield_diastolic_blood_pressure_standard_value = models.IntegerField(null=True, blank=True, verbose_name='舒张压标准值')
    numberfield_diastolic_blood_pressure_up_limit = models.IntegerField(default=89.0, null=True, blank=True, verbose_name='舒张压上限')
    numberfield_diastolic_blood_pressure_down_limit = models.IntegerField(default=60.0, null=True, blank=True, verbose_name='舒张压下限')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '血压监测'
        verbose_name_plural = '血压监测'

    def get_absolute_url(self):
        return reverse('blood_pressure_monitoring_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('blood_pressure_monitoring_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('blood_pressure_monitoring_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Major_life_events(models.Model):
    datetimefield_date = models.DateTimeField(null=True, blank=True, verbose_name='日期')
    relatedfield_major_life = models.ForeignKey(Life_event, related_name='life_event_for_relatedfield_major_life_major_life_events', on_delete=models.CASCADE, null=True, blank=True, verbose_name='生活事件')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '重大生活事件调查'
        verbose_name_plural = '重大生活事件调查'

    def get_absolute_url(self):
        return reverse('major_life_events_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('major_life_events_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('major_life_events_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Physical_examination_vision(models.Model):
    characterfield_left_eye_vision = models.CharField(max_length=255, null=True, blank=True, verbose_name='左眼视力')
    characterfield_right_eye_vision = models.CharField(max_length=255, null=True, blank=True, verbose_name='右眼视力')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '查体视力'
        verbose_name_plural = '查体视力'

    def get_absolute_url(self):
        return reverse('physical_examination_vision_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('physical_examination_vision_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('physical_examination_vision_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Lower_extremity_edema_examination(models.Model):
    relatedfield_lower_extremity_edema = models.ForeignKey(Edema, related_name='edema_for_relatedfield_lower_extremity_edema_lower_extremity_edema_examination', on_delete=models.CASCADE, null=True, blank=True, verbose_name='下肢水肿')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '下肢水肿检查'
        verbose_name_plural = '下肢水肿检查'

    def get_absolute_url(self):
        return reverse('lower_extremity_edema_examination_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('lower_extremity_edema_examination_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('lower_extremity_edema_examination_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Basic_personal_information(models.Model):
    relatedfield_family_relationship = models.ForeignKey(Family_relationship, related_name='family_relationship_for_relatedfield_family_relationship_basic_personal_information', on_delete=models.CASCADE, null=True, blank=True, verbose_name='家庭成员关系')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_identification_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='身份证号码')
    datetimefield_date_of_birth = models.DateTimeField(null=True, blank=True, verbose_name='出生日期')
    relatedfield_family_id = models.ForeignKey(Icpc1_register_logins, related_name='icpc1_register_logins_for_relatedfield_family_id_basic_personal_information', on_delete=models.CASCADE, null=True, blank=True, verbose_name='家庭编号')
    characterfield_resident_file_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='居民档案号')
    relatedfield_gender = models.ForeignKey(Gender, related_name='gender_for_relatedfield_gender_basic_personal_information', on_delete=models.CASCADE, null=True, blank=True, verbose_name='性别')
    relatedfield_nationality = models.ForeignKey(Nationality, related_name='nationality_for_relatedfield_nationality_basic_personal_information', on_delete=models.CASCADE, null=True, blank=True, verbose_name='民族')
    relatedfield_marital_status = models.ForeignKey(Marital_status, related_name='marital_status_for_relatedfield_marital_status_basic_personal_information', on_delete=models.CASCADE, null=True, blank=True, verbose_name='婚姻状况')
    relatedfield_education = models.ForeignKey(Education, related_name='education_for_relatedfield_education_basic_personal_information', on_delete=models.CASCADE, null=True, blank=True, verbose_name='文化程度')
    relatedfield_occupational_status = models.ForeignKey(Occupational_status, related_name='occupational_status_for_relatedfield_occupational_status_basic_personal_information', on_delete=models.CASCADE, null=True, blank=True, verbose_name='职业状况')
    characterfield_family_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='家庭地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_medical_ic_card_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='医疗ic卡号')
    relatedfield_medical_expenses_burden = models.ForeignKey(Medical_expenses_burden, related_name='medical_expenses_burden_for_relatedfield_medical_expenses_burden_basic_personal_information', on_delete=models.CASCADE, null=True, blank=True, verbose_name='医疗费用负担')
    relatedfield_type_of_residence = models.ForeignKey(Type_of_residence, related_name='type_of_residence_for_relatedfield_type_of_residence_basic_personal_information', on_delete=models.CASCADE, null=True, blank=True, verbose_name='居住类型')
    relatedfield_blood_type = models.ForeignKey(Blood_type, related_name='blood_type_for_relatedfield_blood_type_basic_personal_information', on_delete=models.CASCADE, null=True, blank=True, verbose_name='血型')
    boolfield_contract_signatory = models.BooleanField(null=True, blank=True, verbose_name='合同签约户')
    relatedfield_signed_family_doctor = models.ForeignKey(Employee_list, related_name='employee_list_for_relatedfield_signed_family_doctor_basic_personal_information', on_delete=models.CASCADE, null=True, blank=True, verbose_name='签约家庭医生')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '个人基本情况'
        verbose_name_plural = '个人基本情况'

    def get_absolute_url(self):
        return reverse('basic_personal_information_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('basic_personal_information_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('basic_personal_information_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Physical_examination_athletic_ability(models.Model):
    relatedfield_athletic_ability = models.ForeignKey(Exercise_time, related_name='exercise_time_for_relatedfield_athletic_ability_physical_examination_athletic_ability', on_delete=models.CASCADE, null=True, blank=True, verbose_name='运动能力')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '查体运动能力'
        verbose_name_plural = '查体运动能力'

    def get_absolute_url(self):
        return reverse('physical_examination_athletic_ability_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('physical_examination_athletic_ability_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('physical_examination_athletic_ability_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class User_registry(models.Model):
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    characterfield_identification_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='身份证号码')
    characterfield_contact_information = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_password_setting = models.CharField(max_length=255, null=True, blank=True, verbose_name='密码设置')
    characterfield_confirm_password = models.CharField(max_length=255, null=True, blank=True, verbose_name='确认密码')
    datetimefield_date_of_birth = models.DateTimeField(null=True, blank=True, verbose_name='出生日期')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="客户")
    operator = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业人员")
    pid = models.ForeignKey(Operation_proc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="作业进程id")
    slug = models.SlugField(max_length=250, blank=True, null=True, verbose_name="slug")

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '用户注册表'
        verbose_name_plural = '用户注册表'

    def get_absolute_url(self):
        return reverse('user_registry_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('user_registry_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('user_registry_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

