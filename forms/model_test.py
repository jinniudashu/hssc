from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from time import time
from datetime import date
from django.utils import timezone

from icpc.models import *
from dictionaries.enums import *
from core.models import Staff, Customer

class Ge_ren_ji_ben_xin_xi_diao_cha_1638065370(models.Model):
    xing_ming_1638063956 = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    dian_hua_1638063972 = models.CharField(max_length=255, null=True, blank=True, verbose_name='电话')
    di_zhi_1638063979 = models.CharField(max_length=255, default="碧瑶", null=True, blank=True, verbose_name='地址')
    jiu_zhen_shi_jian_1638064039 = models.DateTimeField(default=timezone.now(), null=True, blank=True, verbose_name='就诊时间')
    chu_sheng_ri_qi_1638064057 = models.DateField(default=date.today(), null=True, blank=True, verbose_name='出生日期')
    shen_gao_1638064084 = models.IntegerField(null=True, blank=True, verbose_name='身高')
    shen_gao_1638064084_standard_value = models.IntegerField(null=True, blank=True, verbose_name='身高标准值')
    shen_gao_1638064084_up_limit = models.IntegerField(null=True, blank=True, verbose_name='身高上限')
    shen_gao_1638064084_down_limit = models.IntegerField(null=True, blank=True, verbose_name='身高下限')
    ti_zhong_1638064102 = models.IntegerField(default=60.0, verbose_name='体重')
    ti_zhong_1638064102_standard_value = models.IntegerField(default=50.0, verbose_name='体重标准值')
    ti_zhong_1638064102_up_limit = models.IntegerField(default=100.0, verbose_name='体重上限')
    ti_zhong_1638064102_down_limit = models.IntegerField(default=30.0, verbose_name='体重下限')
    Xing_bie_1638064165Enum = [(0, "男"),(1, "女"),]
    xing_bie_1638064165 = models.PositiveSmallIntegerField(choices=Xing_bie_1638064165Enum, verbose_name='性别')
    Xue_xing_1638064329Enum = [(0, "未知"),(1, "A型"),(2, "B型"),(3, "O型"),(4, "AB型"),]
    xue_xing_1638064329 = models.PositiveSmallIntegerField(default=0, choices=Xue_xing_1638064329Enum, verbose_name='血型')
    ICPC_zheng_zhuang_he_wen_ti_1638064906 = models.ForeignKey(Icpc3_symptoms_and_problems, on_delete=models.CASCADE, verbose_name='ICPC症状和问题')
    ri_qi_1638065523 = models.DateTimeField(null=True, blank=True, verbose_name='日期')
    icpc_jian_cha_jie_guo_he_tong_ji_1638189070 = models.ForeignKey(Icpc10_test_results_and_statistics, on_delete=models.CASCADE, verbose_name='ICPC检查结果和统计')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '个人基本信息调查'
        verbose_name_plural = '个人基本信息调查'

    def get_absolute_url(self):
        return reverse('ge_ren_ji_ben_xin_xi_diao_cha_1638065370_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('ge_ren_ji_ben_xin_xi_diao_cha_1638065370_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('ge_ren_ji_ben_xin_xi_diao_cha_1638065370_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Ji_bing_shi_1638065556(models.Model):
    xing_ming_1638063956 = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    ICPC_zheng_zhuang_he_wen_ti_1638064906 = models.ForeignKey(Icpc3_symptoms_and_problems, on_delete=models.CASCADE, verbose_name='ICPC症状和问题')
    ri_qi_1638065523 = models.DateTimeField(null=True, blank=True, verbose_name='日期')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '疾病史'
        verbose_name_plural = '疾病史'

    def get_absolute_url(self):
        return reverse('ji_bing_shi_1638065556_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('ji_bing_shi_1638065556_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('ji_bing_shi_1638065556_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

