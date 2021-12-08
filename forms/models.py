from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from time import time
from datetime import date
from django.utils import timezone

from icpc.models import *
from dictionaries.enums import *
from core.models import Staff, Customer

class Ge_ren_ji_ben_xin_xi_1638359483(models.Model):
    xing_ming_1638358955 = models.CharField(max_length=255, verbose_name='姓名')
    di_zhi_1638358983 = models.TextField(max_length=500, null=True, blank=True, verbose_name='地址')
    dian_hua_1638358998 = models.CharField(max_length=255, null=True, blank=True, verbose_name='电话')
    shen_gao_1638359066 = models.FloatField(null=True, blank=True, verbose_name='身高')
    shen_gao_1638359066_standard_value = models.FloatField(default=-3.0, null=True, blank=True, verbose_name='身高标准值')
    shen_gao_1638359066_up_limit = models.FloatField(null=True, blank=True, verbose_name='身高上限')
    shen_gao_1638359066_down_limit = models.FloatField(null=True, blank=True, verbose_name='身高下限')
    ti_zhong_1638359087 = models.FloatField(null=True, blank=True, verbose_name='体重')
    ti_zhong_1638359087_standard_value = models.FloatField(null=True, blank=True, verbose_name='体重标准值')
    ti_zhong_1638359087_up_limit = models.FloatField(null=True, blank=True, verbose_name='体重上限')
    ti_zhong_1638359087_down_limit = models.FloatField(null=True, blank=True, verbose_name='体重下限')
    ri_qi_1638359153 = models.DateField(default=date.today(), null=True, blank=True, verbose_name='日期')
    chu_sheng_ri_qi_1638359167 = models.DateField(null=True, blank=True, verbose_name='出生日期')
    Xing_bie_1638359238Enum = [(0, "未知"),(1, "男"),(2, "女"),(3, "其他"),]
    xing_bie_1638359238 = models.PositiveSmallIntegerField(default=0, null=True, blank=True, choices=Xing_bie_1638359238Enum, verbose_name='性别')
    Xue_xing_1638359282Enum = [(0, "未知"),(1, "A型"),(2, "B型"),(3, "AB型"),(4, "O型"),]
    xue_xing_1638359282 = models.PositiveSmallIntegerField(null=True, blank=True, choices=Xue_xing_1638359282Enum, verbose_name='血型')
    zheng_zhuang_1638359376 = models.ForeignKey(Icpc3_symptoms_and_problems, on_delete=models.CASCADE, verbose_name='症状')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '个人基本信息'
        verbose_name_plural = '个人基本信息'

    def get_absolute_url(self):
        return reverse('ge_ren_ji_ben_xin_xi_1638359483_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('ge_ren_ji_ben_xin_xi_1638359483_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('ge_ren_ji_ben_xin_xi_1638359483_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

class Ji_bing_shi_1638359530(models.Model):
    xing_ming_1638358955 = models.CharField(max_length=255, verbose_name='姓名')
    ri_qi_1638359153 = models.DateField(default=date.today(), null=True, blank=True, verbose_name='日期')
    zhen_duan_1638359350 = models.ForeignKey(Icpc5_evaluation_and_diagnoses, on_delete=models.CASCADE, verbose_name='诊断')

    def __str__(self):
        return str(self.customer)

    class Meta:
        verbose_name = '疾病史'
        verbose_name_plural = '疾病史'

    def get_absolute_url(self):
        return reverse('ji_bing_shi_1638359530_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('ji_bing_shi_1638359530_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('ji_bing_shi_1638359530_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self._meta.model_name, allow_unicode=True) + f'-{int(time())}'
        super().save(*args, **kwargs)        
        

