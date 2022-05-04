from django.db import models
from django.shortcuts import reverse
import json

from icpc.models import *
from dictionaries.models import *
from core.models import HsscFormModel, Role, Staff, OperationProc
from entities.models import *


@receiver(post_save, sender=OperationProc)
def operation_proc_created(sender, instance, created, **kwargs):
    # 创建服务进程里使用的表单实例, 将form_slugs保存到进程实例中
    if created:
        form_slugs = []
        for form in instance.service.buessiness_forms.all():
            form_class_name = form.name.capitalize()
            print('创建表单实例:', form_class_name)
            form = eval(form_class_name).objects.create(
                customer=instance.customer,
                creater=instance.operator,
                pid=instance,
                cpid=instance.contract_service_proc,
            )
            form_slugs.append({'form_name': form_class_name, 'slug': form.slug})
        instance.form_slugs = json.dumps(form_slugs, ensure_ascii=False, indent=4)
        instance.save()


class Z6205(HsscFormModel):
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    characterhssc_identification_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='身份证号码')
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_practice_qualification = models.CharField(max_length=255, null=True, blank=True, verbose_name='执业资质')
    characterfield_password_setting = models.CharField(max_length=255, null=True, blank=True, verbose_name='密码设置')
    characterfield_confirm_password = models.CharField(max_length=255, null=True, blank=True, verbose_name='确认密码')
    characterfield_expertise = models.CharField(max_length=255, null=True, blank=True, verbose_name='专长')
    characterfield_practice_time = models.CharField(max_length=255, null=True, blank=True, verbose_name='执业时间')
    datetimefield_date_of_birth = models.DateField(null=True, blank=True, verbose_name='出生日期')
    relatedfield_affiliation = models.ForeignKey(Institution, related_name='institution_for_relatedfield_affiliation_Z6205', on_delete=models.CASCADE, null=True, blank=True, verbose_name='所属机构')
    relatedfield_service_role = models.ManyToManyField(Fu_wu_jue_se, related_name='fu_wu_jue_se_for_relatedfield_service_role_Z6205', verbose_name='服务角色')
    class Meta:
        verbose_name = '医生注册'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('Z6205_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('Z6205_update_url', kwargs={'slug': self.slug})
        

class A3109(HsscFormModel):
    characterfield_right_eye_vision = models.CharField(max_length=255, null=True, blank=True, verbose_name='右眼视力')
    characterfield_left_eye_vision = models.CharField(max_length=255, null=True, blank=True, verbose_name='左眼视力')
    class Meta:
        verbose_name = '视力检查'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A3109_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A3109_update_url', kwargs={'slug': self.slug})
        

class A3108(HsscFormModel):
    relatedfield_lips = models.ForeignKey(Lips, related_name='lips_for_relatedfield_lips_A3108', on_delete=models.CASCADE, null=True, blank=True, verbose_name='口唇')
    relatedfield_dentition = models.ForeignKey(Dentition, related_name='dentition_for_relatedfield_dentition_A3108', on_delete=models.CASCADE, null=True, blank=True, verbose_name='齿列')
    relatedfield_pharynx = models.ForeignKey(Pharynx, related_name='pharynx_for_relatedfield_pharynx_A3108', on_delete=models.CASCADE, null=True, blank=True, verbose_name='咽部')
    class Meta:
        verbose_name = '口腔检查'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A3108_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A3108_update_url', kwargs={'slug': self.slug})
        

class T4502(HsscFormModel):
    T4502 = models.ManyToManyField(Icpc8_other_health_interventions, related_name='icpc8_other_health_interventions_for_T4502_T4502', verbose_name='运动干预')
    class Meta:
        verbose_name = '运动干预'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('T4502_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('T4502_update_url', kwargs={'slug': self.slug})
        

class Ji_gou_ji_ben_xin_xi_biao(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    boolfield_ji_gou_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构编码')
    boolfield_ji_gou_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构名称')
    boolfield_ji_gou_dai_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构代码')
    boolfield_ji_gou_shu_xing = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构属性')
    boolfield_ji_gou_ceng_ji = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构层级')
    boolfield_suo_zai_hang_zheng_qu_hua_dai_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='所在行政区划代码')
    boolfield_xing_zheng_qu_hua_gui_shu = models.CharField(max_length=255, null=True, blank=True, verbose_name='行政区划归属')
    boolfield_fa_ding_fu_ze_ren = models.CharField(max_length=255, null=True, blank=True, verbose_name='法定负责人')
    class Meta:
        verbose_name = '机构基本信息表'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('ji_gou_ji_ben_xin_xi_biao_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('ji_gou_ji_ben_xin_xi_biao_update_url', kwargs={'slug': self.slug})
        

class Wu_liu_gong_ying_shang_ji_ben_xin_xi_biao(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    boolfield_gong_ying_shang_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='供应商编码')
    boolfield_zhu_yao_gong_ying_chan_pin = models.CharField(max_length=255, null=True, blank=True, verbose_name='主要供应产品')
    boolfield_gong_huo_zhou_qi = models.CharField(max_length=255, null=True, blank=True, verbose_name='供货周期')
    boolfield_gong_ying_shang_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='供应商名称')
    boolfield_xin_yu_ping_ji = models.ForeignKey(Xin_yu_ping_ji, related_name='xin_yu_ping_ji_for_boolfield_xin_yu_ping_ji_wu_liu_gong_ying_shang_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='信誉评级')
    class Meta:
        verbose_name = '物料供应商基本信息表'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('wu_liu_gong_ying_shang_ji_ben_xin_xi_biao_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('wu_liu_gong_ying_shang_ji_ben_xin_xi_biao_update_url', kwargs={'slug': self.slug})
        

class Zhi_yuan_ji_ben_xin_xi_biao(HsscFormModel):
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterhssc_identification_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='身份证号码')
    characterfield_practice_qualification = models.CharField(max_length=255, null=True, blank=True, verbose_name='执业资质')
    characterfield_expertise = models.CharField(max_length=255, null=True, blank=True, verbose_name='专长')
    characterfield_practice_time = models.CharField(max_length=255, null=True, blank=True, verbose_name='执业时间')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    boolfield_zhi_yuan_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='职员编码')
    relatedfield_affiliation = models.ForeignKey(Institution, related_name='institution_for_relatedfield_affiliation_zhi_yuan_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='所属机构')
    relatedfield_service_role = models.ManyToManyField(Fu_wu_jue_se, related_name='fu_wu_jue_se_for_relatedfield_service_role_zhi_yuan_ji_ben_xin_xi_biao', verbose_name='服务角色')
    class Meta:
        verbose_name = '职员基本信息表'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('zhi_yuan_ji_ben_xin_xi_biao_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('zhi_yuan_ji_ben_xin_xi_biao_update_url', kwargs={'slug': self.slug})
        

class She_bei_ji_ben_xin_xi_biao(HsscFormModel):
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    boolfield_she_bei_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备名称')
    boolfield_she_bei_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备编码')
    boolfield_sheng_chan_chang_jia = models.CharField(max_length=255, null=True, blank=True, verbose_name='生产厂家')
    boolfield_she_bei_fu_wu_dan_wei_hao_shi = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备服务单位耗时')
    boolfield_she_bei_jian_xiu_zhou_qi = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备检修周期')
    boolfield_she_bei_shi_yong_cheng_ben = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备使用成本')
    boolfield_she_bei_shi_yong_fu_wu_gong_neng = models.ForeignKey(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_she_bei_shi_yong_fu_wu_gong_neng_she_bei_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='设备适用服务功能')
    class Meta:
        verbose_name = '设备基本信息表'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('she_bei_ji_ben_xin_xi_biao_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('she_bei_ji_ben_xin_xi_biao_update_url', kwargs={'slug': self.slug})
        

class Yong_yao_diao_cha_biao(HsscFormModel):
    relatedfield_drug_name = models.ManyToManyField(Medicine, related_name='medicine_for_relatedfield_drug_name_yong_yao_diao_cha_biao', verbose_name='药品名称')
    class Meta:
        verbose_name = '用药调查表'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('yong_yao_diao_cha_biao_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('yong_yao_diao_cha_biao_update_url', kwargs={'slug': self.slug})
        

class T3003(HsscFormModel):
    relatedfield_left_foot = models.ForeignKey(Dorsal_artery_pulsation, related_name='dorsal_artery_pulsation_for_relatedfield_left_foot_T3003', on_delete=models.CASCADE, null=True, blank=True, verbose_name='左脚')
    relatedfield_right_foot = models.ForeignKey(Dorsal_artery_pulsation, related_name='dorsal_artery_pulsation_for_relatedfield_right_foot_T3003', on_delete=models.CASCADE, null=True, blank=True, verbose_name='右脚')
    class Meta:
        verbose_name = '足背动脉检查'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('T3003_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('T3003_update_url', kwargs={'slug': self.slug})
        

class T3002(HsscFormModel):
    relatedfield_fundus = models.ForeignKey(Normality, related_name='normality_for_relatedfield_fundus_T3002', on_delete=models.CASCADE, null=True, blank=True, verbose_name='眼底')
    class Meta:
        verbose_name = '眼底检查'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('T3002_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('T3002_update_url', kwargs={'slug': self.slug})
        

class Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_biao(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    boolfield_ji_gou_dai_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构代码')
    boolfield_ji_gou_shu_xing = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构属性')
    boolfield_gong_ying_shang_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='供应商编码')
    boolfield_gong_ying_shang_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='供应商名称')
    boolfield_zhuan_ye_fu_wu = models.CharField(max_length=255, null=True, blank=True, verbose_name='专业服务')
    boolfield_xin_yu_ping_ji = models.ForeignKey(Xin_yu_ping_ji, related_name='xin_yu_ping_ji_for_boolfield_xin_yu_ping_ji_fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='信誉评级')
    class Meta:
        verbose_name = '服务分供机构基本信息表'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_biao_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_biao_update_url', kwargs={'slug': self.slug})
        

class A6208(HsscFormModel):
    numberfield_blood_transfusion = models.IntegerField(null=True, blank=True, verbose_name='输血量')
    numberfield_blood_transfusion_standard_value = models.IntegerField(null=True, blank=True, verbose_name='输血量标准值')
    numberfield_blood_transfusion_up_limit = models.IntegerField(default=400.0, null=True, blank=True, verbose_name='输血量上限')
    numberfield_blood_transfusion_down_limit = models.IntegerField(null=True, blank=True, verbose_name='输血量下限')
    boolfield_shu_xue_ri_qi = models.DateField(null=True, blank=True, verbose_name='输血日期')
    class Meta:
        verbose_name = '输血史'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6208_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6208_update_url', kwargs={'slug': self.slug})
        

class Z6233(HsscFormModel):
    characterfield_username = models.CharField(max_length=255, null=True, blank=True, verbose_name='用户名')
    characterfield_password = models.CharField(max_length=255, null=True, blank=True, verbose_name='密码')
    class Meta:
        verbose_name = '医生'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('Z6233_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('Z6233_update_url', kwargs={'slug': self.slug})
        

class Yao_pin_ji_ben_xin_xi_biao(HsscFormModel):
    boolfield_yao_pin_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='药品编码')
    boolfield_yao_pin_gui_ge = models.CharField(max_length=255, null=True, blank=True, verbose_name='药品规格')
    boolfield_yong_yao_zhou_qi = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药疗程')
    boolfield_chang_yong_chu_fang_liang = models.CharField(max_length=255, null=True, blank=True, verbose_name='常用处方量')
    boolfield_dui_zhao_yi_bao_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='对照医保名称')
    boolfield_dui_zhao_ji_yao_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='对照基药名称')
    boolfield_huan_suan_gui_ze = models.CharField(max_length=255, null=True, blank=True, verbose_name='换算规则')
    boolfield_fu_yong_pin_ci = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药频次')
    boolfield_chu_fang_ji_liang_dan_wei = models.ForeignKey(Yao_pin_dan_wei, related_name='yao_pin_dan_wei_for_boolfield_chu_fang_ji_liang_dan_wei_yao_pin_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='处方计量单位')
    boolfield_ru_ku_ji_liang_dan_wei = models.ForeignKey(Yao_pin_dan_wei, related_name='yao_pin_dan_wei_for_boolfield_ru_ku_ji_liang_dan_wei_yao_pin_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='入库计量单位')
    boolfield_xiao_shou_ji_liang_dan_wei = models.ForeignKey(Yao_pin_dan_wei, related_name='yao_pin_dan_wei_for_boolfield_xiao_shou_ji_liang_dan_wei_yao_pin_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='销售计量单位')
    relatedfield_drug_name = models.ManyToManyField(Medicine, related_name='medicine_for_relatedfield_drug_name_yao_pin_ji_ben_xin_xi_biao', verbose_name='药品名称')
    boolfield_yong_yao_tu_jing = models.ForeignKey(Yong_yao_tu_jing, related_name='yong_yao_tu_jing_for_boolfield_yong_yao_tu_jing_yao_pin_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='用药途径')
    boolfield_yao_pin_fen_lei = models.ForeignKey(Yao_pin_fen_lei, related_name='yao_pin_fen_lei_for_boolfield_yao_pin_fen_lei_yao_pin_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='药品分类')
    class Meta:
        verbose_name = '药品基本信息表'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('yao_pin_ji_ben_xin_xi_biao_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('yao_pin_ji_ben_xin_xi_biao_update_url', kwargs={'slug': self.slug})
        

class A5001(HsscFormModel):
    boolfield_yong_yao_zhou_qi = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药疗程')
    boolfield_chang_yong_chu_fang_liang = models.CharField(max_length=255, null=True, blank=True, verbose_name='常用处方量')
    boolfield_fu_yong_pin_ci = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药频次')
    relatedfield_drug_name = models.ManyToManyField(Medicine, related_name='medicine_for_relatedfield_drug_name_A5001', verbose_name='药品名称')
    boolfield_yong_yao_tu_jing = models.ForeignKey(Yong_yao_tu_jing, related_name='yong_yao_tu_jing_for_boolfield_yong_yao_tu_jing_A5001', on_delete=models.CASCADE, null=True, blank=True, verbose_name='用药途径')
    class Meta:
        verbose_name = '药物处方'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A5001_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A5001_update_url', kwargs={'slug': self.slug})
        

class T4504(HsscFormModel):
    T4504 = models.ManyToManyField(Icpc8_other_health_interventions, related_name='icpc8_other_health_interventions_for_T4504_T4504', verbose_name='健康教育')
    class Meta:
        verbose_name = '健康教育'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('T4504_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('T4504_update_url', kwargs={'slug': self.slug})
        

class Shu_ye_zhu_she_dan(HsscFormModel):
    boolfield_yao_pin_gui_ge = models.CharField(max_length=255, null=True, blank=True, verbose_name='药品规格')
    boolfield_yong_yao_zhou_qi = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药疗程')
    boolfield_chang_yong_chu_fang_liang = models.CharField(max_length=255, null=True, blank=True, verbose_name='常用处方量')
    boolfield_zhi_xing_qian_ming = models.CharField(max_length=255, null=True, blank=True, verbose_name='执行签名')
    boolfield_fu_yong_pin_ci = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药频次')
    boolfield_zhu_she_ri_qi = models.DateTimeField(null=True, blank=True, verbose_name='注射日期')
    relatedfield_drug_name = models.ManyToManyField(Medicine, related_name='medicine_for_relatedfield_drug_name_shu_ye_zhu_she_dan', verbose_name='药品名称')
    class Meta:
        verbose_name = '输液注射单'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('shu_ye_zhu_she_dan_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('shu_ye_zhu_she_dan_update_url', kwargs={'slug': self.slug})
        

class A6219(HsscFormModel):
    characterfield_supplementary_description_of_the_condition = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')
    relatedfield_symptom_list = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_relatedfield_symptom_list_A6219', verbose_name='症状')
    boolfield_tang_niao_bing_zheng_zhuang = models.ManyToManyField(Tang_niao_bing_zheng_zhuang, related_name='tang_niao_bing_zheng_zhuang_for_boolfield_tang_niao_bing_zheng_zhuang_A6219', verbose_name='糖尿病症状')
    class Meta:
        verbose_name = '糖尿病专用问诊'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6219_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6219_update_url', kwargs={'slug': self.slug})
        

class A6203(HsscFormModel):
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterhssc_identification_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='身份证号码')
    characterfield_resident_file_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='居民档案号')
    characterfield_family_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='家庭地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_medical_ic_card_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='医疗ic卡号')
    datetimefield_date_of_birth = models.DateField(null=True, blank=True, verbose_name='出生日期')
    relatedfield_gender = models.ForeignKey(Gender, related_name='gender_for_relatedfield_gender_A6203', on_delete=models.CASCADE, null=True, blank=True, verbose_name='性别')
    relatedfield_nationality = models.ForeignKey(Nationality, related_name='nationality_for_relatedfield_nationality_A6203', on_delete=models.CASCADE, null=True, blank=True, verbose_name='民族')
    relatedfield_marital_status = models.ForeignKey(Marital_status, related_name='marital_status_for_relatedfield_marital_status_A6203', on_delete=models.CASCADE, null=True, blank=True, verbose_name='婚姻状况')
    relatedfield_education = models.ForeignKey(Education, related_name='education_for_relatedfield_education_A6203', on_delete=models.CASCADE, null=True, blank=True, verbose_name='文化程度')
    relatedfield_occupational_status = models.ForeignKey(Occupational_status, related_name='occupational_status_for_relatedfield_occupational_status_A6203', on_delete=models.CASCADE, null=True, blank=True, verbose_name='职业状况')
    relatedfield_medical_expenses_burden = models.ManyToManyField(Medical_expenses_burden, related_name='medical_expenses_burden_for_relatedfield_medical_expenses_burden_A6203', verbose_name='医疗费用负担')
    relatedfield_type_of_residence = models.ForeignKey(Type_of_residence, related_name='type_of_residence_for_relatedfield_type_of_residence_A6203', on_delete=models.CASCADE, null=True, blank=True, verbose_name='居住类型')
    relatedfield_blood_type = models.ForeignKey(Blood_type, related_name='blood_type_for_relatedfield_blood_type_A6203', on_delete=models.CASCADE, null=True, blank=True, verbose_name='血型')
    relatedfield_signed_family_doctor = models.ForeignKey(Staff, related_name='staff_for_relatedfield_signed_family_doctor_A6203', on_delete=models.CASCADE, null=True, blank=True, verbose_name='签约家庭医生')
    relatedfield_family_relationship = models.ForeignKey(Family_relationship, related_name='family_relationship_for_relatedfield_family_relationship_A6203', on_delete=models.CASCADE, null=True, blank=True, verbose_name='家庭成员关系')
    class Meta:
        verbose_name = '个人基本信息'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6203_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6203_update_url', kwargs={'slug': self.slug})
        

class A3001(HsscFormModel):
    characterfield_right_eye_vision = models.CharField(max_length=255, null=True, blank=True, verbose_name='右眼视力')
    characterfield_left_eye_vision = models.CharField(max_length=255, null=True, blank=True, verbose_name='左眼视力')
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
    numberfield_systolic_blood_pressure = models.IntegerField(null=True, blank=True, verbose_name='收缩压')
    numberfield_systolic_blood_pressure_standard_value = models.IntegerField(null=True, blank=True, verbose_name='收缩压标准值')
    numberfield_systolic_blood_pressure_up_limit = models.IntegerField(default=139.0, null=True, blank=True, verbose_name='收缩压上限')
    numberfield_systolic_blood_pressure_down_limit = models.IntegerField(default=90.0, null=True, blank=True, verbose_name='收缩压下限')
    numberfield_diastolic_blood_pressure = models.IntegerField(null=True, blank=True, verbose_name='舒张压')
    numberfield_diastolic_blood_pressure_standard_value = models.IntegerField(null=True, blank=True, verbose_name='舒张压标准值')
    numberfield_diastolic_blood_pressure_up_limit = models.IntegerField(default=89.0, null=True, blank=True, verbose_name='舒张压上限')
    numberfield_diastolic_blood_pressure_down_limit = models.IntegerField(default=60.0, null=True, blank=True, verbose_name='舒张压下限')
    boolfield_yao_wei = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='腰围')
    boolfield_yao_wei_standard_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='腰围标准值')
    boolfield_yao_wei_up_limit = models.DecimalField(max_digits=10, decimal_places=2, default=85.0, null=True, blank=True, verbose_name='腰围上限')
    boolfield_yao_wei_down_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='腰围下限')
    relatedfield_athletic_ability = models.ForeignKey(Exercise_time, related_name='exercise_time_for_relatedfield_athletic_ability_A3001', on_delete=models.CASCADE, null=True, blank=True, verbose_name='运动能力')
    relatedfield_left_ear_hearing = models.ForeignKey(Hearing, related_name='hearing_for_relatedfield_left_ear_hearing_A3001', on_delete=models.CASCADE, null=True, blank=True, verbose_name='左耳听力')
    relatedfield_right_ear_hearing = models.ForeignKey(Hearing, related_name='hearing_for_relatedfield_right_ear_hearing_A3001', on_delete=models.CASCADE, null=True, blank=True, verbose_name='右耳听力')
    relatedfield_lips = models.ForeignKey(Lips, related_name='lips_for_relatedfield_lips_A3001', on_delete=models.CASCADE, null=True, blank=True, verbose_name='口唇')
    relatedfield_dentition = models.ForeignKey(Dentition, related_name='dentition_for_relatedfield_dentition_A3001', on_delete=models.CASCADE, null=True, blank=True, verbose_name='齿列')
    relatedfield_pharynx = models.ForeignKey(Pharynx, related_name='pharynx_for_relatedfield_pharynx_A3001', on_delete=models.CASCADE, null=True, blank=True, verbose_name='咽部')
    relatedfield_lower_extremity_edema = models.ForeignKey(Edema, related_name='edema_for_relatedfield_lower_extremity_edema_A3001', on_delete=models.CASCADE, null=True, blank=True, verbose_name='下肢水肿')
    class Meta:
        verbose_name = '体格检查表'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A3001_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A3001_update_url', kwargs={'slug': self.slug})
        

class A3101(HsscFormModel):
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
    class Meta:
        verbose_name = '身高体重测量'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A3101_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A3101_update_url', kwargs={'slug': self.slug})
        

class A6501(HsscFormModel):
    datetimefield_ri_qi_shi_jian = models.DateTimeField(null=True, blank=True, verbose_name='预约时间')
    boolfield_ze_ren_ren = models.ForeignKey(Staff, related_name='staff_for_boolfield_ze_ren_ren_A6501', on_delete=models.CASCADE, null=True, blank=True, verbose_name='责任人')
    class Meta:
        verbose_name = '代人预约挂号'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6501_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6501_update_url', kwargs={'slug': self.slug})
        

class T4505(HsscFormModel):
    numberfield_kong_fu_xue_tang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='空腹血糖')
    numberfield_kong_fu_xue_tang_standard_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='空腹血糖标准值')
    numberfield_kong_fu_xue_tang_up_limit = models.DecimalField(max_digits=10, decimal_places=2, default=7.0, null=True, blank=True, verbose_name='空腹血糖上限')
    numberfield_kong_fu_xue_tang_down_limit = models.DecimalField(max_digits=10, decimal_places=2, default=3.9, null=True, blank=True, verbose_name='空腹血糖下限')
    class Meta:
        verbose_name = '糖尿病自我监测'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('T4505_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('T4505_update_url', kwargs={'slug': self.slug})
        

class A6211(HsscFormModel):
    datetimefield_date = models.DateField(null=True, blank=True, verbose_name='手术日期')
    relatedfield_major_life = models.ManyToManyField(Life_event, related_name='life_event_for_relatedfield_major_life_A6211', verbose_name='生活事件')
    class Meta:
        verbose_name = '重大生活事件调查'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6211_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6211_update_url', kwargs={'slug': self.slug})
        

class A3502(HsscFormModel):
    boolfield_niao_tang = models.ForeignKey(Niao_tang, related_name='niao_tang_for_boolfield_niao_tang_A3502', on_delete=models.CASCADE, null=True, blank=True, verbose_name='尿糖')
    boolfield_dan_bai_zhi = models.ForeignKey(Dan_bai_zhi, related_name='dan_bai_zhi_for_boolfield_dan_bai_zhi_A3502', on_delete=models.CASCADE, null=True, blank=True, verbose_name='蛋白质')
    boolfield_tong_ti = models.ForeignKey(Tong_ti, related_name='tong_ti_for_boolfield_tong_ti_A3502', on_delete=models.CASCADE, null=True, blank=True, verbose_name='尿酮体')
    class Meta:
        verbose_name = '尿常规检查'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A3502_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A3502_update_url', kwargs={'slug': self.slug})
        

class T4501(HsscFormModel):
    T4501 = models.ManyToManyField(Icpc8_other_health_interventions, related_name='icpc8_other_health_interventions_for_T4501_T4501', verbose_name='营养干预')
    class Meta:
        verbose_name = '营养干预'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('T4501_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('T4501_update_url', kwargs={'slug': self.slug})
        

class A6207(HsscFormModel):
    relatedfield_drug_name = models.ManyToManyField(Medicine, related_name='medicine_for_relatedfield_drug_name_A6207', verbose_name='药品名称')
    class Meta:
        verbose_name = '过敏史'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6207_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6207_update_url', kwargs={'slug': self.slug})
        

class A6206(HsscFormModel):
    boolfield_wai_shang_ri_qi = models.DateField(null=True, blank=True, verbose_name='外伤日期')
    boolfield_wai_shang_xing_ji_bing = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_wai_shang_xing_ji_bing_A6206', on_delete=models.CASCADE, null=True, blank=True, verbose_name='外伤性疾病')
    class Meta:
        verbose_name = '外伤史'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6206_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6206_update_url', kwargs={'slug': self.slug})
        

class A3103(HsscFormModel):
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
    class Meta:
        verbose_name = '生命体征检查'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A3103_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A3103_update_url', kwargs={'slug': self.slug})
        

class A6215(HsscFormModel):
    characterfield_working_hours_per_day = models.TextField(max_length=255, null=True, blank=True, verbose_name='每天工作及工作往返总时长')
    relatedfield_are_you_satisfied_with_the_job_and_life = models.ForeignKey(Satisfaction, related_name='satisfaction_for_relatedfield_are_you_satisfied_with_the_job_and_life_A6215', on_delete=models.CASCADE, null=True, blank=True, verbose_name='对目前生活和工作满意吗')
    relatedfield_are_you_satisfied_with_your_adaptability = models.ForeignKey(Satisfaction, related_name='satisfaction_for_relatedfield_are_you_satisfied_with_your_adaptability_A6215', on_delete=models.CASCADE, null=True, blank=True, verbose_name='对自己的适应能力满意吗')
    class Meta:
        verbose_name = '个人适应能力评估'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6215_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6215_update_url', kwargs={'slug': self.slug})
        

class Z6201(HsscFormModel):
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    characterhssc_identification_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='身份证号码')
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_password_setting = models.CharField(max_length=255, null=True, blank=True, verbose_name='密码设置')
    characterfield_confirm_password = models.CharField(max_length=255, null=True, blank=True, verbose_name='确认密码')
    datetimefield_date_of_birth = models.DateField(null=True, blank=True, verbose_name='出生日期')
    class Meta:
        verbose_name = '用户注册'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('Z6201_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('Z6201_update_url', kwargs={'slug': self.slug})
        

class T3404(HsscFormModel):
    numberfield_kong_fu_xue_tang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='空腹血糖')
    numberfield_kong_fu_xue_tang_standard_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='空腹血糖标准值')
    numberfield_kong_fu_xue_tang_up_limit = models.DecimalField(max_digits=10, decimal_places=2, default=7.0, null=True, blank=True, verbose_name='空腹血糖上限')
    numberfield_kong_fu_xue_tang_down_limit = models.DecimalField(max_digits=10, decimal_places=2, default=3.9, null=True, blank=True, verbose_name='空腹血糖下限')
    class Meta:
        verbose_name = '空腹血糖检查'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('T3404_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('T3404_update_url', kwargs={'slug': self.slug})
        

class A3110(HsscFormModel):
    relatedfield_left_ear_hearing = models.ForeignKey(Hearing, related_name='hearing_for_relatedfield_left_ear_hearing_A3110', on_delete=models.CASCADE, null=True, blank=True, verbose_name='左耳听力')
    relatedfield_right_ear_hearing = models.ForeignKey(Hearing, related_name='hearing_for_relatedfield_right_ear_hearing_A3110', on_delete=models.CASCADE, null=True, blank=True, verbose_name='右耳听力')
    class Meta:
        verbose_name = '听力检查'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A3110_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A3110_update_url', kwargs={'slug': self.slug})
        

class A6216(HsscFormModel):
    relatedfield_is_the_living_environment_satisfactory = models.ForeignKey(Satisfaction, related_name='satisfaction_for_relatedfield_is_the_living_environment_satisfactory_A6216', on_delete=models.CASCADE, null=True, blank=True, verbose_name='您对居住环境满意吗')
    relatedfield_is_the_transportation_convenient = models.ForeignKey(Convenience, related_name='convenience_for_relatedfield_is_the_transportation_convenient_A6216', on_delete=models.CASCADE, null=True, blank=True, verbose_name='您所在的社区交通方便吗')
    class Meta:
        verbose_name = '社会环境评估'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6216_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6216_update_url', kwargs={'slug': self.slug})
        

class A6218(HsscFormModel):
    characterfield_supplementary_description_of_the_condition = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')
    relatedfield_symptom_list = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_relatedfield_symptom_list_A6218', verbose_name='症状')
    class Meta:
        verbose_name = '门诊医生问诊'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6218_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6218_update_url', kwargs={'slug': self.slug})
        

class A6205(HsscFormModel):
    datetimefield_date = models.DateField(null=True, blank=True, verbose_name='手术日期')
    relatedfield_name_of_operation = models.ForeignKey(Icpc7_treatments, related_name='icpc7_treatments_for_relatedfield_name_of_operation_A6205', on_delete=models.CASCADE, null=True, blank=True, verbose_name='手术名称')
    class Meta:
        verbose_name = '手术史'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6205_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6205_update_url', kwargs={'slug': self.slug})
        

class A6214(HsscFormModel):
    relatedfield_own_health = models.ForeignKey(State_degree, related_name='state_degree_for_relatedfield_own_health_A6214', on_delete=models.CASCADE, null=True, blank=True, verbose_name='觉得自身健康状况如何')
    relatedfield_compared_to_last_year = models.ForeignKey(Comparative_expression, related_name='comparative_expression_for_relatedfield_compared_to_last_year_A6214', on_delete=models.CASCADE, null=True, blank=True, verbose_name='较之过去一年状态如何')
    relatedfield_sports_preference = models.ForeignKey(Sports_preference, related_name='sports_preference_for_relatedfield_sports_preference_A6214', on_delete=models.CASCADE, null=True, blank=True, verbose_name='运动偏好')
    relatedfield_exercise_time = models.ForeignKey(Exercise_time, related_name='exercise_time_for_relatedfield_exercise_time_A6214', on_delete=models.CASCADE, null=True, blank=True, verbose_name='运动时长')
    relatedfield_have_any_recent_symptoms_of_physical_discomfort = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_relatedfield_have_any_recent_symptoms_of_physical_discomfort_A6214', verbose_name='近来有无身体不适症状')
    class Meta:
        verbose_name = '个人身体健康评估'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6214_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6214_update_url', kwargs={'slug': self.slug})
        

class Z6230(HsscFormModel):
    characterfield_username = models.CharField(max_length=255, null=True, blank=True, verbose_name='用户名')
    characterfield_password = models.CharField(max_length=255, null=True, blank=True, verbose_name='密码')
    class Meta:
        verbose_name = '用户登录'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('Z6230_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('Z6230_update_url', kwargs={'slug': self.slug})
        

class A3105(HsscFormModel):
    numberfield_systolic_blood_pressure = models.IntegerField(null=True, blank=True, verbose_name='收缩压')
    numberfield_systolic_blood_pressure_standard_value = models.IntegerField(null=True, blank=True, verbose_name='收缩压标准值')
    numberfield_systolic_blood_pressure_up_limit = models.IntegerField(default=139.0, null=True, blank=True, verbose_name='收缩压上限')
    numberfield_systolic_blood_pressure_down_limit = models.IntegerField(default=90.0, null=True, blank=True, verbose_name='收缩压下限')
    numberfield_diastolic_blood_pressure = models.IntegerField(null=True, blank=True, verbose_name='舒张压')
    numberfield_diastolic_blood_pressure_standard_value = models.IntegerField(null=True, blank=True, verbose_name='舒张压标准值')
    numberfield_diastolic_blood_pressure_up_limit = models.IntegerField(default=89.0, null=True, blank=True, verbose_name='舒张压上限')
    numberfield_diastolic_blood_pressure_down_limit = models.IntegerField(default=60.0, null=True, blank=True, verbose_name='舒张压下限')
    class Meta:
        verbose_name = '血压监测'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A3105_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A3105_update_url', kwargs={'slug': self.slug})
        

class A6217(HsscFormModel):
    characterfield_supplementary_description_of_the_condition = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')
    relatedfield_symptom_list = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_relatedfield_symptom_list_A6217', verbose_name='症状')
    class Meta:
        verbose_name = '院内辅助问诊'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6217_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6217_update_url', kwargs={'slug': self.slug})
        

class T3405(HsscFormModel):
    numberfield_tang_hua_xue_hong_dan_bai = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='糖化血红蛋白')
    numberfield_tang_hua_xue_hong_dan_bai_standard_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='糖化血红蛋白标准值')
    numberfield_tang_hua_xue_hong_dan_bai_up_limit = models.DecimalField(max_digits=10, decimal_places=2, default=6.0, null=True, blank=True, verbose_name='糖化血红蛋白上限')
    numberfield_tang_hua_xue_hong_dan_bai_down_limit = models.DecimalField(max_digits=10, decimal_places=2, default=4.0, null=True, blank=True, verbose_name='糖化血红蛋白下限')
    class Meta:
        verbose_name = '糖化血红蛋白检查'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('T3405_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('T3405_update_url', kwargs={'slug': self.slug})
        

class A6202(HsscFormModel):
    characterfield_supplementary_description_of_the_condition = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')
    relatedfield_symptom_list = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_relatedfield_symptom_list_A6202', verbose_name='症状')
    class Meta:
        verbose_name = '院外辅助问诊'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6202_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6202_update_url', kwargs={'slug': self.slug})
        

class A6220(HsscFormModel):
    boolfield_yuan_wai_jian_kang_ping_gu = models.ForeignKey(Sui_fang_ping_gu, related_name='sui_fang_ping_gu_for_boolfield_yuan_wai_jian_kang_ping_gu_A6220', on_delete=models.CASCADE, null=True, blank=True, verbose_name='监测评估')
    class Meta:
        verbose_name = '监测评估'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6220_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6220_update_url', kwargs={'slug': self.slug})
        

class A6212(HsscFormModel):
    characterfield_average_sleep_duration = models.CharField(max_length=255, null=True, blank=True, verbose_name='平均睡眠时长')
    characterfield_duration_of_insomnia = models.CharField(max_length=255, null=True, blank=True, verbose_name='持续失眠时间')
    relatedfield_drinking_frequency = models.ForeignKey(Frequency, related_name='frequency_for_relatedfield_drinking_frequency_A6212', on_delete=models.CASCADE, null=True, blank=True, verbose_name='饮酒频次')
    relatedfield_smoking_frequency = models.ForeignKey(Frequency, related_name='frequency_for_relatedfield_smoking_frequency_A6212', on_delete=models.CASCADE, null=True, blank=True, verbose_name='吸烟频次')
    class Meta:
        verbose_name = '个人健康行为调查'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6212_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6212_update_url', kwargs={'slug': self.slug})
        

class T9001(HsscFormModel):
    relatedfield_disease_name = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_relatedfield_disease_name_T9001', on_delete=models.CASCADE, null=True, blank=True, verbose_name='疾病名称')
    relatedfield_yi_lou_zhen_duan = models.ManyToManyField(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_relatedfield_yi_lou_zhen_duan_T9001', verbose_name='可能诊断')
    relatedfield_pai_chu_zhen_duan = models.ManyToManyField(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_relatedfield_pai_chu_zhen_duan_T9001', verbose_name='排除诊断')
    class Meta:
        verbose_name = '非胰岛素依赖性糖尿病'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('T9001_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('T9001_update_url', kwargs={'slug': self.slug})
        

class A5002(HsscFormModel):
    relatedfield_drug_name = models.ManyToManyField(Medicine, related_name='medicine_for_relatedfield_drug_name_A5002', verbose_name='药品名称')
    relatedfield_disease_name = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_relatedfield_disease_name_A5002', on_delete=models.CASCADE, null=True, blank=True, verbose_name='疾病名称')
    boolfield_shi_fou_ji_xu_shi_yong = models.ForeignKey(Ji_xu_shi_yong_qing_kuang, related_name='ji_xu_shi_yong_qing_kuang_for_boolfield_shi_fou_ji_xu_shi_yong_A5002', on_delete=models.CASCADE, null=True, blank=True, verbose_name='是否继续使用')
    class Meta:
        verbose_name = '药事服务'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A5002_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A5002_update_url', kwargs={'slug': self.slug})
        

class Physical_examination_athletic_ability(HsscFormModel):
    relatedfield_athletic_ability = models.ForeignKey(Exercise_time, related_name='exercise_time_for_relatedfield_athletic_ability_physical_examination_athletic_ability', on_delete=models.CASCADE, null=True, blank=True, verbose_name='运动能力')
    class Meta:
        verbose_name = '运动能力调查'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('physical_examination_athletic_ability_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('physical_examination_athletic_ability_update_url', kwargs={'slug': self.slug})
        

class A6213(HsscFormModel):
    relatedfield_personality_tendency = models.ForeignKey(Character, related_name='character_for_relatedfield_personality_tendency_A6213', on_delete=models.CASCADE, null=True, blank=True, verbose_name='性格倾向')
    boolfield_shi_mian_qing_kuang = models.ForeignKey(Shi_mian_qing_kuang, related_name='shi_mian_qing_kuang_for_boolfield_shi_mian_qing_kuang_A6213', on_delete=models.CASCADE, null=True, blank=True, verbose_name='失眠情况')
    boolfield_sheng_huo_gong_zuo_ya_li_qing_kuang = models.ForeignKey(Ya_li_qing_kuang, related_name='ya_li_qing_kuang_for_boolfield_sheng_huo_gong_zuo_ya_li_qing_kuang_A6213', on_delete=models.CASCADE, null=True, blank=True, verbose_name='生活工作压力情况')
    class Meta:
        verbose_name = '个人心理综合素质调查'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6213_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6213_update_url', kwargs={'slug': self.slug})
        

class Z6261(HsscFormModel):
    boolfield_jia_ting_qian_yue_fu_wu_xie_yi = models.CharField(max_length=255, null=True, blank=True, verbose_name='家庭签约服务协议')
    boolfield_qian_yue_que_ren = models.ForeignKey(Qian_yue_que_ren, related_name='qian_yue_que_ren_for_boolfield_qian_yue_que_ren_Z6261', on_delete=models.CASCADE, null=True, blank=True, verbose_name='签约确认')
    boolfield_ze_ren_ren = models.ForeignKey(Staff, related_name='staff_for_boolfield_ze_ren_ren_Z6261', on_delete=models.CASCADE, null=True, blank=True, verbose_name='责任人')
    class Meta:
        verbose_name = '家庭医生签约'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('Z6261_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('Z6261_update_url', kwargs={'slug': self.slug})
        

class A6201(HsscFormModel):
    characterfield_supplementary_description_of_the_condition = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')
    relatedfield_symptom_list = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_relatedfield_symptom_list_A6201', verbose_name='症状')
    boolfield_chang_yong_zheng_zhuang = models.ManyToManyField(Chang_yong_zheng_zhuang, related_name='chang_yong_zheng_zhuang_for_boolfield_chang_yong_zheng_zhuang_A6201', verbose_name='常用症状')
    class Meta:
        verbose_name = '院外咨询'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6201_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6201_update_url', kwargs={'slug': self.slug})
        

class A6502(HsscFormModel):
    boolfield_qian_dao_que_ren = models.ForeignKey(Qian_dao_que_ren, related_name='qian_dao_que_ren_for_boolfield_qian_dao_que_ren_A6502', on_delete=models.CASCADE, null=True, blank=True, verbose_name='签到确认')
    class Meta:
        verbose_name = '门诊分诊'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6502_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6502_update_url', kwargs={'slug': self.slug})
        

class A6204(HsscFormModel):
    datetimefield_time_of_diagnosis = models.DateTimeField(null=True, blank=True, verbose_name='确诊时间')
    boolfield_ge_ren_bing_shi = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_ge_ren_bing_shi_A6204', on_delete=models.CASCADE, null=True, blank=True, verbose_name='个人病史')
    class Meta:
        verbose_name = '疾病史'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6204_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6204_update_url', kwargs={'slug': self.slug})
        

class T6301(HsscFormModel):
    boolfield_fu_yong_pin_ci = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药频次')
    boolfield_yao_pin_dan_wei = models.ForeignKey(Yao_pin_dan_wei, related_name='yao_pin_dan_wei_for_boolfield_yao_pin_dan_wei_T6301', on_delete=models.CASCADE, null=True, blank=True, verbose_name='药品单位')
    relatedfield_drug_name = models.ManyToManyField(Medicine, related_name='medicine_for_relatedfield_drug_name_T6301', verbose_name='药品名称')
    relatedfield_drinking_frequency = models.ForeignKey(Frequency, related_name='frequency_for_relatedfield_drinking_frequency_T6301', on_delete=models.CASCADE, null=True, blank=True, verbose_name='饮酒频次')
    relatedfield_smoking_frequency = models.ForeignKey(Frequency, related_name='frequency_for_relatedfield_smoking_frequency_T6301', on_delete=models.CASCADE, null=True, blank=True, verbose_name='吸烟频次')
    boolfield_tang_niao_bing_zheng_zhuang = models.ManyToManyField(Tang_niao_bing_zheng_zhuang, related_name='tang_niao_bing_zheng_zhuang_for_boolfield_tang_niao_bing_zheng_zhuang_T6301', verbose_name='糖尿病症状')
    class Meta:
        verbose_name = '糖尿病一般随访'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('T6301_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('T6301_update_url', kwargs={'slug': self.slug})
        

class A6210(HsscFormModel):
    boolfield_yi_chuan_ji_bing = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_yi_chuan_ji_bing_A6210', on_delete=models.CASCADE, null=True, blank=True, verbose_name='遗传性疾病')
    boolfield_yi_chuan_bing_shi_cheng_yuan = models.ManyToManyField(Qin_shu_guan_xi, related_name='qin_shu_guan_xi_for_boolfield_yi_chuan_bing_shi_cheng_yuan_A6210', verbose_name='遗传病史成员')
    class Meta:
        verbose_name = '遗传病史'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6210_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6210_update_url', kwargs={'slug': self.slug})
        

class A6209(HsscFormModel):
    boolfield_jia_zu_xing_ji_bing = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_jia_zu_xing_ji_bing_A6209', on_delete=models.CASCADE, null=True, blank=True, verbose_name='家族性疾病')
    boolfield_jia_zu_bing_shi_cheng_yuan = models.ManyToManyField(Qin_shu_guan_xi, related_name='qin_shu_guan_xi_for_boolfield_jia_zu_bing_shi_cheng_yuan_A6209', verbose_name='家族病史成员')
    class Meta:
        verbose_name = '家族病史'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('A6209_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('A6209_update_url', kwargs={'slug': self.slug})
        

