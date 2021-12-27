from django.db import models

class Drug_list(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "药品清单"
            verbose_name_plural = "药品清单"
            
class Character(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "性格"
            verbose_name_plural = "性格"
            
class Satisfaction(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "满意度"
            verbose_name_plural = "满意度"
            
class Sports_preference(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "运动类型"
            verbose_name_plural = "运动类型"
            
class Exercise_time(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "运动时长"
            verbose_name_plural = "运动时长"
            
class Family_relationship(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "家庭成员关系"
            verbose_name_plural = "家庭成员关系"
            
class Service_role(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "服务角色"
            verbose_name_plural = "服务角色"
            
class Institutions_list(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "机构清单"
            verbose_name_plural = "机构清单"
            
class Dorsal_artery_pulsation(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "足背动脉搏动情况"
            verbose_name_plural = "足背动脉搏动情况"
            
class Hearing(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "听力"
            verbose_name_plural = "听力"
            
class Lips(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "口唇"
            verbose_name_plural = "口唇"
            
class Dentition(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "齿列"
            verbose_name_plural = "齿列"
            
class Pharynx(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "咽部"
            verbose_name_plural = "咽部"
            
class Life_event(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "生活事件"
            verbose_name_plural = "生活事件"
            
class Edema(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "水肿情况"
            verbose_name_plural = "水肿情况"
            
class Marital_status(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "婚姻状况"
            verbose_name_plural = "婚姻状况"
            
class Education(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "文化程度"
            verbose_name_plural = "文化程度"
            
class Occupational_status(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "职业状况"
            verbose_name_plural = "职业状况"
            
class Medical_expenses_burden(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "医疗费用负担"
            verbose_name_plural = "医疗费用负担"
            
class Type_of_residence(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "居住类型"
            verbose_name_plural = "居住类型"
            
class Blood_type(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "血型"
            verbose_name_plural = "血型"
            
class Employee_list(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "职员表"
            verbose_name_plural = "职员表"
            
class Gender(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "性别"
            verbose_name_plural = "性别"
            
class Frequency(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "频次"
            verbose_name_plural = "频次"
            
class Nationality(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "民族"
            verbose_name_plural = "民族"
            
class Comparative_expression(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "比较表达"
            verbose_name_plural = "比较表达"
            
class Normality(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "正常性判断"
            verbose_name_plural = "正常性判断"
            
class Convenience(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "便捷程度"
            verbose_name_plural = "便捷程度"
            
class State_degree(models.Model):
        value = models.CharField(max_length=60, null=True, blank=True, verbose_name="值")
        def __str__(self):
            return self.value

        class Meta:
            verbose_name = "状态程度"
            verbose_name_plural = "状态程度"
            
