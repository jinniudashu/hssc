from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
import json

from icpc.models import *
from dictionaries.models import *
from core.models import HsscFormModel, HsscBaseFormModel, CustomerServiceLog


# 创建一个服务表单实例
def create_form_instance(operation_proc):
    model_name = operation_proc.service.name.capitalize()
    form_instance = eval(model_name).objects.create(
        customer=operation_proc.customer,
        creater=operation_proc.operator,
        pid=operation_proc,
        cpid=operation_proc.contract_service_proc,
    )
    print('From service.models.create_form_instance, 创建表单实例:', model_name, form_instance, model_to_dict(form_instance))
    return form_instance


# **********************************************************************************************************************
# Service表单Model
# **********************************************************************************************************************
class Ji_gou_ji_ben_xin_xi_biao(HsscBaseFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    boolfield_ji_gou_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构编码')
    boolfield_ji_gou_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构名称')
    boolfield_ji_gou_dai_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构代码')
    boolfield_ji_gou_shu_xing = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构属性')
    boolfield_ji_gou_ceng_ji = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构层级')
    boolfield_suo_zai_hang_zheng_qu_hua_dai_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='所在行政区划代码')
    boolfield_xing_zheng_qu_hua_gui_shu = models.CharField(max_length=255, null=True, blank=True, verbose_name='行政区划归属')
    boolfield_fa_ding_fu_ze_ren = models.CharField(max_length=255, null=True, blank=True, verbose_name='法定负责人')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')

    class Meta:
        verbose_name = '机构基本信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Zhi_yuan_ji_ben_xin_xi_biao(HsscBaseFormModel):
    characterhssc_identification_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='身份证号码')
    characterfield_practice_qualification = models.CharField(max_length=255, null=True, blank=True, verbose_name='执业资质')
    characterfield_expertise = models.CharField(max_length=255, null=True, blank=True, verbose_name='专长')
    characterfield_practice_time = models.CharField(max_length=255, null=True, blank=True, verbose_name='执业时间')
    boolfield_zhi_yuan_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='职员编码')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    relatedfield_affiliation = models.ForeignKey(Ji_gou_ji_ben_xin_xi_biao, related_name='ji_gou_ji_ben_xin_xi_biao_for_relatedfield_affiliation_zhi_yuan_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='所属机构')
    relatedfield_service_role = models.ManyToManyField(Fu_wu_jue_se, related_name='fu_wu_jue_se_for_relatedfield_service_role_zhi_yuan_ji_ben_xin_xi_biao', verbose_name='服务角色')

    class Meta:
        verbose_name = '职员基本信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_cha(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    boolfield_ji_gou_dai_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构代码')
    boolfield_ji_gou_shu_xing = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构属性')
    boolfield_gong_ying_shang_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='供应商编码')
    boolfield_zhuan_ye_fu_wu = models.CharField(max_length=255, null=True, blank=True, verbose_name='专业服务')
    boolfield_gong_ying_shang_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='供应商名称')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    boolfield_xin_yu_ping_ji = models.ForeignKey(Xin_yu_ping_ji, related_name='xin_yu_ping_ji_for_boolfield_xin_yu_ping_ji_fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='信誉评级')

    class Meta:
        verbose_name = '服务分供机构基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class She_bei_ji_ben_xin_xi_ji_lu(HsscBaseFormModel):
    boolfield_she_bei_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备编码')
    boolfield_sheng_chan_chang_jia = models.CharField(max_length=255, null=True, blank=True, verbose_name='生产厂家')
    boolfield_she_bei_fu_wu_dan_wei_hao_shi = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备服务单位耗时')
    boolfield_she_bei_jian_xiu_zhou_qi = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备检修周期')
    boolfield_she_bei_shi_yong_cheng_ben = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备使用成本')
    boolfield_she_bei_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备名称')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    boolfield_she_bei_shi_yong_fu_wu_gong_neng = models.ForeignKey(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_she_bei_shi_yong_fu_wu_gong_neng_she_bei_ji_ben_xin_xi_ji_lu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='设备适用服务功能')

    class Meta:
        verbose_name = '设备基本信息表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Gong_ying_shang_ji_ben_xin_xi_diao_cha(HsscBaseFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    boolfield_gong_ying_shang_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='供应商编码')
    boolfield_zhu_yao_gong_ying_chan_pin = models.CharField(max_length=255, null=True, blank=True, verbose_name='主要供应产品')
    boolfield_gong_huo_zhou_qi = models.CharField(max_length=255, null=True, blank=True, verbose_name='供货周期')
    boolfield_gong_ying_shang_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='供应商名称')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    boolfield_xin_yu_ping_ji = models.ForeignKey(Xin_yu_ping_ji, related_name='xin_yu_ping_ji_for_boolfield_xin_yu_ping_ji_gong_ying_shang_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='信誉评级')

    class Meta:
        verbose_name = '物料供应商基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Yao_pin_ji_ben_xin_xi_biao(HsscBaseFormModel):
    boolfield_yao_pin_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='药品名称')
    boolfield_fu_yong_pin_ci = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药频次')
    boolfield_yao_pin_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='药品编码')
    boolfield_yao_pin_gui_ge = models.CharField(max_length=255, null=True, blank=True, verbose_name='药品规格')
    boolfield_chang_yong_chu_fang_liang = models.CharField(max_length=255, null=True, blank=True, verbose_name='常用处方量')
    boolfield_dui_zhao_yi_bao_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='对照医保名称')
    boolfield_dui_zhao_ji_yao_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='对照基药名称')
    boolfield_huan_suan_gui_ze = models.CharField(max_length=255, null=True, blank=True, verbose_name='换算规则')
    boolfield_yong_yao_zhou_qi = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药疗程')
    boolfield_chu_fang_ji_liang_dan_wei = models.ForeignKey(Yao_pin_dan_wei, related_name='yao_pin_dan_wei_for_boolfield_chu_fang_ji_liang_dan_wei_yao_pin_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='处方计量单位')
    boolfield_ru_ku_ji_liang_dan_wei = models.ForeignKey(Yao_pin_dan_wei, related_name='yao_pin_dan_wei_for_boolfield_ru_ku_ji_liang_dan_wei_yao_pin_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='入库计量单位')
    boolfield_xiao_shou_ji_liang_dan_wei = models.ForeignKey(Yao_pin_dan_wei, related_name='yao_pin_dan_wei_for_boolfield_xiao_shou_ji_liang_dan_wei_yao_pin_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='销售计量单位')
    boolfield_yong_yao_tu_jing = models.ForeignKey(Yong_yao_tu_jing, related_name='yong_yao_tu_jing_for_boolfield_yong_yao_tu_jing_yao_pin_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='用药途径')
    boolfield_yao_pin_fen_lei = models.ForeignKey(Yao_pin_fen_lei, related_name='yao_pin_fen_lei_for_boolfield_yao_pin_fen_lei_yao_pin_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='药品分类')

    class Meta:
        verbose_name = '药品基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Shen_qing_kong_fu_xue_tang_jian_cha_fu_wu(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    boolfield_dang_qian_pai_dui_ren_shu = models.IntegerField(null=True, blank=True, verbose_name='当前排队人数')
    boolfield_dang_qian_pai_dui_ren_shu_standard_value = models.IntegerField(null=True, blank=True, verbose_name='当前排队人数标准值')
    boolfield_dang_qian_pai_dui_ren_shu_up_limit = models.IntegerField(null=True, blank=True, verbose_name='当前排队人数上限')
    boolfield_dang_qian_pai_dui_ren_shu_down_limit = models.IntegerField(null=True, blank=True, verbose_name='当前排队人数下限')
    boolfield_yu_ji_deng_hou_shi_jian = models.IntegerField(null=True, blank=True, verbose_name='预计等候时间')
    boolfield_yu_ji_deng_hou_shi_jian_standard_value = models.IntegerField(null=True, blank=True, verbose_name='预计等候时间标准值')
    boolfield_yu_ji_deng_hou_shi_jian_up_limit = models.IntegerField(null=True, blank=True, verbose_name='预计等候时间上限')
    boolfield_yu_ji_deng_hou_shi_jian_down_limit = models.IntegerField(null=True, blank=True, verbose_name='预计等候时间下限')
    boolfield_ze_ren_ren = models.ForeignKey(Zhi_yuan_ji_ben_xin_xi_biao, related_name='zhi_yuan_ji_ben_xin_xi_biao_for_boolfield_ze_ren_ren_shen_qing_kong_fu_xue_tang_jian_cha_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='责任人')
    boolfield_fu_wu_xiang_mu_ming_cheng = models.ForeignKey(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_fu_wu_xiang_mu_ming_cheng_shen_qing_kong_fu_xue_tang_jian_cha_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='服务项目名称')
    boolfield_an_pai_que_ren = models.ForeignKey(An_pai_que_ren, related_name='an_pai_que_ren_for_boolfield_an_pai_que_ren_shen_qing_kong_fu_xue_tang_jian_cha_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='安排确认')

    class Meta:
        verbose_name = '申请空腹血糖检查服务'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Ju_min_ji_ben_xin_xi_diao_cha(HsscBaseFormModel):
    characterhssc_identification_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='身份证号码')
    characterfield_resident_file_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='居民档案号')
    characterfield_family_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='家庭地址')
    characterfield_medical_ic_card_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='医疗ic卡号')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    datetimefield_date_of_birth = models.DateField(null=True, blank=True, verbose_name='出生日期')
    relatedfield_gender = models.ForeignKey(Gender, related_name='gender_for_relatedfield_gender_ju_min_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='性别')
    relatedfield_nationality = models.ForeignKey(Nationality, related_name='nationality_for_relatedfield_nationality_ju_min_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='民族')
    relatedfield_marital_status = models.ForeignKey(Marital_status, related_name='marital_status_for_relatedfield_marital_status_ju_min_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='婚姻状况')
    relatedfield_education = models.ForeignKey(Education, related_name='education_for_relatedfield_education_ju_min_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='文化程度')
    relatedfield_occupational_status = models.ForeignKey(Occupational_status, related_name='occupational_status_for_relatedfield_occupational_status_ju_min_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='职业状况')
    relatedfield_medical_expenses_burden = models.ManyToManyField(Medical_expenses_burden, related_name='medical_expenses_burden_for_relatedfield_medical_expenses_burden_ju_min_ji_ben_xin_xi_diao_cha', verbose_name='医疗费用负担')
    relatedfield_type_of_residence = models.ForeignKey(Type_of_residence, related_name='type_of_residence_for_relatedfield_type_of_residence_ju_min_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='居住类型')
    relatedfield_blood_type = models.ForeignKey(Blood_type, related_name='blood_type_for_relatedfield_blood_type_ju_min_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='血型')
    relatedfield_signed_family_doctor = models.ForeignKey(Zhi_yuan_ji_ben_xin_xi_biao, related_name='zhi_yuan_ji_ben_xin_xi_biao_for_relatedfield_signed_family_doctor_ju_min_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='签约家庭医生')
    relatedfield_family_relationship = models.ForeignKey(Family_relationship, related_name='family_relationship_for_relatedfield_family_relationship_ju_min_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='家庭成员关系')

    class Meta:
        verbose_name = '居民基本信息调查'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Shu_ye_zhu_she(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    boolfield_fu_yong_pin_ci = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药频次')
    boolfield_yao_pin_gui_ge = models.CharField(max_length=255, null=True, blank=True, verbose_name='药品规格')
    boolfield_chang_yong_chu_fang_liang = models.CharField(max_length=255, null=True, blank=True, verbose_name='常用处方量')
    boolfield_zhi_xing_qian_ming = models.CharField(max_length=255, null=True, blank=True, verbose_name='执行签名')
    boolfield_yong_yao_zhou_qi = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药疗程')
    boolfield_zhu_she_ri_qi = models.DateTimeField(null=True, verbose_name='注射日期')
    relatedfield_drug_name = models.ManyToManyField(Yao_pin_ji_ben_xin_xi_biao, related_name='yao_pin_ji_ben_xin_xi_biao_for_relatedfield_drug_name_shu_ye_zhu_she', verbose_name='药品名')

    class Meta:
        verbose_name = '输液注射'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Qian_yue_fu_wu(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    boolfield_jia_ting_qian_yue_fu_wu_xie_yi = models.CharField(max_length=255, null=True, blank=True, verbose_name='家庭签约服务协议')
    boolfield_qian_yue_que_ren = models.ForeignKey(Qian_yue_que_ren, related_name='qian_yue_que_ren_for_boolfield_qian_yue_que_ren_qian_yue_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='签约确认')
    boolfield_ze_ren_ren = models.ForeignKey(Zhi_yuan_ji_ben_xin_xi_biao, related_name='zhi_yuan_ji_ben_xin_xi_biao_for_boolfield_ze_ren_ren_qian_yue_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='责任人')

    class Meta:
        verbose_name = '签约服务'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class T9001(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    relatedfield_disease_name = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_relatedfield_disease_name_T9001', on_delete=models.CASCADE, null=True, blank=True, verbose_name='疾病名称')
    relatedfield_yi_lou_zhen_duan = models.ManyToManyField(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_relatedfield_yi_lou_zhen_duan_T9001', verbose_name='可能诊断')
    relatedfield_pai_chu_zhen_duan = models.ManyToManyField(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_relatedfield_pai_chu_zhen_duan_T9001', verbose_name='排除诊断')

    class Meta:
        verbose_name = '非胰岛素依赖性糖尿病'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Tang_hua_xue_hong_dan_bai_jian_cha_biao(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    numberfield_tang_hua_xue_hong_dan_bai = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='糖化血红蛋白')
    numberfield_tang_hua_xue_hong_dan_bai_standard_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='糖化血红蛋白标准值')
    numberfield_tang_hua_xue_hong_dan_bai_up_limit = models.DecimalField(max_digits=10, decimal_places=2, default=6.0, null=True, blank=True, verbose_name='糖化血红蛋白上限')
    numberfield_tang_hua_xue_hong_dan_bai_down_limit = models.DecimalField(max_digits=10, decimal_places=2, default=4.0, null=True, blank=True, verbose_name='糖化血红蛋白下限')

    class Meta:
        verbose_name = '糖化血红蛋白检查表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Kong_fu_xue_tang_jian_cha(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    numberfield_kong_fu_xue_tang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='空腹血糖')
    numberfield_kong_fu_xue_tang_standard_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='空腹血糖标准值')
    numberfield_kong_fu_xue_tang_up_limit = models.DecimalField(max_digits=10, decimal_places=2, default=7.0, null=True, blank=True, verbose_name='空腹血糖上限')
    numberfield_kong_fu_xue_tang_down_limit = models.DecimalField(max_digits=10, decimal_places=2, default=3.9, null=True, blank=True, verbose_name='空腹血糖下限')

    class Meta:
        verbose_name = '空腹血糖检查'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Xue_ya_jian_ce(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
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

    def __str__(self):
        return self.customer.name

        
class Tang_niao_bing_cha_ti(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    relatedfield_fundus = models.ForeignKey(Normality, related_name='normality_for_relatedfield_fundus_tang_niao_bing_cha_ti', on_delete=models.CASCADE, null=True, blank=True, verbose_name='眼底')
    relatedfield_left_foot = models.ForeignKey(Dorsal_artery_pulsation, related_name='dorsal_artery_pulsation_for_relatedfield_left_foot_tang_niao_bing_cha_ti', on_delete=models.CASCADE, null=True, blank=True, verbose_name='左脚')
    relatedfield_right_foot = models.ForeignKey(Dorsal_artery_pulsation, related_name='dorsal_artery_pulsation_for_relatedfield_right_foot_tang_niao_bing_cha_ti', on_delete=models.CASCADE, null=True, blank=True, verbose_name='右脚')

    class Meta:
        verbose_name = '糖尿病查体'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class A3502(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    boolfield_niao_tang = models.ForeignKey(Niao_tang, related_name='niao_tang_for_boolfield_niao_tang_A3502', on_delete=models.CASCADE, null=True, blank=True, verbose_name='尿糖')
    boolfield_dan_bai_zhi = models.ForeignKey(Dan_bai_zhi, related_name='dan_bai_zhi_for_boolfield_dan_bai_zhi_A3502', on_delete=models.CASCADE, null=True, blank=True, verbose_name='蛋白质')
    boolfield_tong_ti = models.ForeignKey(Tong_ti, related_name='tong_ti_for_boolfield_tong_ti_A3502', on_delete=models.CASCADE, null=True, blank=True, verbose_name='尿酮体')

    class Meta:
        verbose_name = '尿常规检查'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class A6299(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    boolfield_yi_chuan_ji_bing = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_yi_chuan_ji_bing_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='遗传性疾病')
    boolfield_yi_chuan_bing_shi_cheng_yuan = models.ManyToManyField(Qin_shu_guan_xi, related_name='qin_shu_guan_xi_for_boolfield_yi_chuan_bing_shi_cheng_yuan_A6299', verbose_name='遗传病史成员')
    relatedfield_drug_name = models.ManyToManyField(Yao_pin_ji_ben_xin_xi_biao, related_name='yao_pin_ji_ben_xin_xi_biao_for_relatedfield_drug_name_A6299', verbose_name='药品名')
    boolfield_jia_zu_xing_ji_bing = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_jia_zu_xing_ji_bing_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='家族性疾病')
    boolfield_jia_zu_bing_shi_cheng_yuan = models.ManyToManyField(Qin_shu_guan_xi, related_name='qin_shu_guan_xi_for_boolfield_jia_zu_bing_shi_cheng_yuan_A6299', verbose_name='家族病史成员')
    datetimefield_date = models.DateField(null=True, blank=True, verbose_name='手术日期')
    relatedfield_name_of_operation = models.ForeignKey(Icpc7_treatments, related_name='icpc7_treatments_for_relatedfield_name_of_operation_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='手术名称')
    datetimefield_time_of_diagnosis = models.DateTimeField(null=True, blank=True, verbose_name='确诊时间')
    boolfield_ge_ren_bing_shi = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_ge_ren_bing_shi_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='个人病史')
    boolfield_wai_shang_ri_qi = models.DateField(null=True, blank=True, verbose_name='外伤日期')
    boolfield_wai_shang_xing_ji_bing = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_wai_shang_xing_ji_bing_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='外伤性疾病')
    numberfield_blood_transfusion = models.IntegerField(null=True, blank=True, verbose_name='输血量')
    numberfield_blood_transfusion_standard_value = models.IntegerField(null=True, blank=True, verbose_name='输血量标准值')
    numberfield_blood_transfusion_up_limit = models.IntegerField(default=400.0, null=True, blank=True, verbose_name='输血量上限')
    numberfield_blood_transfusion_down_limit = models.IntegerField(null=True, blank=True, verbose_name='输血量下限')
    boolfield_shu_xue_ri_qi = models.DateField(null=True, blank=True, verbose_name='输血日期')
    relatedfield_personality_tendency = models.ForeignKey(Character, related_name='character_for_relatedfield_personality_tendency_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='性格倾向')
    boolfield_shi_mian_qing_kuang = models.ForeignKey(Shi_mian_qing_kuang, related_name='shi_mian_qing_kuang_for_boolfield_shi_mian_qing_kuang_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='失眠情况')
    boolfield_sheng_huo_gong_zuo_ya_li_qing_kuang = models.ForeignKey(Ya_li_qing_kuang, related_name='ya_li_qing_kuang_for_boolfield_sheng_huo_gong_zuo_ya_li_qing_kuang_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='生活工作压力情况')
    characterfield_working_hours_per_day = models.TextField(max_length=255, null=True, blank=True, verbose_name='每天工作及工作往返总时长')
    relatedfield_are_you_satisfied_with_the_job_and_life = models.ForeignKey(Satisfaction, related_name='satisfaction_for_relatedfield_are_you_satisfied_with_the_job_and_life_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='对目前生活和工作满意吗')
    relatedfield_are_you_satisfied_with_your_adaptability = models.ForeignKey(Satisfaction, related_name='satisfaction_for_relatedfield_are_you_satisfied_with_your_adaptability_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='对自己的适应能力满意吗')
    relatedfield_own_health = models.ForeignKey(State_degree, related_name='state_degree_for_relatedfield_own_health_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='觉得自身健康状况如何')
    relatedfield_compared_to_last_year = models.ForeignKey(Comparative_expression, related_name='comparative_expression_for_relatedfield_compared_to_last_year_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='较之过去一年状态如何')
    relatedfield_sports_preference = models.ForeignKey(Sports_preference, related_name='sports_preference_for_relatedfield_sports_preference_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='运动偏好')
    relatedfield_exercise_time = models.ForeignKey(Exercise_time, related_name='exercise_time_for_relatedfield_exercise_time_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='运动时长')
    relatedfield_have_any_recent_symptoms_of_physical_discomfort = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_relatedfield_have_any_recent_symptoms_of_physical_discomfort_A6299', verbose_name='近来有无身体不适症状')
    characterfield_average_sleep_duration = models.CharField(max_length=255, null=True, blank=True, verbose_name='平均睡眠时长')
    characterfield_duration_of_insomnia = models.CharField(max_length=255, null=True, blank=True, verbose_name='持续失眠时间')
    relatedfield_drinking_frequency = models.ForeignKey(Frequency, related_name='frequency_for_relatedfield_drinking_frequency_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='饮酒频次')
    relatedfield_smoking_frequency = models.ForeignKey(Frequency, related_name='frequency_for_relatedfield_smoking_frequency_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='吸烟频次')
    relatedfield_is_the_living_environment_satisfactory = models.ForeignKey(Satisfaction, related_name='satisfaction_for_relatedfield_is_the_living_environment_satisfactory_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='您对居住环境满意吗')
    relatedfield_is_the_transportation_convenient = models.ForeignKey(Convenience, related_name='convenience_for_relatedfield_is_the_transportation_convenient_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='您所在的社区交通方便吗')

    class Meta:
        verbose_name = '居民健康信息调查'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class A6220(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    boolfield_yuan_wai_jian_kang_ping_gu = models.ForeignKey(Sui_fang_ping_gu, related_name='sui_fang_ping_gu_for_boolfield_yuan_wai_jian_kang_ping_gu_A6220', on_delete=models.CASCADE, null=True, blank=True, verbose_name='监测评估')

    class Meta:
        verbose_name = '监测评估'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class A6202(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    characterfield_supplementary_description_of_the_condition = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')
    relatedfield_symptom_list = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_relatedfield_symptom_list_A6202', verbose_name='症状')

    class Meta:
        verbose_name = '院外辅助问诊'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class T6301(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    boolfield_fu_yong_pin_ci = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药频次')
    boolfield_yao_pin_dan_wei = models.ForeignKey(Yao_pin_dan_wei, related_name='yao_pin_dan_wei_for_boolfield_yao_pin_dan_wei_T6301', on_delete=models.CASCADE, null=True, blank=True, verbose_name='药品单位')
    relatedfield_drinking_frequency = models.ForeignKey(Frequency, related_name='frequency_for_relatedfield_drinking_frequency_T6301', on_delete=models.CASCADE, null=True, blank=True, verbose_name='饮酒频次')
    relatedfield_smoking_frequency = models.ForeignKey(Frequency, related_name='frequency_for_relatedfield_smoking_frequency_T6301', on_delete=models.CASCADE, null=True, blank=True, verbose_name='吸烟频次')
    boolfield_tang_niao_bing_zheng_zhuang = models.ManyToManyField(Tang_niao_bing_zheng_zhuang, related_name='tang_niao_bing_zheng_zhuang_for_boolfield_tang_niao_bing_zheng_zhuang_T6301', verbose_name='糖尿病症状')
    relatedfield_drug_name = models.ManyToManyField(Yao_pin_ji_ben_xin_xi_biao, related_name='yao_pin_ji_ben_xin_xi_biao_for_relatedfield_drug_name_T6301', verbose_name='药品名')
    relatedfield_left_foot = models.ForeignKey(Dorsal_artery_pulsation, related_name='dorsal_artery_pulsation_for_relatedfield_left_foot_T6301', on_delete=models.CASCADE, null=True, blank=True, verbose_name='左脚')
    relatedfield_right_foot = models.ForeignKey(Dorsal_artery_pulsation, related_name='dorsal_artery_pulsation_for_relatedfield_right_foot_T6301', on_delete=models.CASCADE, null=True, blank=True, verbose_name='右脚')
    relatedfield_fundus = models.ForeignKey(Normality, related_name='normality_for_relatedfield_fundus_T6301', on_delete=models.CASCADE, null=True, blank=True, verbose_name='眼底')
    numberfield_systolic_blood_pressure = models.IntegerField(null=True, blank=True, verbose_name='收缩压')
    numberfield_systolic_blood_pressure_standard_value = models.IntegerField(null=True, blank=True, verbose_name='收缩压标准值')
    numberfield_systolic_blood_pressure_up_limit = models.IntegerField(default=139.0, null=True, blank=True, verbose_name='收缩压上限')
    numberfield_systolic_blood_pressure_down_limit = models.IntegerField(default=90.0, null=True, blank=True, verbose_name='收缩压下限')
    numberfield_diastolic_blood_pressure = models.IntegerField(null=True, blank=True, verbose_name='舒张压')
    numberfield_diastolic_blood_pressure_standard_value = models.IntegerField(null=True, blank=True, verbose_name='舒张压标准值')
    numberfield_diastolic_blood_pressure_up_limit = models.IntegerField(default=89.0, null=True, blank=True, verbose_name='舒张压上限')
    numberfield_diastolic_blood_pressure_down_limit = models.IntegerField(default=60.0, null=True, blank=True, verbose_name='舒张压下限')
    numberfield_kong_fu_xue_tang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='空腹血糖')
    numberfield_kong_fu_xue_tang_standard_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='空腹血糖标准值')
    numberfield_kong_fu_xue_tang_up_limit = models.DecimalField(max_digits=10, decimal_places=2, default=7.0, null=True, blank=True, verbose_name='空腹血糖上限')
    numberfield_kong_fu_xue_tang_down_limit = models.DecimalField(max_digits=10, decimal_places=2, default=3.9, null=True, blank=True, verbose_name='空腹血糖下限')

    class Meta:
        verbose_name = '糖尿病一般随访'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class T8901(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    relatedfield_disease_name = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_relatedfield_disease_name_T8901', on_delete=models.CASCADE, null=True, blank=True, verbose_name='疾病名称')
    relatedfield_yi_lou_zhen_duan = models.ManyToManyField(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_relatedfield_yi_lou_zhen_duan_T8901', verbose_name='可能诊断')
    relatedfield_pai_chu_zhen_duan = models.ManyToManyField(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_relatedfield_pai_chu_zhen_duan_T8901', verbose_name='排除诊断')

    class Meta:
        verbose_name = '胰岛素依赖性糖尿病'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class A6218(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    characterfield_supplementary_description_of_the_condition = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')
    relatedfield_symptom_list = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_relatedfield_symptom_list_A6218', verbose_name='症状')

    class Meta:
        verbose_name = '门诊医生问诊'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name


class A6201(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    characterfield_supplementary_description_of_the_condition = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')
    relatedfield_symptom_list = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_relatedfield_symptom_list_A6201', verbose_name='症状')
    boolfield_chang_yong_zheng_zhuang = models.ManyToManyField(Chang_yong_zheng_zhuang, related_name='chang_yong_zheng_zhuang_for_boolfield_chang_yong_zheng_zhuang_A6201', verbose_name='常用症状')

    class Meta:
        verbose_name = '院外咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class A6217(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    characterfield_supplementary_description_of_the_condition = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')
    relatedfield_symptom_list = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_relatedfield_symptom_list_A6217', verbose_name='症状')

    class Meta:
        verbose_name = '院内辅助问诊'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Tang_niao_bing_zi_wo_jian_ce(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    numberfield_kong_fu_xue_tang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='空腹血糖')
    numberfield_kong_fu_xue_tang_standard_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='空腹血糖标准值')
    numberfield_kong_fu_xue_tang_up_limit = models.DecimalField(max_digits=10, decimal_places=2, default=7.0, null=True, blank=True, verbose_name='空腹血糖上限')
    numberfield_kong_fu_xue_tang_down_limit = models.DecimalField(max_digits=10, decimal_places=2, default=3.9, null=True, blank=True, verbose_name='空腹血糖下限')

    class Meta:
        verbose_name = '糖尿病自我监测'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Yao_shi_fu_wu(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    relatedfield_disease_name = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_relatedfield_disease_name_yao_shi_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='疾病名称')
    boolfield_shi_fou_ji_xu_shi_yong = models.ForeignKey(Ji_xu_shi_yong_qing_kuang, related_name='ji_xu_shi_yong_qing_kuang_for_boolfield_shi_fou_ji_xu_shi_yong_yao_shi_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='是否继续使用')
    relatedfield_drug_name = models.ManyToManyField(Yao_pin_ji_ben_xin_xi_biao, related_name='yao_pin_ji_ben_xin_xi_biao_for_relatedfield_drug_name_yao_shi_fu_wu', verbose_name='药品名')

    class Meta:
        verbose_name = '用药提醒服务'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Tang_niao_bing_zhuan_yong_wen_zhen(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    characterfield_supplementary_description_of_the_condition = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')
    relatedfield_symptom_list = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_relatedfield_symptom_list_tang_niao_bing_zhuan_yong_wen_zhen', verbose_name='症状')
    boolfield_tang_niao_bing_zheng_zhuang = models.ManyToManyField(Tang_niao_bing_zheng_zhuang, related_name='tang_niao_bing_zheng_zhuang_for_boolfield_tang_niao_bing_zheng_zhuang_tang_niao_bing_zhuan_yong_wen_zhen', verbose_name='糖尿病症状')

    class Meta:
        verbose_name = '糖尿病专用问诊'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class A3101(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
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
    relatedfield_athletic_ability = models.ForeignKey(Exercise_time, related_name='exercise_time_for_relatedfield_athletic_ability_A3101', on_delete=models.CASCADE, null=True, blank=True, verbose_name='运动能力')
    relatedfield_left_ear_hearing = models.ForeignKey(Hearing, related_name='hearing_for_relatedfield_left_ear_hearing_A3101', on_delete=models.CASCADE, null=True, blank=True, verbose_name='左耳听力')
    relatedfield_right_ear_hearing = models.ForeignKey(Hearing, related_name='hearing_for_relatedfield_right_ear_hearing_A3101', on_delete=models.CASCADE, null=True, blank=True, verbose_name='右耳听力')
    relatedfield_lips = models.ForeignKey(Lips, related_name='lips_for_relatedfield_lips_A3101', on_delete=models.CASCADE, null=True, blank=True, verbose_name='口唇')
    relatedfield_dentition = models.ForeignKey(Dentition, related_name='dentition_for_relatedfield_dentition_A3101', on_delete=models.CASCADE, null=True, blank=True, verbose_name='齿列')
    relatedfield_pharynx = models.ForeignKey(Pharynx, related_name='pharynx_for_relatedfield_pharynx_A3101', on_delete=models.CASCADE, null=True, blank=True, verbose_name='咽部')
    relatedfield_lower_extremity_edema = models.ForeignKey(Edema, related_name='edema_for_relatedfield_lower_extremity_edema_A3101', on_delete=models.CASCADE, null=True, blank=True, verbose_name='下肢水肿')

    class Meta:
        verbose_name = '体格检查/部分健康评估'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class A6502(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    datetimefield_ri_qi_shi_jian = models.DateTimeField(null=True, verbose_name='预约时间')
    boolfield_qian_dao_que_ren = models.ForeignKey(Qian_dao_que_ren, related_name='qian_dao_que_ren_for_boolfield_qian_dao_que_ren_A6502', on_delete=models.CASCADE, null=True, blank=True, verbose_name='签到确认')
    boolfield_ze_ren_ren = models.ForeignKey(Zhi_yuan_ji_ben_xin_xi_biao, related_name='zhi_yuan_ji_ben_xin_xi_biao_for_boolfield_ze_ren_ren_A6502', on_delete=models.CASCADE, null=True, blank=True, verbose_name='责任人')

    class Meta:
        verbose_name = '门诊分诊'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class A6501(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    datetimefield_ri_qi_shi_jian = models.DateTimeField(null=True, verbose_name='预约时间')
    boolfield_ze_ren_ren = models.ForeignKey(Zhi_yuan_ji_ben_xin_xi_biao, related_name='zhi_yuan_ji_ben_xin_xi_biao_for_boolfield_ze_ren_ren_A6501', on_delete=models.CASCADE, null=True, blank=True, verbose_name='责任人')

    class Meta:
        verbose_name = '代人预约挂号'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Men_zhen_chu_fang_biao(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=True, verbose_name='性别')
    characterfield_age = models.CharField(max_length=255, null=True, blank=True, verbose_name='年龄')
    boolfield_fu_yong_pin_ci = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药频次')
    boolfield_chang_yong_chu_fang_liang = models.CharField(max_length=255, null=True, blank=True, verbose_name='常用处方量')
    boolfield_yong_yao_zhou_qi = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药疗程')
    boolfield_yong_yao_tu_jing = models.ForeignKey(Yong_yao_tu_jing, related_name='yong_yao_tu_jing_for_boolfield_yong_yao_tu_jing_men_zhen_chu_fang_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='用药途径')
    relatedfield_drug_name = models.ManyToManyField(Yao_pin_ji_ben_xin_xi_biao, related_name='yao_pin_ji_ben_xin_xi_biao_for_relatedfield_drug_name_men_zhen_chu_fang_biao', verbose_name='药品名')

    class Meta:
        verbose_name = '药物干预'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name
