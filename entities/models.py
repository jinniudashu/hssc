from django.db import models
from core.models import HsscFormModel
from icpc.models import *
from dictionaries.models import *


class Ji_gou_ji_ben_xin_xi_biao(HsscFormModel):
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


class A6203(HsscFormModel):
    characterhssc_identification_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='身份证号码')
    characterfield_resident_file_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='居民档案号')
    characterfield_family_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='家庭地址')
    characterfield_medical_ic_card_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='医疗ic卡号')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    datetimefield_date_of_birth = models.DateField(null=True, blank=True, verbose_name='出生日期')
    relatedfield_gender = models.ForeignKey(Gender, related_name='gender_for_relatedfield_gender_A6203', on_delete=models.CASCADE, null=True, blank=True, verbose_name='性别')
    relatedfield_nationality = models.ForeignKey(Nationality, related_name='nationality_for_relatedfield_nationality_A6203', on_delete=models.CASCADE, null=True, blank=True, verbose_name='民族')
    relatedfield_marital_status = models.ForeignKey(Marital_status, related_name='marital_status_for_relatedfield_marital_status_A6203', on_delete=models.CASCADE, null=True, blank=True, verbose_name='婚姻状况')
    relatedfield_education = models.ForeignKey(Education, related_name='education_for_relatedfield_education_A6203', on_delete=models.CASCADE, null=True, blank=True, verbose_name='文化程度')
    relatedfield_occupational_status = models.ForeignKey(Occupational_status, related_name='occupational_status_for_relatedfield_occupational_status_A6203', on_delete=models.CASCADE, null=True, blank=True, verbose_name='职业状况')
    relatedfield_medical_expenses_burden = models.ManyToManyField(Medical_expenses_burden, related_name='medical_expenses_burden_for_relatedfield_medical_expenses_burden_A6203', verbose_name='医疗费用负担')
    relatedfield_type_of_residence = models.ForeignKey(Type_of_residence, related_name='type_of_residence_for_relatedfield_type_of_residence_A6203', on_delete=models.CASCADE, null=True, blank=True, verbose_name='居住类型')
    relatedfield_blood_type = models.ForeignKey(Blood_type, related_name='blood_type_for_relatedfield_blood_type_A6203', on_delete=models.CASCADE, null=True, blank=True, verbose_name='血型')
    relatedfield_signed_family_doctor = models.ForeignKey('Zhi_yuan_ji_ben_xin_xi_biao', related_name='zhi_yuan_ji_ben_xin_xi_biao_for_relatedfield_signed_family_doctor_A6203', on_delete=models.CASCADE, null=True, blank=True, verbose_name='签约家庭医生')
    relatedfield_family_relationship = models.ForeignKey(Family_relationship, related_name='family_relationship_for_relatedfield_family_relationship_A6203', on_delete=models.CASCADE, null=True, blank=True, verbose_name='家庭成员关系')
    class Meta:
        verbose_name = '个人基本信息'
        verbose_name_plural = verbose_name
        

class Yao_pin_ji_ben_xin_xi_biao(HsscFormModel):
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
        verbose_name = '药品基本信息表'
        verbose_name_plural = verbose_name
        

class Zhi_yuan_ji_ben_xin_xi_biao(HsscFormModel):
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
                

class She_bei_ji_ben_xin_xi_biao(HsscFormModel):
    boolfield_she_bei_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备编码')
    boolfield_sheng_chan_chang_jia = models.CharField(max_length=255, null=True, blank=True, verbose_name='生产厂家')
    boolfield_she_bei_fu_wu_dan_wei_hao_shi = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备服务单位耗时')
    boolfield_she_bei_jian_xiu_zhou_qi = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备检修周期')
    boolfield_she_bei_shi_yong_cheng_ben = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备使用成本')
    boolfield_she_bei_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备名称')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    boolfield_she_bei_shi_yong_fu_wu_gong_neng = models.ForeignKey(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_she_bei_shi_yong_fu_wu_gong_neng_she_bei_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='设备适用服务功能')
    class Meta:
        verbose_name = '设备基本信息表'
        verbose_name_plural = verbose_name
        

class Wu_liu_gong_ying_shang_ji_ben_xin_xi_biao(HsscFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    boolfield_gong_ying_shang_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='供应商编码')
    boolfield_zhu_yao_gong_ying_chan_pin = models.CharField(max_length=255, null=True, blank=True, verbose_name='主要供应产品')
    boolfield_gong_huo_zhou_qi = models.CharField(max_length=255, null=True, blank=True, verbose_name='供货周期')
    boolfield_gong_ying_shang_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='供应商名称')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    boolfield_xin_yu_ping_ji = models.ForeignKey(Xin_yu_ping_ji, related_name='xin_yu_ping_ji_for_boolfield_xin_yu_ping_ji_wu_liu_gong_ying_shang_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='信誉评级')
    class Meta:
        verbose_name = '物料供应商基本信息表'
        verbose_name_plural = verbose_name
        

