from django.db import models

from icpc.models import *
from dictionaries.models import *
from core.models import HsscFormModel, HsscBaseFormModel


# **********************************************************************************************************************
# Service基本信息表单Model
# **********************************************************************************************************************
class Ji_gou_ji_ben_xin_xi_biao(HsscBaseFormModel):
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构联系地址')
    boolfield_ji_gou_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构编码')
    boolfield_ji_gou_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构名称')
    boolfield_ji_gou_dai_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构代码')
    boolfield_ji_gou_shu_xing = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构属性')
    boolfield_ji_gou_ceng_ji = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构层级')
    boolfield_suo_zai_hang_zheng_qu_hua_dai_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='所在行政区划代码')
    boolfield_xing_zheng_qu_hua_gui_shu = models.CharField(max_length=255, null=True, blank=True, verbose_name='行政区划归属')
    boolfield_fa_ding_fu_ze_ren = models.CharField(max_length=255, null=True, blank=True, verbose_name='法定负责人')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构联系电话')

    class Meta:
        verbose_name = '机构基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Li_pei_shen_qing_shu_shen_he(HsscFormModel):
    characterfield_name = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人性别')
    datetimefield_date_of_birth = models.DateField(null=True, blank=False, verbose_name='出生日期')
    boolfield_chang_zhu_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='常住地址')
    characterhssc_identification_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='证件号码')
    relatedfield_gender = models.ForeignKey(Gender, related_name='gender_for_relatedfield_gender_li_pei_shen_qing_shu_shen_he', on_delete=models.CASCADE, null=True, blank=True, verbose_name='性别')
    boolfield_zheng_jian_lei_xing = models.ForeignKey(Zheng_jian_lei_xing, related_name='zheng_jian_lei_xing_for_boolfield_zheng_jian_lei_xing_li_pei_shen_qing_shu_shen_he', on_delete=models.CASCADE, null=True, blank=True, verbose_name='证件类型')
    boolfield_shen_qing_ren_xing_ming = models.CharField(max_length=255, null=True, blank=True, verbose_name='申请人姓名')
    boolfield_yu_chu_xian_ren_guan_xi = models.ForeignKey(Yu_chu_xian_ren_guan_xi, related_name='yu_chu_xian_ren_guan_xi_for_boolfield_yu_chu_xian_ren_guan_xi_li_pei_shen_qing_shu_shen_he', on_delete=models.CASCADE, null=True, blank=True, verbose_name='与出险人关系')
    boolfield_zheng_jian_you_xiao_qi = models.CharField(max_length=255, null=True, blank=True, verbose_name='证件有效期')
    boolfield_guo_ji_di_qu = models.CharField(max_length=255, null=True, blank=True, verbose_name='国籍/地区')
    boolfield_hang_ye = models.CharField(max_length=255, null=True, blank=True, verbose_name='行业')
    boolfield_zhi_ye = models.CharField(max_length=255, null=True, blank=True, verbose_name='职业')
    boolfield_chang_zhu_di_zhi = models.CharField(max_length=255, null=True, blank=True, verbose_name='常住地址')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    boolfield_qian_shu_que_ren = models.ForeignKey(Qian_shu_que_ren, related_name='qian_shu_que_ren_for_boolfield_qian_shu_que_ren_li_pei_shen_qing_shu_shen_he', on_delete=models.CASCADE, null=True, blank=False, verbose_name='签署确认')
    boolfield_tui_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='退单原因')

    class Meta:
        verbose_name = '理赔申请书审核'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Li_pei_dui_zhang_dan_shen_he(HsscFormModel):
    characterfield_name = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人性别')
    datetimefield_date_of_birth = models.DateField(null=True, blank=False, verbose_name='出生日期')
    boolfield_chang_zhu_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='常住地址')
    boolfield_qian_shu_que_ren = models.ForeignKey(Qian_shu_que_ren, related_name='qian_shu_que_ren_for_boolfield_qian_shu_que_ren_li_pei_dui_zhang_dan_shen_he', on_delete=models.CASCADE, null=True, blank=False, verbose_name='签署确认')
    boolfield_tui_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='退单原因')
    characterfield_age = models.CharField(max_length=255, null=True, blank=False, verbose_name='年龄')
    datetimefield_date_of_birth = models.DateField(null=True, blank=False, verbose_name='出生日期')
    relatedfield_gender = models.ForeignKey(Gender, related_name='gender_for_relatedfield_gender_li_pei_dui_zhang_dan_shen_he', on_delete=models.CASCADE, null=True, blank=False, verbose_name='性别')
    boolfield_zheng_jian_lei_xing = models.ForeignKey(Zheng_jian_lei_xing, related_name='zheng_jian_lei_xing_for_boolfield_zheng_jian_lei_xing_li_pei_dui_zhang_dan_shen_he', on_delete=models.CASCADE, null=True, blank=False, verbose_name='证件类型')
    boolfield_xu_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='序号')
    boolfield_bao_dan_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='保单号')
    boolfield_bao_an_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='报案时间')
    boolfield_chu_xian_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='出险时间')
    boolfield_bao_an_ren_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=False, verbose_name='报案人联系电话')
    boolfield_chu_xian_ren_xing_ming = models.CharField(max_length=255, null=True, blank=False, verbose_name='出险人姓名')
    boolfield_chu_xian_di_dian = models.CharField(max_length=255, null=True, blank=False, verbose_name='出险地点')
    boolfield_chu_xian_di_dian_sheng_ji_bie = models.CharField(max_length=255, null=True, blank=False, verbose_name='出险地点_省级别')
    boolfield_chu_xian_di_dian_shi_ji_bie = models.CharField(max_length=255, null=True, blank=False, verbose_name='出险地点_市级别')
    boolfield_shi_gu_gai_kuo = models.CharField(max_length=255, null=True, blank=False, verbose_name='事故概括')
    boolfield_bei_bao_xian_ren_zheng_jian_hao_ma = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保险人证件号码')
    boolfield_gui_shu_cheng_shi = models.CharField(max_length=255, null=True, blank=False, verbose_name='归属城市')
    boolfield_yi_yuan_xin_xi = models.CharField(max_length=255, null=True, blank=False, verbose_name='医院信息')
    boolfield_ji_bing_xin_xi = models.CharField(max_length=255, null=True, blank=False, verbose_name='疾病信息')
    boolfield_li_pei_jin_e_bao_xiao_jian_mian_jin_e = models.CharField(max_length=255, null=True, blank=False, verbose_name='理赔金额_报销/减免金额')
    boolfield_li_pei_fang_shi = models.CharField(max_length=255, null=True, blank=False, verbose_name='理赔方式')
    boolfield_bei_zhu = models.CharField(max_length=255, null=True, blank=False, verbose_name='备注')
    boolfield_bao_an_ren = models.CharField(max_length=255, null=True, blank=False, verbose_name='报案人')

    class Meta:
        verbose_name = '理赔对账单审核'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Li_pei_men_zhen_ji_lu_shen_he(HsscBaseFormModel):
    boolfield_she_bei_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备编码')
    boolfield_sheng_chan_chang_jia = models.CharField(max_length=255, null=True, blank=True, verbose_name='生产厂家')
    boolfield_she_bei_fu_wu_dan_wei_hao_shi = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备服务单位耗时')
    boolfield_she_bei_jian_xiu_zhou_qi = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备检修周期')
    boolfield_she_bei_shi_yong_cheng_ben = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备使用成本')
    boolfield_she_bei_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备名称')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构联系电话')
    boolfield_she_bei_shi_yong_fu_wu_gong_neng = models.ForeignKey(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_she_bei_shi_yong_fu_wu_gong_neng_li_pei_men_zhen_ji_lu_shen_he', on_delete=models.CASCADE, null=True, blank=True, verbose_name='设备适用服务功能')
    relatedfield_symptom_list = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_relatedfield_symptom_list_li_pei_men_zhen_ji_lu_shen_he', blank=True, verbose_name='症状')
    boolfield_zhen_duan = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_zhen_duan_li_pei_men_zhen_ji_lu_shen_he', on_delete=models.CASCADE, null=True, blank=False, verbose_name='诊断')
    boolfield_jian_cha_xiang_mu = models.ManyToManyField(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_jian_cha_xiang_mu_li_pei_men_zhen_ji_lu_shen_he', blank=False, verbose_name='检查项目')
    boolfield_zhi_liao_xiang_mu = models.ManyToManyField(Icpc7_treatments, related_name='icpc7_treatments_for_boolfield_zhi_liao_xiang_mu_li_pei_men_zhen_ji_lu_shen_he', blank=False, verbose_name='治疗项目')
    boolfield_qi_ta_fu_wu_xiang_mu = models.ManyToManyField(Icpc8_other_health_interventions, related_name='icpc8_other_health_interventions_for_boolfield_qi_ta_fu_wu_xiang_mu_li_pei_men_zhen_ji_lu_shen_he', blank=True, verbose_name='其他健康干预服务')
    boolfield_fei_yong_he_ji = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='费用合计')
    boolfield_men_zhen_bing_li_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='门诊病历附件')

    class Meta:
        verbose_name = '理赔门诊记录审核'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Li_pei_fei_yong_hui_zong_dan_shen_he(HsscFormModel):
    characterfield_name = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人性别')
    datetimefield_date_of_birth = models.DateField(null=True, blank=False, verbose_name='出生日期')
    boolfield_chang_zhu_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='常住地址')
    boolfield_fei_yong_he_ji = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='费用合计')
    boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu = models.ManyToManyField(Fu_wu_xiang_mu, related_name='fu_wu_xiang_mu_for_boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu_li_pei_fei_yong_hui_zong_dan_shen_he', blank=False, verbose_name='保单内服务收费项目')
    boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu = models.ManyToManyField(Fu_wu_xiang_mu, related_name='fu_wu_xiang_mu_for_boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu_li_pei_fei_yong_hui_zong_dan_shen_he', blank=False, verbose_name='保单外服务收费项目')
    boolfield_fei_yong = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='保单内服务费用')
    boolfield_bao_dan_wai_fu_wu_fei_yong = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='保单外服务费用')
    boolfield_fei_yong_qing_dan_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='费用清单附件')
    boolfield_qian_shu_que_ren = models.ForeignKey(Qian_shu_que_ren, related_name='qian_shu_que_ren_for_boolfield_qian_shu_que_ren_li_pei_fei_yong_hui_zong_dan_shen_he', on_delete=models.CASCADE, null=True, blank=False, verbose_name='签署确认')
    boolfield_tui_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='退单原因')

    class Meta:
        verbose_name = '理赔费用汇总单审核'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Man_yi_du_diao_cha(HsscFormModel):
    characterfield_name = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人性别')
    datetimefield_date_of_birth = models.DateField(null=True, blank=False, verbose_name='出生日期')
    boolfield_chang_zhu_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='常住地址')
    boolfield_you_dai_gai_jin_de_fu_wu = models.CharField(max_length=255, null=True, blank=True, verbose_name='有待改进的服务')
    boolfield_yi_liao_fu_wu_ji_neng_xiang_mu_ping_fen = models.ForeignKey(Ping_fen, related_name='ping_fen_for_boolfield_yi_liao_fu_wu_ji_neng_xiang_mu_ping_fen_man_yi_du_diao_cha', on_delete=models.CASCADE, null=True, blank=False, verbose_name='医疗服务技能项目评分')
    boolfield_ping_tai_fu_wu_xiang_mu_ping_fen = models.ForeignKey(Ping_fen, related_name='ping_fen_for_boolfield_ping_tai_fu_wu_xiang_mu_ping_fen_man_yi_du_diao_cha', on_delete=models.CASCADE, null=True, blank=False, verbose_name='平台服务项目评分')
    boolfield_xi_wang_zeng_jia_de_fu_wu_xiang_mu = models.CharField(max_length=255, null=True, blank=True, verbose_name='希望增加的服务项目')
    boolfield_fu_wu_xiao_lv_ping_fen = models.ForeignKey(Ping_fen, related_name='ping_fen_for_boolfield_fu_wu_xiao_lv_ping_fen_man_yi_du_diao_cha', on_delete=models.CASCADE, null=True, blank=False, verbose_name='服务效率评分')
    boolfield_fu_wu_liu_cheng_ping_fen = models.ForeignKey(Ping_fen, related_name='ping_fen_for_boolfield_fu_wu_liu_cheng_ping_fen_man_yi_du_diao_cha', on_delete=models.CASCADE, null=True, blank=False, verbose_name='服务流程评分')

    class Meta:
        verbose_name = '满意度调查'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Zhen_hou_sui_fang(HsscFormModel):
    characterfield_name = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人性别')
    datetimefield_date_of_birth = models.DateField(null=True, blank=False, verbose_name='出生日期')
    boolfield_chang_zhu_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='常住地址')
    boolfield_deng_hou_qing_kuang = models.ForeignKey(Deng_hou_shi_jian, related_name='deng_hou_shi_jian_for_boolfield_deng_hou_qing_kuang_zhen_hou_sui_fang', on_delete=models.CASCADE, null=True, blank=True, verbose_name='等候情况')
    boolfield_cun_zai_de_wen_ti = models.CharField(max_length=255, null=True, blank=True, verbose_name='存在的问题')
    boolfield_nin_de_dan_xin_he_gu_lv = models.CharField(max_length=255, null=True, blank=True, verbose_name='您的担心和顾虑')
    boolfield_fu_wu_xiao_guo_ping_jia = models.ForeignKey(Fu_wu_xiao_guo_ping_jia, related_name='fu_wu_xiao_guo_ping_jia_for_boolfield_fu_wu_xiao_guo_ping_jia_zhen_hou_sui_fang', on_delete=models.CASCADE, null=True, blank=True, verbose_name='治疗感受/效果评价')
    boolfield_you_dai_gai_jin_de_fu_wu = models.CharField(max_length=255, null=True, blank=True, verbose_name='有待改进的服务')
    boolfield_nin_hai_xu_yao_de_fu_wu = models.CharField(max_length=255, null=True, blank=True, verbose_name='您还需要的服务')

    class Meta:
        verbose_name = '诊后回访'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Zhen_jian_sui_fang(HsscFormModel):
    characterfield_name = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人性别')
    datetimefield_date_of_birth = models.DateField(null=True, blank=False, verbose_name='出生日期')
    boolfield_chang_zhu_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='常住地址')
    boolfield_zhi_liao_jian_gou_tong_qing_kuang = models.ForeignKey(Gou_tong_qing_kuang, related_name='gou_tong_qing_kuang_for_boolfield_zhi_liao_jian_gou_tong_qing_kuang_zhen_jian_sui_fang', on_delete=models.CASCADE, null=True, blank=True, verbose_name='治疗间沟通情况')
    boolfield_deng_hou_qing_kuang = models.ForeignKey(Deng_hou_shi_jian, related_name='deng_hou_shi_jian_for_boolfield_deng_hou_qing_kuang_zhen_jian_sui_fang', on_delete=models.CASCADE, null=True, blank=True, verbose_name='等候情况')
    boolfield_jie_dai_fu_wu = models.ForeignKey(Jie_dai_fu_wu, related_name='jie_dai_fu_wu_for_boolfield_jie_dai_fu_wu_zhen_jian_sui_fang', on_delete=models.CASCADE, null=True, blank=True, verbose_name='接待服务')
    boolfield_cun_zai_de_wen_ti = models.CharField(max_length=255, null=True, blank=True, verbose_name='存在的问题')
    boolfield_qi_ta_xu_qiu = models.CharField(max_length=255, null=True, blank=True, verbose_name='其他需求')
    boolfield_nin_de_dan_xin_he_gu_lv = models.CharField(max_length=255, null=True, blank=True, verbose_name='您的担心和顾虑')
    boolfield_nin_xiang_yao_de_bang_zhu = models.CharField(max_length=255, null=True, blank=True, verbose_name='您想要的帮助')
    boolfield_fu_wu_xiao_guo_ping_jia = models.ForeignKey(Fu_wu_xiao_guo_ping_jia, related_name='fu_wu_xiao_guo_ping_jia_for_boolfield_fu_wu_xiao_guo_ping_jia_zhen_jian_sui_fang', on_delete=models.CASCADE, null=True, blank=False, verbose_name='治疗感受/效果评价')

    class Meta:
        verbose_name = '诊间随访'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Men_zhen_ji_lu(HsscBaseFormModel):
    relatedfield_symptom_list = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_relatedfield_symptom_list_men_zhen_ji_lu', blank=True, verbose_name='症状')
    boolfield_zhen_duan = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_zhen_duan_men_zhen_ji_lu', on_delete=models.CASCADE, null=True, blank=False, verbose_name='诊断')
    boolfield_jian_cha_xiang_mu = models.ManyToManyField(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_jian_cha_xiang_mu_men_zhen_ji_lu', blank=False, verbose_name='检查项目')
    boolfield_zhi_liao_xiang_mu = models.ManyToManyField(Icpc7_treatments, related_name='icpc7_treatments_for_boolfield_zhi_liao_xiang_mu_men_zhen_ji_lu', blank=False, verbose_name='治疗项目')
    boolfield_qi_ta_fu_wu_xiang_mu = models.ManyToManyField(Icpc8_other_health_interventions, related_name='icpc8_other_health_interventions_for_boolfield_qi_ta_fu_wu_xiang_mu_men_zhen_ji_lu', blank=True, verbose_name='其他健康干预服务')
    boolfield_fei_yong_he_ji = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='费用合计')
    boolfield_men_zhen_bing_li_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='门诊病历附件')
    characterhssc_identification_number = models.CharField(max_length=255, null=True, blank=False, verbose_name='证件号码')
    characterfield_name = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人性别')
    datetimefield_date_of_birth = models.DateField(null=True, blank=False, verbose_name='出生日期')
    boolfield_bao_xian_you_xiao_qi = models.DateField(null=True, blank=False, verbose_name='保险有效期')
    boolfield_zheng_jian_lei_xing = models.ForeignKey(Zheng_jian_lei_xing, related_name='zheng_jian_lei_xing_for_boolfield_zheng_jian_lei_xing_men_zhen_ji_lu', on_delete=models.CASCADE, null=True, blank=False, verbose_name='证件类型')
    boolfield_xu_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='序号')
    boolfield_bao_dan_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='保单号')
    boolfield_bao_xian_ze_ren = models.CharField(max_length=255, null=True, blank=False, verbose_name='保险责任')
    boolfield_chang_zhu_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='常住地址')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=False, verbose_name='联系电话')

    class Meta:
        verbose_name = '门诊记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Yu_yue_tong_zhi(HsscFormModel):
    characterfield_name = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人性别')
    datetimefield_date_of_birth = models.DateField(null=True, blank=False, verbose_name='出生日期')
    boolfield_chang_zhu_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='常住地址')
    characterfield_contact_address = models.CharField(max_length=255, null=True, blank=False, verbose_name='机构联系地址')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=False, verbose_name='机构联系电话')
    datetimefield_ri_qi_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='预约时间')
    boolfield_ze_ren_ren = models.ForeignKey(Ji_gou_ji_ben_xin_xi_biao, related_name='ji_gou_ji_ben_xin_xi_biao_for_boolfield_ze_ren_ren_yu_yue_tong_zhi', on_delete=models.CASCADE, null=True, blank=False, verbose_name='就诊机构')
    boolfield_jiu_zhen_yi_sheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='就诊医生')
    boolfield_yu_yue_xu_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='预约序号')

    class Meta:
        verbose_name = '预约通知'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Fen_zhen_que_ren(HsscBaseFormModel):
    datetimefield_ri_qi_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='预约时间')
    boolfield_ze_ren_ren = models.ForeignKey(Ji_gou_ji_ben_xin_xi_biao, related_name='ji_gou_ji_ben_xin_xi_biao_for_boolfield_ze_ren_ren_fen_zhen_que_ren', on_delete=models.CASCADE, null=True, blank=True, verbose_name='就诊机构')
    boolfield_jiu_zhen_wen_ti = models.CharField(max_length=255, null=True, blank=False, verbose_name='就诊问题')
    boolfield_shi_yong_bao_xian_chan_pin = models.ManyToManyField(Bao_xian_chan_pin, related_name='bao_xian_chan_pin_for_boolfield_shi_yong_bao_xian_chan_pin_fen_zhen_que_ren', blank=True, verbose_name='使用服务产品')
    boolfield_fu_jia_fu_wu_yao_qiu = models.CharField(max_length=255, null=True, blank=True, verbose_name='附加服务要求')
    characterhssc_identification_number = models.CharField(max_length=255, null=True, blank=False, verbose_name='证件号码')
    characterfield_name = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人性别')
    datetimefield_date_of_birth = models.DateField(null=True, blank=False, verbose_name='出生日期')
    boolfield_bao_xian_you_xiao_qi = models.DateField(null=True, blank=False, verbose_name='保险有效期')
    boolfield_zheng_jian_lei_xing = models.ForeignKey(Zheng_jian_lei_xing, related_name='zheng_jian_lei_xing_for_boolfield_zheng_jian_lei_xing_fen_zhen_que_ren', on_delete=models.CASCADE, null=True, blank=False, verbose_name='证件类型')
    boolfield_xu_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='序号')
    boolfield_bao_dan_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='保单号')
    boolfield_bao_xian_ze_ren = models.CharField(max_length=255, null=True, blank=False, verbose_name='保险责任')
    boolfield_chang_zhu_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='常住地址')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=False, verbose_name='联系电话')
    boolfield_fen_zhen_que_ren = models.ForeignKey(Qian_dao_que_ren, related_name='qian_dao_que_ren_for_boolfield_fen_zhen_que_ren_fen_zhen_que_ren', on_delete=models.CASCADE, null=True, blank=False, verbose_name='到达确认')
    boolfield_shen_fen_zheng_jian_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='身份证件附件')

    class Meta:
        verbose_name = '到店确认'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Yu_yue_que_ren(HsscBaseFormModel):
    boolfield_qian_dao_que_ren = models.ForeignKey(Jie_dan_que_ren, related_name='jie_dan_que_ren_for_boolfield_qian_dao_que_ren_yu_yue_que_ren', on_delete=models.CASCADE, null=True, blank=False, verbose_name='接单确认')
    datetimefield_ri_qi_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='预约时间')
    boolfield_ze_ren_ren = models.ForeignKey(Ji_gou_ji_ben_xin_xi_biao, related_name='ji_gou_ji_ben_xin_xi_biao_for_boolfield_ze_ren_ren_yu_yue_que_ren', on_delete=models.CASCADE, null=True, blank=True, verbose_name='就诊机构')
    boolfield_jiu_zhen_wen_ti = models.CharField(max_length=255, null=True, blank=False, verbose_name='就诊问题')
    boolfield_shi_yong_bao_xian_chan_pin = models.ManyToManyField(Bao_xian_chan_pin, related_name='bao_xian_chan_pin_for_boolfield_shi_yong_bao_xian_chan_pin_yu_yue_que_ren', blank=True, verbose_name='使用服务产品')
    boolfield_fu_jia_fu_wu_yao_qiu = models.CharField(max_length=255, null=True, blank=True, verbose_name='附加服务要求')
    characterhssc_identification_number = models.CharField(max_length=255, null=True, blank=False, verbose_name='证件号码')
    characterfield_name = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人性别')
    datetimefield_date_of_birth = models.DateField(null=True, blank=False, verbose_name='出生日期')
    boolfield_bao_xian_you_xiao_qi = models.DateField(null=True, blank=False, verbose_name='保险有效期')
    boolfield_zheng_jian_lei_xing = models.ForeignKey(Zheng_jian_lei_xing, related_name='zheng_jian_lei_xing_for_boolfield_zheng_jian_lei_xing_yu_yue_que_ren', on_delete=models.CASCADE, null=True, blank=False, verbose_name='证件类型')
    boolfield_xu_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='序号')
    boolfield_bao_dan_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='保单号')
    boolfield_bao_xian_ze_ren = models.CharField(max_length=255, null=True, blank=False, verbose_name='保险责任')
    boolfield_chang_zhu_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='常住地址')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=False, verbose_name='联系电话')

    class Meta:
        verbose_name = '预约确认'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Yu_yue_an_pai(HsscBaseFormModel):
    datetimefield_ri_qi_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='预约时间')
    boolfield_ze_ren_ren = models.ForeignKey(Ji_gou_ji_ben_xin_xi_biao, related_name='ji_gou_ji_ben_xin_xi_biao_for_boolfield_ze_ren_ren_yu_yue_an_pai', on_delete=models.CASCADE, null=True, blank=True, verbose_name='就诊机构')
    boolfield_jiu_zhen_wen_ti = models.CharField(max_length=255, null=True, blank=False, verbose_name='就诊问题')
    boolfield_shi_yong_bao_xian_chan_pin = models.ManyToManyField(Bao_xian_chan_pin, related_name='bao_xian_chan_pin_for_boolfield_shi_yong_bao_xian_chan_pin_yu_yue_an_pai', blank=True, verbose_name='使用服务产品')
    boolfield_fu_jia_fu_wu_yao_qiu = models.CharField(max_length=255, null=True, blank=True, verbose_name='附加服务要求')
    characterhssc_identification_number = models.CharField(max_length=255, null=True, blank=False, verbose_name='证件号码')
    characterfield_name = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人性别')
    datetimefield_date_of_birth = models.DateField(null=True, blank=False, verbose_name='出生日期')
    boolfield_bao_xian_you_xiao_qi = models.DateField(null=True, blank=False, verbose_name='保险有效期')
    boolfield_zheng_jian_lei_xing = models.ForeignKey(Zheng_jian_lei_xing, related_name='zheng_jian_lei_xing_for_boolfield_zheng_jian_lei_xing_yu_yue_an_pai', on_delete=models.CASCADE, null=True, blank=False, verbose_name='证件类型')
    boolfield_xu_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='序号')
    boolfield_bao_dan_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='保单号')
    boolfield_bao_xian_ze_ren = models.CharField(max_length=255, null=True, blank=False, verbose_name='保险责任')
    boolfield_chang_zhu_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='常住地址')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=False, verbose_name='联系电话')

    class Meta:
        verbose_name = '预约安排'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Zhi_yuan_ji_ben_xin_xi_biao(HsscBaseFormModel):
    characterhssc_identification_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='证件号码')
    characterfield_practice_qualification = models.CharField(max_length=255, null=True, blank=True, verbose_name='执业资质')
    characterfield_expertise = models.CharField(max_length=255, null=True, blank=True, verbose_name='专长')
    characterfield_practice_time = models.CharField(max_length=255, null=True, blank=True, verbose_name='执业时间')
    boolfield_zhi_yuan_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='职员编码')
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构联系电话')
    characterfield_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='被保人姓名')
    relatedfield_affiliation = models.ForeignKey(Ji_gou_ji_ben_xin_xi_biao, related_name='ji_gou_ji_ben_xin_xi_biao_for_relatedfield_affiliation_zhi_yuan_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='所属机构')
    relatedfield_service_role = models.ManyToManyField(Fu_wu_jue_se, related_name='fu_wu_jue_se_for_relatedfield_service_role_zhi_yuan_ji_ben_xin_xi_biao', blank=True, verbose_name='服务角色')

    class Meta:
        verbose_name = '职员基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_cha(HsscBaseFormModel):

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
    characterfield_contact_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构联系电话')
    boolfield_she_bei_shi_yong_fu_wu_gong_neng = models.ForeignKey(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_she_bei_shi_yong_fu_wu_gong_neng_she_bei_ji_ben_xin_xi_ji_lu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='设备适用服务功能')

    class Meta:
        verbose_name = '设备基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Gong_ying_shang_ji_ben_xin_xi_diao_cha(HsscBaseFormModel):

    class Meta:
        verbose_name = '物料供应商基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Yao_pin_ji_ben_xin_xi_biao(HsscBaseFormModel):

    class Meta:
        verbose_name = '药品基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Ju_min_ji_ben_xin_xi_diao_cha(HsscBaseFormModel):
    characterhssc_identification_number = models.CharField(max_length=255, null=True, blank=False, verbose_name='证件号码')
    characterfield_name = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人性别')
    datetimefield_date_of_birth = models.DateField(null=True, blank=False, verbose_name='出生日期')
    boolfield_bao_xian_you_xiao_qi = models.DateField(null=True, blank=False, verbose_name='保险有效期')
    boolfield_zheng_jian_lei_xing = models.ForeignKey(Zheng_jian_lei_xing, related_name='zheng_jian_lei_xing_for_boolfield_zheng_jian_lei_xing_ju_min_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=False, verbose_name='证件类型')
    boolfield_xu_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='序号')
    boolfield_bao_dan_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='保单号')
    boolfield_bao_xian_ze_ren = models.CharField(max_length=255, null=True, blank=False, verbose_name='保险责任')
    boolfield_chang_zhu_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='常住地址')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=False, verbose_name='联系电话')

    class Meta:
        verbose_name = '被保人基本信息调查'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class A6401(HsscFormModel):
    characterfield_name = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人姓名')
    characterfield_gender = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人性别')
    datetimefield_date_of_birth = models.DateField(null=True, blank=False, verbose_name='出生日期')
    boolfield_chang_zhu_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='常住地址')
    datetimefield_ri_qi_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='预约时间')
    boolfield_ze_ren_ren = models.ForeignKey(Ji_gou_ji_ben_xin_xi_biao, related_name='ji_gou_ji_ben_xin_xi_biao_for_boolfield_ze_ren_ren_A6401', on_delete=models.CASCADE, null=True, blank=True, verbose_name='就诊机构')
    boolfield_jiu_zhen_wen_ti = models.CharField(max_length=255, null=True, blank=False, verbose_name='就诊问题')
    boolfield_shi_yong_bao_xian_chan_pin = models.ManyToManyField(Bao_xian_chan_pin, related_name='bao_xian_chan_pin_for_boolfield_shi_yong_bao_xian_chan_pin_A6401', blank=True, verbose_name='使用服务产品')
    boolfield_fu_jia_fu_wu_yao_qiu = models.CharField(max_length=255, null=True, blank=True, verbose_name='附加服务要求')

    class Meta:
        verbose_name = '预约申请'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
