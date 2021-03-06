from django.db import models

from icpc.models import *
from dictionaries.models import *
from core.models import HsscFormModel, HsscBaseFormModel, Staff, Institution, Service, ServicePackage, Customer
from core.hsscbase_class import HsscBase

class CustomerSchedulePackage(HsscFormModel):
    servicepackage = models.ForeignKey(ServicePackage, on_delete=models.CASCADE, verbose_name='服务包')
    
    class Meta:
        verbose_name = '安排服务包'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.servicepackage.label

class CustomerScheduleDraft(HsscBase):
    schedule_package = models.ForeignKey(CustomerSchedulePackage, null=True, on_delete=models.CASCADE, verbose_name='服务包')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    Cycle_unit = [('TOTAL', '总共'), ('DAY', '每天'), ('WEEK', '每周'), ('MONTH', '每月'), ('QUARTER', '每季'), ('YEAR', '每年')]
    cycle_unit = models.CharField(max_length=10, choices=Cycle_unit, default='TOTAL', blank=True, null=True, verbose_name='周期单位')
    cycle_frequency = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="每周期频次")
    cycle_times = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="周期数/天数")
    Default_beginning_time = [(1, '当前系统时间'), (2, '首个服务开始时间'), (3, '上个服务结束时间'), (4, '客户出生日期')]
    default_beginning_time = models.PositiveSmallIntegerField(choices=Default_beginning_time, default=1, verbose_name='执行时间基准')
    base_interval = models.DurationField(blank=True, null=True, verbose_name='基准间隔', help_text='例如：3 days, 22:00:00')
    scheduled_operator = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True, verbose_name='服务人员')
    
    class Meta:
        verbose_name = '服务项目安排'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.service.label

class CustomerSchedule(HsscBase):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE, verbose_name='客户')
    schedule_package = models.ForeignKey(CustomerSchedulePackage, null=True, on_delete=models.CASCADE, verbose_name='服务包')
    scheduled_draft = models.ForeignKey(CustomerScheduleDraft, on_delete=models.CASCADE, verbose_name='日程草案')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    scheduled_time = models.DateTimeField(blank=True, null=True, verbose_name='计划执行时间')
    scheduled_operator = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True, verbose_name='服务人员')

    class Meta:
        verbose_name = '客户服务日程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.service.label


# **********************************************************************************************************************
# Service基本信息表单Model
# **********************************************************************************************************************
class Men_zhen_ji_lu_hui_zong(HsscFormModel):
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_men_zhen_ji_lu_hui_zong', blank=True, verbose_name='症状')
    boolfield_jian_cha_xiang_mu = models.ManyToManyField(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_jian_cha_xiang_mu_men_zhen_ji_lu_hui_zong', blank=True, verbose_name='检查项目')
    boolfield_zhen_duan = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_zhen_duan_men_zhen_ji_lu_hui_zong', on_delete=models.CASCADE, null=True, blank=False, verbose_name='诊断')
    boolfield_zhi_liao_xiang_mu = models.ManyToManyField(Icpc7_treatments, related_name='icpc7_treatments_for_boolfield_zhi_liao_xiang_mu_men_zhen_ji_lu_hui_zong', blank=False, verbose_name='治疗项目')
    boolfield_qi_ta_jian_kang_gan_yu_fu_wu = models.ManyToManyField(Icpc8_other_health_interventions, related_name='icpc8_other_health_interventions_for_boolfield_qi_ta_jian_kang_gan_yu_fu_wu_men_zhen_ji_lu_hui_zong', blank=True, verbose_name='其他健康干预服务')
    boolfield_fei_yong_he_ji = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='费用合计')
    boolfield_men_zhen_bing_li_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='门诊病历附件')

    class Meta:
        verbose_name = '门诊记录汇总'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Chong_xin_yu_yue_an_pai(HsscFormModel):
    boolfield_yu_yue_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='预约时间')
    boolfield_jiu_zhen_wen_ti = models.CharField(max_length=255, null=True, blank=False, verbose_name='就诊问题')
    boolfield_jiu_zhen_ji_gou_ze_ren_ren = models.ForeignKey(Staff, related_name='staff_for_boolfield_jiu_zhen_ji_gou_ze_ren_ren_chong_xin_yu_yue_an_pai', on_delete=models.CASCADE, null=True, blank=True, verbose_name='就诊机构责任人')
    boolfield_shi_yong_fu_wu_chan_pin = models.ManyToManyField(Bao_xian_chan_pin, related_name='bao_xian_chan_pin_for_boolfield_shi_yong_fu_wu_chan_pin_chong_xin_yu_yue_an_pai', blank=True, verbose_name='使用服务产品')
    boolfield_fu_jia_fu_wu_yao_qiu = models.CharField(max_length=255, null=True, blank=True, verbose_name='附加服务要求')
    boolfield_jie_dan_que_ren = models.ForeignKey(Jie_dan_que_ren, related_name='jie_dan_que_ren_for_boolfield_jie_dan_que_ren_chong_xin_yu_yue_an_pai', on_delete=models.CASCADE, null=True, blank=False, verbose_name='接单确认')
    boolfield_ju_jue_jie_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='拒绝接单原因')

    class Meta:
        verbose_name = '重新预约安排'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Zhen_suo_yu_yue(HsscFormModel):
    boolfield_yu_yue_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='预约时间')
    boolfield_jiu_zhen_wen_ti = models.CharField(max_length=255, null=True, blank=False, verbose_name='就诊问题')
    boolfield_jiu_zhen_ji_gou_ze_ren_ren = models.ForeignKey(Staff, related_name='staff_for_boolfield_jiu_zhen_ji_gou_ze_ren_ren_zhen_suo_yu_yue', on_delete=models.CASCADE, null=True, blank=True, verbose_name='就诊机构责任人')
    boolfield_shi_yong_fu_wu_chan_pin = models.ManyToManyField(Bao_xian_chan_pin, related_name='bao_xian_chan_pin_for_boolfield_shi_yong_fu_wu_chan_pin_zhen_suo_yu_yue', blank=True, verbose_name='使用服务产品')
    boolfield_fu_jia_fu_wu_yao_qiu = models.CharField(max_length=255, null=True, blank=True, verbose_name='附加服务要求')

    class Meta:
        verbose_name = '诊所安排'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Li_pei_shen_qing_chong_shen(HsscFormModel):
    boolfield_shen_qing_ren_xing_ming = models.CharField(max_length=255, null=True, blank=False, verbose_name='申请人姓名')
    boolfield_xing_bie = models.ForeignKey(Gender, related_name='gender_for_boolfield_xing_bie_li_pei_shen_qing_chong_shen', on_delete=models.CASCADE, null=True, blank=False, verbose_name='性别')
    boolfield_yu_chu_xian_ren_guan_xi = models.ForeignKey(Yu_chu_xian_ren_guan_xi, related_name='yu_chu_xian_ren_guan_xi_for_boolfield_yu_chu_xian_ren_guan_xi_li_pei_shen_qing_chong_shen', on_delete=models.CASCADE, null=True, blank=False, verbose_name='与出险人关系')
    boolfield_zheng_jian_lei_xing = models.ForeignKey(Zheng_jian_lei_xing, related_name='zheng_jian_lei_xing_for_boolfield_zheng_jian_lei_xing_li_pei_shen_qing_chong_shen', on_delete=models.CASCADE, null=True, blank=False, verbose_name='证件类型')
    boolfield_zheng_jian_hao_ma = models.CharField(max_length=255, null=True, blank=False, verbose_name='证件号码')
    boolfield_zheng_jian_you_xiao_qi = models.CharField(max_length=255, null=True, blank=False, verbose_name='证件有效期')
    boolfield_guo_ji_di_qu = models.CharField(max_length=255, null=True, blank=False, verbose_name='国籍地区')
    boolfield_hang_ye = models.CharField(max_length=255, null=True, blank=False, verbose_name='行业')
    boolfield_zhi_ye = models.CharField(max_length=255, null=True, blank=False, verbose_name='职业')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=False, verbose_name='联系电话')
    boolfield_chang_zhu_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='常住地址')
    boolfield_shen_qing_ren_zheng_jian_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='申请人证件附件')
    boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu = models.ForeignKey(Qian_shu_que_ren, related_name='qian_shu_que_ren_for_boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu_li_pei_shen_qing_chong_shen', on_delete=models.CASCADE, null=True, blank=False, verbose_name='人身险理赔申请书签署')
    boolfield_ren_shen_xian_li_pei_shen_qing_shu_tui_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='人身险理赔申请书退单原因')
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_li_pei_shen_qing_chong_shen', blank=True, verbose_name='症状')
    boolfield_jian_cha_xiang_mu = models.ManyToManyField(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_jian_cha_xiang_mu_li_pei_shen_qing_chong_shen', blank=True, verbose_name='检查项目')
    boolfield_zhen_duan = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_zhen_duan_li_pei_shen_qing_chong_shen', on_delete=models.CASCADE, null=True, blank=False, verbose_name='诊断')
    boolfield_zhi_liao_xiang_mu = models.ManyToManyField(Icpc7_treatments, related_name='icpc7_treatments_for_boolfield_zhi_liao_xiang_mu_li_pei_shen_qing_chong_shen', blank=False, verbose_name='治疗项目')
    boolfield_qi_ta_jian_kang_gan_yu_fu_wu = models.ManyToManyField(Icpc8_other_health_interventions, related_name='icpc8_other_health_interventions_for_boolfield_qi_ta_jian_kang_gan_yu_fu_wu_li_pei_shen_qing_chong_shen', blank=True, verbose_name='其他健康干预服务')
    boolfield_fei_yong_he_ji = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='费用合计')
    boolfield_men_zhen_bing_li_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='门诊病历附件')
    boolfield_men_zhen_ji_lu_dan_tui_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='门诊记录单退单原因')
    boolfield_li_pei_men_zhen_ji_lu_qian_shu = models.ForeignKey(Qian_shu_que_ren, related_name='qian_shu_que_ren_for_boolfield_li_pei_men_zhen_ji_lu_qian_shu_li_pei_shen_qing_chong_shen', on_delete=models.CASCADE, null=True, blank=False, verbose_name='理赔门诊记录签署')
    boolfield_xu_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='序号')
    boolfield_bao_dan_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='保单号')
    boolfield_bao_an_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='报案时间')
    boolfield_bao_an_ren = models.CharField(max_length=255, null=True, blank=False, verbose_name='报案人')
    boolfield_bao_an_ren_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=False, verbose_name='报案人联系电话')
    boolfield_chu_xian_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='出险时间')
    boolfield_chu_xian_ren_xing_ming = models.CharField(max_length=255, null=True, blank=False, verbose_name='出险人姓名')
    boolfield_chu_xian_di_dian = models.CharField(max_length=255, null=True, blank=False, verbose_name='出险地点')
    boolfield_chu_xian_di_dian_sheng_ji_bie = models.CharField(max_length=255, null=True, blank=False, verbose_name='出险地点省级别')
    boolfield_chu_xian_di_dian_shi_ji_bie = models.CharField(max_length=255, null=True, blank=False, verbose_name='出险地点市级别')
    boolfield_shi_gu_gai_kuo = models.CharField(max_length=255, null=True, blank=False, verbose_name='事故概括')
    boolfield_zheng_jian_lei_xing = models.ForeignKey(Zheng_jian_lei_xing, related_name='zheng_jian_lei_xing_for_boolfield_zheng_jian_lei_xing_li_pei_shen_qing_chong_shen', on_delete=models.CASCADE, null=True, blank=False, verbose_name='证件类型')
    boolfield_bei_bao_xian_ren_zheng_jian_hao_ma = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保险人证件号码')
    boolfield_xing_bie = models.ForeignKey(Gender, related_name='gender_for_boolfield_xing_bie_li_pei_shen_qing_chong_shen', on_delete=models.CASCADE, null=True, blank=False, verbose_name='性别')
    boolfield_nian_ling = models.CharField(max_length=255, null=True, blank=False, verbose_name='年龄')
    boolfield_chu_sheng_ri_qi = models.DateField(null=True, blank=False, verbose_name='出生日期')
    boolfield_gui_shu_cheng_shi = models.CharField(max_length=255, null=True, blank=False, verbose_name='归属城市')
    boolfield_yi_yuan_xin_xi = models.CharField(max_length=255, null=True, blank=False, verbose_name='医院信息')
    boolfield_ji_bing_xin_xi = models.CharField(max_length=255, null=True, blank=False, verbose_name='疾病信息')
    boolfield_li_pei_jin_e = models.CharField(max_length=255, null=True, blank=False, verbose_name='理赔金额')
    boolfield_li_pei_fang_shi = models.CharField(max_length=255, null=True, blank=False, verbose_name='理赔方式')
    boolfield_bei_zhu = models.CharField(max_length=255, null=True, blank=False, verbose_name='备注')
    boolfield_bei_bao_ren_zheng_jian_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='被保人证件附件')
    boolfield_li_pei_dui_zhang_dan_qian_shu = models.ForeignKey(Qian_shu_que_ren, related_name='qian_shu_que_ren_for_boolfield_li_pei_dui_zhang_dan_qian_shu_li_pei_shen_qing_chong_shen', on_delete=models.CASCADE, null=True, blank=False, verbose_name='理赔对账单签署')
    boolfield_li_pei_dui_zhang_dan_tui_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='理赔对账单退单原因')
    boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu = models.ManyToManyField(Fu_wu_xiang_mu, related_name='fu_wu_xiang_mu_for_boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu_li_pei_shen_qing_chong_shen', blank=False, verbose_name='保单内服务收费项目')
    boolfield_bao_dan_nei_fu_wu_fei_yong = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='保单内服务费用')
    boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu = models.ManyToManyField(Fu_wu_xiang_mu, related_name='fu_wu_xiang_mu_for_boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu_li_pei_shen_qing_chong_shen', blank=False, verbose_name='保单外服务收费项目')
    boolfield_bao_dan_wai_fu_wu_fei_yong = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='保单外服务费用')
    boolfield_fei_yong_he_ji = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='费用合计')
    boolfield_hui_zong_fei_yong_qing_dan_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='汇总费用清单附件')
    boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu = models.ForeignKey(Qian_shu_que_ren, related_name='qian_shu_que_ren_for_boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu_li_pei_shen_qing_chong_shen', on_delete=models.CASCADE, null=True, blank=False, verbose_name='理赔费用汇总单签署')
    boolfield_li_pei_fei_yong_hui_zong_dan_tui_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='理赔费用汇总单退单原因')

    class Meta:
        verbose_name = '重新申请理赔'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Yu_yue_zi_xun(HsscFormModel):
    boolfield_yu_yue_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='预约时间')
    boolfield_jiu_zhen_wen_ti = models.CharField(max_length=255, null=True, blank=False, verbose_name='就诊问题')
    boolfield_jiu_zhen_ji_gou_ze_ren_ren = models.ForeignKey(Staff, related_name='staff_for_boolfield_jiu_zhen_ji_gou_ze_ren_ren_yu_yue_zi_xun', on_delete=models.CASCADE, null=True, blank=True, verbose_name='就诊机构责任人')
    boolfield_shi_yong_fu_wu_chan_pin = models.ManyToManyField(Bao_xian_chan_pin, related_name='bao_xian_chan_pin_for_boolfield_shi_yong_fu_wu_chan_pin_yu_yue_zi_xun', blank=True, verbose_name='使用服务产品')
    boolfield_fu_jia_fu_wu_yao_qiu = models.CharField(max_length=255, null=True, blank=True, verbose_name='附加服务要求')

    class Meta:
        verbose_name = '咨询预约'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Ti_jiao_he_bao_zi_liao(HsscFormModel):
    boolfield_shen_qing_ren_xing_ming = models.CharField(max_length=255, null=True, blank=False, verbose_name='申请人姓名')
    boolfield_xing_bie = models.ForeignKey(Gender, related_name='gender_for_boolfield_xing_bie_ti_jiao_he_bao_zi_liao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='性别')
    boolfield_yu_chu_xian_ren_guan_xi = models.ForeignKey(Yu_chu_xian_ren_guan_xi, related_name='yu_chu_xian_ren_guan_xi_for_boolfield_yu_chu_xian_ren_guan_xi_ti_jiao_he_bao_zi_liao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='与出险人关系')
    boolfield_zheng_jian_lei_xing = models.ForeignKey(Zheng_jian_lei_xing, related_name='zheng_jian_lei_xing_for_boolfield_zheng_jian_lei_xing_ti_jiao_he_bao_zi_liao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='证件类型')
    boolfield_zheng_jian_hao_ma = models.CharField(max_length=255, null=True, blank=False, verbose_name='证件号码')
    boolfield_zheng_jian_you_xiao_qi = models.CharField(max_length=255, null=True, blank=False, verbose_name='证件有效期')
    boolfield_guo_ji_di_qu = models.CharField(max_length=255, null=True, blank=False, verbose_name='国籍地区')
    boolfield_hang_ye = models.CharField(max_length=255, null=True, blank=False, verbose_name='行业')
    boolfield_zhi_ye = models.CharField(max_length=255, null=True, blank=False, verbose_name='职业')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=False, verbose_name='联系电话')
    boolfield_chang_zhu_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='常住地址')
    boolfield_shen_qing_ren_zheng_jian_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='申请人证件附件')
    boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu = models.ForeignKey(Qian_shu_que_ren, related_name='qian_shu_que_ren_for_boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu_ti_jiao_he_bao_zi_liao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='人身险理赔申请书签署')
    boolfield_ren_shen_xian_li_pei_shen_qing_shu_tui_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='人身险理赔申请书退单原因')
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_ti_jiao_he_bao_zi_liao', blank=True, verbose_name='症状')
    boolfield_jian_cha_xiang_mu = models.ManyToManyField(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_jian_cha_xiang_mu_ti_jiao_he_bao_zi_liao', blank=True, verbose_name='检查项目')
    boolfield_zhen_duan = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_zhen_duan_ti_jiao_he_bao_zi_liao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='诊断')
    boolfield_zhi_liao_xiang_mu = models.ManyToManyField(Icpc7_treatments, related_name='icpc7_treatments_for_boolfield_zhi_liao_xiang_mu_ti_jiao_he_bao_zi_liao', blank=False, verbose_name='治疗项目')
    boolfield_qi_ta_jian_kang_gan_yu_fu_wu = models.ManyToManyField(Icpc8_other_health_interventions, related_name='icpc8_other_health_interventions_for_boolfield_qi_ta_jian_kang_gan_yu_fu_wu_ti_jiao_he_bao_zi_liao', blank=True, verbose_name='其他健康干预服务')
    boolfield_fei_yong_he_ji = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='费用合计')
    boolfield_men_zhen_bing_li_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='门诊病历附件')
    boolfield_men_zhen_ji_lu_dan_tui_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='门诊记录单退单原因')
    boolfield_li_pei_men_zhen_ji_lu_qian_shu = models.ForeignKey(Qian_shu_que_ren, related_name='qian_shu_que_ren_for_boolfield_li_pei_men_zhen_ji_lu_qian_shu_ti_jiao_he_bao_zi_liao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='理赔门诊记录签署')
    boolfield_xu_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='序号')
    boolfield_bao_dan_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='保单号')
    boolfield_bao_an_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='报案时间')
    boolfield_bao_an_ren = models.CharField(max_length=255, null=True, blank=False, verbose_name='报案人')
    boolfield_bao_an_ren_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=False, verbose_name='报案人联系电话')
    boolfield_chu_xian_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='出险时间')
    boolfield_chu_xian_ren_xing_ming = models.CharField(max_length=255, null=True, blank=False, verbose_name='出险人姓名')
    boolfield_chu_xian_di_dian = models.CharField(max_length=255, null=True, blank=False, verbose_name='出险地点')
    boolfield_chu_xian_di_dian_sheng_ji_bie = models.CharField(max_length=255, null=True, blank=False, verbose_name='出险地点省级别')
    boolfield_chu_xian_di_dian_shi_ji_bie = models.CharField(max_length=255, null=True, blank=False, verbose_name='出险地点市级别')
    boolfield_shi_gu_gai_kuo = models.CharField(max_length=255, null=True, blank=False, verbose_name='事故概括')
    boolfield_zheng_jian_lei_xing = models.ForeignKey(Zheng_jian_lei_xing, related_name='zheng_jian_lei_xing_for_boolfield_zheng_jian_lei_xing_ti_jiao_he_bao_zi_liao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='证件类型')
    boolfield_bei_bao_xian_ren_zheng_jian_hao_ma = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保险人证件号码')
    boolfield_xing_bie = models.ForeignKey(Gender, related_name='gender_for_boolfield_xing_bie_ti_jiao_he_bao_zi_liao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='性别')
    boolfield_nian_ling = models.CharField(max_length=255, null=True, blank=False, verbose_name='年龄')
    boolfield_chu_sheng_ri_qi = models.DateField(null=True, blank=False, verbose_name='出生日期')
    boolfield_gui_shu_cheng_shi = models.CharField(max_length=255, null=True, blank=False, verbose_name='归属城市')
    boolfield_yi_yuan_xin_xi = models.CharField(max_length=255, null=True, blank=False, verbose_name='医院信息')
    boolfield_ji_bing_xin_xi = models.CharField(max_length=255, null=True, blank=False, verbose_name='疾病信息')
    boolfield_li_pei_jin_e = models.CharField(max_length=255, null=True, blank=False, verbose_name='理赔金额')
    boolfield_li_pei_fang_shi = models.CharField(max_length=255, null=True, blank=False, verbose_name='理赔方式')
    boolfield_bei_zhu = models.CharField(max_length=255, null=True, blank=False, verbose_name='备注')
    boolfield_bei_bao_ren_zheng_jian_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='被保人证件附件')
    boolfield_li_pei_dui_zhang_dan_qian_shu = models.ForeignKey(Qian_shu_que_ren, related_name='qian_shu_que_ren_for_boolfield_li_pei_dui_zhang_dan_qian_shu_ti_jiao_he_bao_zi_liao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='理赔对账单签署')
    boolfield_li_pei_dui_zhang_dan_tui_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='理赔对账单退单原因')
    boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu = models.ManyToManyField(Fu_wu_xiang_mu, related_name='fu_wu_xiang_mu_for_boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu_ti_jiao_he_bao_zi_liao', blank=False, verbose_name='保单内服务收费项目')
    boolfield_bao_dan_nei_fu_wu_fei_yong = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='保单内服务费用')
    boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu = models.ManyToManyField(Fu_wu_xiang_mu, related_name='fu_wu_xiang_mu_for_boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu_ti_jiao_he_bao_zi_liao', blank=False, verbose_name='保单外服务收费项目')
    boolfield_bao_dan_wai_fu_wu_fei_yong = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='保单外服务费用')
    boolfield_fei_yong_he_ji = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='费用合计')
    boolfield_hui_zong_fei_yong_qing_dan_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='汇总费用清单附件')
    boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu = models.ForeignKey(Qian_shu_que_ren, related_name='qian_shu_que_ren_for_boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu_ti_jiao_he_bao_zi_liao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='理赔费用汇总单签署')
    boolfield_li_pei_fei_yong_hui_zong_dan_tui_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='理赔费用汇总单退单原因')
    boolfield_shi_fou_shen_he_tong_guo = models.ForeignKey(Shi_fou_shen_he_tong_guo, related_name='shi_fou_shen_he_tong_guo_for_boolfield_shi_fou_shen_he_tong_guo_ti_jiao_he_bao_zi_liao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='是否审核通过')
    boolfield_li_pei_shen_qing_tui_hui_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='理赔申请退回原因')

    class Meta:
        verbose_name = '保险理赔审核服务'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Li_pei_shen_qing_fu_wu(HsscFormModel):
    boolfield_xu_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='序号')
    boolfield_bao_dan_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='保单号')
    boolfield_bao_an_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='报案时间')
    boolfield_bao_an_ren = models.CharField(max_length=255, null=True, blank=False, verbose_name='报案人')
    boolfield_bao_an_ren_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=False, verbose_name='报案人联系电话')
    boolfield_chu_xian_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='出险时间')
    boolfield_chu_xian_ren_xing_ming = models.CharField(max_length=255, null=True, blank=False, verbose_name='出险人姓名')
    boolfield_chu_xian_di_dian = models.CharField(max_length=255, null=True, blank=False, verbose_name='出险地点')
    boolfield_chu_xian_di_dian_sheng_ji_bie = models.CharField(max_length=255, null=True, blank=False, verbose_name='出险地点省级别')
    boolfield_chu_xian_di_dian_shi_ji_bie = models.CharField(max_length=255, null=True, blank=False, verbose_name='出险地点市级别')
    boolfield_shi_gu_gai_kuo = models.CharField(max_length=255, null=True, blank=False, verbose_name='事故概括')
    boolfield_zheng_jian_lei_xing = models.ForeignKey(Zheng_jian_lei_xing, related_name='zheng_jian_lei_xing_for_boolfield_zheng_jian_lei_xing_li_pei_shen_qing_fu_wu', on_delete=models.CASCADE, null=True, blank=False, verbose_name='证件类型')
    boolfield_bei_bao_xian_ren_zheng_jian_hao_ma = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保险人证件号码')
    boolfield_xing_bie = models.ForeignKey(Gender, related_name='gender_for_boolfield_xing_bie_li_pei_shen_qing_fu_wu', on_delete=models.CASCADE, null=True, blank=False, verbose_name='性别')
    boolfield_nian_ling = models.CharField(max_length=255, null=True, blank=False, verbose_name='年龄')
    boolfield_chu_sheng_ri_qi = models.DateField(null=True, blank=False, verbose_name='出生日期')
    boolfield_gui_shu_cheng_shi = models.CharField(max_length=255, null=True, blank=False, verbose_name='归属城市')
    boolfield_yi_yuan_xin_xi = models.CharField(max_length=255, null=True, blank=False, verbose_name='医院信息')
    boolfield_ji_bing_xin_xi = models.CharField(max_length=255, null=True, blank=False, verbose_name='疾病信息')
    boolfield_li_pei_jin_e = models.CharField(max_length=255, null=True, blank=False, verbose_name='理赔金额')
    boolfield_li_pei_fang_shi = models.CharField(max_length=255, null=True, blank=False, verbose_name='理赔方式')
    boolfield_bei_zhu = models.CharField(max_length=255, null=True, blank=False, verbose_name='备注')
    boolfield_bei_bao_ren_zheng_jian_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='被保人证件附件')
    boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu = models.ManyToManyField(Fu_wu_xiang_mu, related_name='fu_wu_xiang_mu_for_boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu_li_pei_shen_qing_fu_wu', blank=False, verbose_name='保单内服务收费项目')
    boolfield_bao_dan_nei_fu_wu_fei_yong = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='保单内服务费用')
    boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu = models.ManyToManyField(Fu_wu_xiang_mu, related_name='fu_wu_xiang_mu_for_boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu_li_pei_shen_qing_fu_wu', blank=False, verbose_name='保单外服务收费项目')
    boolfield_bao_dan_wai_fu_wu_fei_yong = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='保单外服务费用')
    boolfield_fei_yong_he_ji = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='费用合计')
    boolfield_hui_zong_fei_yong_qing_dan_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='汇总费用清单附件')
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_li_pei_shen_qing_fu_wu', blank=True, verbose_name='症状')
    boolfield_jian_cha_xiang_mu = models.ManyToManyField(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_jian_cha_xiang_mu_li_pei_shen_qing_fu_wu', blank=True, verbose_name='检查项目')
    boolfield_zhen_duan = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_zhen_duan_li_pei_shen_qing_fu_wu', on_delete=models.CASCADE, null=True, blank=False, verbose_name='诊断')
    boolfield_zhi_liao_xiang_mu = models.ManyToManyField(Icpc7_treatments, related_name='icpc7_treatments_for_boolfield_zhi_liao_xiang_mu_li_pei_shen_qing_fu_wu', blank=False, verbose_name='治疗项目')
    boolfield_qi_ta_jian_kang_gan_yu_fu_wu = models.ManyToManyField(Icpc8_other_health_interventions, related_name='icpc8_other_health_interventions_for_boolfield_qi_ta_jian_kang_gan_yu_fu_wu_li_pei_shen_qing_fu_wu', blank=True, verbose_name='其他健康干预服务')
    boolfield_fei_yong_he_ji = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='费用合计')
    boolfield_men_zhen_bing_li_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='门诊病历附件')
    boolfield_shen_qing_ren_xing_ming = models.CharField(max_length=255, null=True, blank=False, verbose_name='申请人姓名')
    boolfield_xing_bie = models.ForeignKey(Gender, related_name='gender_for_boolfield_xing_bie_li_pei_shen_qing_fu_wu', on_delete=models.CASCADE, null=True, blank=False, verbose_name='性别')
    boolfield_yu_chu_xian_ren_guan_xi = models.ForeignKey(Yu_chu_xian_ren_guan_xi, related_name='yu_chu_xian_ren_guan_xi_for_boolfield_yu_chu_xian_ren_guan_xi_li_pei_shen_qing_fu_wu', on_delete=models.CASCADE, null=True, blank=False, verbose_name='与出险人关系')
    boolfield_zheng_jian_lei_xing = models.ForeignKey(Zheng_jian_lei_xing, related_name='zheng_jian_lei_xing_for_boolfield_zheng_jian_lei_xing_li_pei_shen_qing_fu_wu', on_delete=models.CASCADE, null=True, blank=False, verbose_name='证件类型')
    boolfield_zheng_jian_hao_ma = models.CharField(max_length=255, null=True, blank=False, verbose_name='证件号码')
    boolfield_zheng_jian_you_xiao_qi = models.CharField(max_length=255, null=True, blank=False, verbose_name='证件有效期')
    boolfield_guo_ji_di_qu = models.CharField(max_length=255, null=True, blank=False, verbose_name='国籍地区')
    boolfield_hang_ye = models.CharField(max_length=255, null=True, blank=False, verbose_name='行业')
    boolfield_zhi_ye = models.CharField(max_length=255, null=True, blank=False, verbose_name='职业')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=False, verbose_name='联系电话')
    boolfield_chang_zhu_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='常住地址')
    boolfield_shen_qing_ren_zheng_jian_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='申请人证件附件')

    class Meta:
        verbose_name = '发起理赔申请'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Li_pei_shen_qing_shu_shen_he(HsscFormModel):
    boolfield_shen_qing_ren_xing_ming = models.CharField(max_length=255, null=True, blank=False, verbose_name='申请人姓名')
    boolfield_xing_bie = models.ForeignKey(Gender, related_name='gender_for_boolfield_xing_bie_li_pei_shen_qing_shu_shen_he', on_delete=models.CASCADE, null=True, blank=False, verbose_name='性别')
    boolfield_yu_chu_xian_ren_guan_xi = models.ForeignKey(Yu_chu_xian_ren_guan_xi, related_name='yu_chu_xian_ren_guan_xi_for_boolfield_yu_chu_xian_ren_guan_xi_li_pei_shen_qing_shu_shen_he', on_delete=models.CASCADE, null=True, blank=False, verbose_name='与出险人关系')
    boolfield_zheng_jian_lei_xing = models.ForeignKey(Zheng_jian_lei_xing, related_name='zheng_jian_lei_xing_for_boolfield_zheng_jian_lei_xing_li_pei_shen_qing_shu_shen_he', on_delete=models.CASCADE, null=True, blank=False, verbose_name='证件类型')
    boolfield_zheng_jian_hao_ma = models.CharField(max_length=255, null=True, blank=False, verbose_name='证件号码')
    boolfield_zheng_jian_you_xiao_qi = models.CharField(max_length=255, null=True, blank=False, verbose_name='证件有效期')
    boolfield_guo_ji_di_qu = models.CharField(max_length=255, null=True, blank=False, verbose_name='国籍地区')
    boolfield_hang_ye = models.CharField(max_length=255, null=True, blank=False, verbose_name='行业')
    boolfield_zhi_ye = models.CharField(max_length=255, null=True, blank=False, verbose_name='职业')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=False, verbose_name='联系电话')
    boolfield_chang_zhu_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='常住地址')
    boolfield_shen_qing_ren_zheng_jian_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='申请人证件附件')
    boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu = models.ForeignKey(Qian_shu_que_ren, related_name='qian_shu_que_ren_for_boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu_li_pei_shen_qing_shu_shen_he', on_delete=models.CASCADE, null=True, blank=False, verbose_name='人身险理赔申请书签署')
    boolfield_ren_shen_xian_li_pei_shen_qing_shu_tui_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='人身险理赔申请书退单原因')
    boolfield_xu_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='序号')
    boolfield_bao_dan_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='保单号')
    boolfield_bao_an_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='报案时间')
    boolfield_bao_an_ren = models.CharField(max_length=255, null=True, blank=False, verbose_name='报案人')
    boolfield_bao_an_ren_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=False, verbose_name='报案人联系电话')
    boolfield_chu_xian_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='出险时间')
    boolfield_chu_xian_ren_xing_ming = models.CharField(max_length=255, null=True, blank=False, verbose_name='出险人姓名')
    boolfield_chu_xian_di_dian = models.CharField(max_length=255, null=True, blank=False, verbose_name='出险地点')
    boolfield_chu_xian_di_dian_sheng_ji_bie = models.CharField(max_length=255, null=True, blank=False, verbose_name='出险地点省级别')
    boolfield_chu_xian_di_dian_shi_ji_bie = models.CharField(max_length=255, null=True, blank=False, verbose_name='出险地点市级别')
    boolfield_shi_gu_gai_kuo = models.CharField(max_length=255, null=True, blank=False, verbose_name='事故概括')
    boolfield_zheng_jian_lei_xing = models.ForeignKey(Zheng_jian_lei_xing, related_name='zheng_jian_lei_xing_for_boolfield_zheng_jian_lei_xing_li_pei_shen_qing_shu_shen_he', on_delete=models.CASCADE, null=True, blank=False, verbose_name='证件类型')
    boolfield_bei_bao_xian_ren_zheng_jian_hao_ma = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保险人证件号码')
    boolfield_xing_bie = models.ForeignKey(Gender, related_name='gender_for_boolfield_xing_bie_li_pei_shen_qing_shu_shen_he', on_delete=models.CASCADE, null=True, blank=False, verbose_name='性别')
    boolfield_nian_ling = models.CharField(max_length=255, null=True, blank=False, verbose_name='年龄')
    boolfield_chu_sheng_ri_qi = models.DateField(null=True, blank=False, verbose_name='出生日期')
    boolfield_gui_shu_cheng_shi = models.CharField(max_length=255, null=True, blank=False, verbose_name='归属城市')
    boolfield_yi_yuan_xin_xi = models.CharField(max_length=255, null=True, blank=False, verbose_name='医院信息')
    boolfield_ji_bing_xin_xi = models.CharField(max_length=255, null=True, blank=False, verbose_name='疾病信息')
    boolfield_li_pei_jin_e = models.CharField(max_length=255, null=True, blank=False, verbose_name='理赔金额')
    boolfield_li_pei_fang_shi = models.CharField(max_length=255, null=True, blank=False, verbose_name='理赔方式')
    boolfield_bei_zhu = models.CharField(max_length=255, null=True, blank=False, verbose_name='备注')
    boolfield_bei_bao_ren_zheng_jian_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='被保人证件附件')
    boolfield_li_pei_dui_zhang_dan_qian_shu = models.ForeignKey(Qian_shu_que_ren, related_name='qian_shu_que_ren_for_boolfield_li_pei_dui_zhang_dan_qian_shu_li_pei_shen_qing_shu_shen_he', on_delete=models.CASCADE, null=True, blank=False, verbose_name='理赔对账单签署')
    boolfield_li_pei_dui_zhang_dan_tui_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='理赔对账单退单原因')
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_li_pei_shen_qing_shu_shen_he', blank=True, verbose_name='症状')
    boolfield_jian_cha_xiang_mu = models.ManyToManyField(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_jian_cha_xiang_mu_li_pei_shen_qing_shu_shen_he', blank=True, verbose_name='检查项目')
    boolfield_zhen_duan = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_zhen_duan_li_pei_shen_qing_shu_shen_he', on_delete=models.CASCADE, null=True, blank=False, verbose_name='诊断')
    boolfield_zhi_liao_xiang_mu = models.ManyToManyField(Icpc7_treatments, related_name='icpc7_treatments_for_boolfield_zhi_liao_xiang_mu_li_pei_shen_qing_shu_shen_he', blank=False, verbose_name='治疗项目')
    boolfield_qi_ta_jian_kang_gan_yu_fu_wu = models.ManyToManyField(Icpc8_other_health_interventions, related_name='icpc8_other_health_interventions_for_boolfield_qi_ta_jian_kang_gan_yu_fu_wu_li_pei_shen_qing_shu_shen_he', blank=True, verbose_name='其他健康干预服务')
    boolfield_fei_yong_he_ji = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='费用合计')
    boolfield_men_zhen_bing_li_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='门诊病历附件')
    boolfield_men_zhen_ji_lu_dan_tui_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='门诊记录单退单原因')
    boolfield_li_pei_men_zhen_ji_lu_qian_shu = models.ForeignKey(Qian_shu_que_ren, related_name='qian_shu_que_ren_for_boolfield_li_pei_men_zhen_ji_lu_qian_shu_li_pei_shen_qing_shu_shen_he', on_delete=models.CASCADE, null=True, blank=False, verbose_name='理赔门诊记录签署')
    boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu = models.ManyToManyField(Fu_wu_xiang_mu, related_name='fu_wu_xiang_mu_for_boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu_li_pei_shen_qing_shu_shen_he', blank=False, verbose_name='保单内服务收费项目')
    boolfield_bao_dan_nei_fu_wu_fei_yong = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='保单内服务费用')
    boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu = models.ManyToManyField(Fu_wu_xiang_mu, related_name='fu_wu_xiang_mu_for_boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu_li_pei_shen_qing_shu_shen_he', blank=False, verbose_name='保单外服务收费项目')
    boolfield_bao_dan_wai_fu_wu_fei_yong = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='保单外服务费用')
    boolfield_fei_yong_he_ji = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='费用合计')
    boolfield_hui_zong_fei_yong_qing_dan_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='汇总费用清单附件')
    boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu = models.ForeignKey(Qian_shu_que_ren, related_name='qian_shu_que_ren_for_boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu_li_pei_shen_qing_shu_shen_he', on_delete=models.CASCADE, null=True, blank=False, verbose_name='理赔费用汇总单签署')
    boolfield_li_pei_fei_yong_hui_zong_dan_tui_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='理赔费用汇总单退单原因')

    class Meta:
        verbose_name = '理赔申请审核'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Man_yi_du_diao_cha(HsscFormModel):
    boolfield_yi_liao_fu_wu_ji_neng_xiang_mu_ping_fen = models.ForeignKey(Ping_fen, related_name='ping_fen_for_boolfield_yi_liao_fu_wu_ji_neng_xiang_mu_ping_fen_man_yi_du_diao_cha', on_delete=models.CASCADE, null=True, blank=False, verbose_name='医疗服务技能项目评分')
    boolfield_ping_tai_fu_wu_xiang_mu_ping_fen = models.ForeignKey(Ping_fen, related_name='ping_fen_for_boolfield_ping_tai_fu_wu_xiang_mu_ping_fen_man_yi_du_diao_cha', on_delete=models.CASCADE, null=True, blank=False, verbose_name='平台服务项目评分')
    boolfield_fu_wu_liu_cheng_ping_fen = models.ForeignKey(Ping_fen, related_name='ping_fen_for_boolfield_fu_wu_liu_cheng_ping_fen_man_yi_du_diao_cha', on_delete=models.CASCADE, null=True, blank=False, verbose_name='服务流程评分')
    boolfield_xi_wang_zeng_jia_de_fu_wu_xiang_mu = models.CharField(max_length=255, null=True, blank=True, verbose_name='希望增加的服务项目')
    boolfield_fu_wu_xiao_lv_ping_fen = models.ForeignKey(Ping_fen, related_name='ping_fen_for_boolfield_fu_wu_xiao_lv_ping_fen_man_yi_du_diao_cha', on_delete=models.CASCADE, null=True, blank=False, verbose_name='服务效率评分')
    boolfield_you_dai_gai_jin_de_fu_wu = models.CharField(max_length=255, null=True, blank=True, verbose_name='有待改进的服务')

    class Meta:
        verbose_name = '满意度调查'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Zhen_hou_sui_fang(HsscFormModel):
    boolfield_zhi_liao_gan_shou_he_xiao_guo_ping_jia = models.ForeignKey(Fu_wu_xiao_guo_ping_jia, related_name='fu_wu_xiao_guo_ping_jia_for_boolfield_zhi_liao_gan_shou_he_xiao_guo_ping_jia_zhen_hou_sui_fang', on_delete=models.CASCADE, null=True, blank=False, verbose_name='治疗感受和效果评价')
    boolfield_deng_hou_qing_kuang = models.ForeignKey(Deng_hou_shi_jian, related_name='deng_hou_shi_jian_for_boolfield_deng_hou_qing_kuang_zhen_hou_sui_fang', on_delete=models.CASCADE, null=True, blank=False, verbose_name='等候情况')
    boolfield_cun_zai_de_wen_ti = models.CharField(max_length=255, null=True, blank=True, verbose_name='存在的问题')
    boolfield_you_dai_gai_jin_de_fu_wu = models.CharField(max_length=255, null=True, blank=True, verbose_name='有待改进的服务')
    boolfield_nin_de_dan_xin_he_gu_lv = models.CharField(max_length=255, null=True, blank=True, verbose_name='您的担心和顾虑')
    boolfield_nin_hai_xu_yao_de_fu_wu = models.CharField(max_length=255, null=True, blank=True, verbose_name='您还需要的服务')
    boolfield_nin_cong_he_chu_zhi_dao_wo_men_de_fu_wu = models.ForeignKey(Nin_cong_he_chu_zhi_dao_wo_men, related_name='nin_cong_he_chu_zhi_dao_wo_men_for_boolfield_nin_cong_he_chu_zhi_dao_wo_men_de_fu_wu_zhen_hou_sui_fang', on_delete=models.CASCADE, null=True, blank=True, verbose_name='您从何处知道我们的服务')
    boolfield_nin_shi_fou_yuan_yi_xiang_ta_ren_tui_jian_wo_men = models.ForeignKey(Shi_fou_yuan_yi_xiang_jia_ren_peng_you_tui_jian_wo_men_de_fu_wu, related_name='shi_fou_yuan_yi_xiang_jia_ren_peng_you_tui_jian_wo_men_de_fu_wu_for_boolfield_nin_shi_fou_yuan_yi_xiang_ta_ren_tui_jian_wo_men_zhen_hou_sui_fang', on_delete=models.CASCADE, null=True, blank=True, verbose_name='您是否愿意向他人推荐我们')

    class Meta:
        verbose_name = '诊后回访'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Zhen_jian_sui_fang(HsscFormModel):
    boolfield_deng_hou_qing_kuang = models.ForeignKey(Deng_hou_shi_jian, related_name='deng_hou_shi_jian_for_boolfield_deng_hou_qing_kuang_zhen_jian_sui_fang', on_delete=models.CASCADE, null=True, blank=False, verbose_name='等候情况')
    boolfield_jie_dai_fu_wu = models.ForeignKey(Jie_dai_fu_wu, related_name='jie_dai_fu_wu_for_boolfield_jie_dai_fu_wu_zhen_jian_sui_fang', on_delete=models.CASCADE, null=True, blank=False, verbose_name='接待服务')
    boolfield_zhi_liao_jian_gou_tong_qing_kuang = models.ForeignKey(Gou_tong_qing_kuang, related_name='gou_tong_qing_kuang_for_boolfield_zhi_liao_jian_gou_tong_qing_kuang_zhen_jian_sui_fang', on_delete=models.CASCADE, null=True, blank=False, verbose_name='治疗间沟通情况')
    boolfield_zhi_liao_gan_shou_he_xiao_guo_ping_jia = models.ForeignKey(Fu_wu_xiao_guo_ping_jia, related_name='fu_wu_xiao_guo_ping_jia_for_boolfield_zhi_liao_gan_shou_he_xiao_guo_ping_jia_zhen_jian_sui_fang', on_delete=models.CASCADE, null=True, blank=False, verbose_name='治疗感受和效果评价')
    boolfield_nin_de_dan_xin_he_gu_lv = models.CharField(max_length=255, null=True, blank=True, verbose_name='您的担心和顾虑')
    boolfield_cun_zai_de_wen_ti = models.CharField(max_length=255, null=True, blank=True, verbose_name='存在的问题')
    boolfield_nin_xiang_yao_de_bang_zhu = models.CharField(max_length=255, null=True, blank=True, verbose_name='您想要的帮助')
    boolfield_qi_ta_xu_qiu = models.CharField(max_length=255, null=True, blank=True, verbose_name='其他需求')

    class Meta:
        verbose_name = '诊间随访'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Men_zhen_ji_lu(HsscFormModel):
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_men_zhen_ji_lu', blank=True, verbose_name='症状')
    boolfield_jian_cha_xiang_mu = models.ManyToManyField(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_jian_cha_xiang_mu_men_zhen_ji_lu', blank=True, verbose_name='检查项目')
    boolfield_zhen_duan = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_zhen_duan_men_zhen_ji_lu', on_delete=models.CASCADE, null=True, blank=False, verbose_name='诊断')
    boolfield_zhi_liao_xiang_mu = models.ManyToManyField(Icpc7_treatments, related_name='icpc7_treatments_for_boolfield_zhi_liao_xiang_mu_men_zhen_ji_lu', blank=False, verbose_name='治疗项目')
    boolfield_qi_ta_jian_kang_gan_yu_fu_wu = models.ManyToManyField(Icpc8_other_health_interventions, related_name='icpc8_other_health_interventions_for_boolfield_qi_ta_jian_kang_gan_yu_fu_wu_men_zhen_ji_lu', blank=True, verbose_name='其他健康干预服务')
    boolfield_fei_yong_he_ji = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='费用合计')
    boolfield_men_zhen_bing_li_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='门诊病历附件')

    class Meta:
        verbose_name = '门诊记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Yu_yue_tong_zhi(HsscFormModel):
    boolfield_ji_gou_ming_cheng = models.CharField(max_length=255, null=True, blank=False, verbose_name='机构名称')
    boolfield_yu_yue_xu_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='预约序号')
    boolfield_ji_gou_lian_xi_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='机构联系地址')
    boolfield_ji_gou_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=False, verbose_name='机构联系电话')
    boolfield_jiu_zhen_yi_sheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='就诊医生')
    boolfield_yu_yue_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='预约时间')
    boolfield_jiu_zhen_wen_ti = models.CharField(max_length=255, null=True, blank=False, verbose_name='就诊问题')
    boolfield_jiu_zhen_ji_gou_ze_ren_ren = models.ForeignKey(Staff, related_name='staff_for_boolfield_jiu_zhen_ji_gou_ze_ren_ren_yu_yue_tong_zhi', on_delete=models.CASCADE, null=True, blank=True, verbose_name='就诊机构责任人')
    boolfield_shi_yong_fu_wu_chan_pin = models.ManyToManyField(Bao_xian_chan_pin, related_name='bao_xian_chan_pin_for_boolfield_shi_yong_fu_wu_chan_pin_yu_yue_tong_zhi', blank=True, verbose_name='使用服务产品')
    boolfield_fu_jia_fu_wu_yao_qiu = models.CharField(max_length=255, null=True, blank=True, verbose_name='附加服务要求')

    class Meta:
        verbose_name = '预约通知'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Fen_zhen_que_ren(HsscFormModel):
    boolfield_dao_dian_shen_fen_yan_zheng = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='到店身份验证')
    boolfield_dao_da_que_ren = models.ForeignKey(Qian_dao_que_ren, related_name='qian_dao_que_ren_for_boolfield_dao_da_que_ren_fen_zhen_que_ren', on_delete=models.CASCADE, null=True, blank=False, verbose_name='到达确认')
    boolfield_yu_yue_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='预约时间')
    boolfield_jiu_zhen_wen_ti = models.CharField(max_length=255, null=True, blank=False, verbose_name='就诊问题')
    boolfield_jiu_zhen_ji_gou_ze_ren_ren = models.ForeignKey(Staff, related_name='staff_for_boolfield_jiu_zhen_ji_gou_ze_ren_ren_fen_zhen_que_ren', on_delete=models.CASCADE, null=True, blank=True, verbose_name='就诊机构责任人')
    boolfield_shi_yong_fu_wu_chan_pin = models.ManyToManyField(Bao_xian_chan_pin, related_name='bao_xian_chan_pin_for_boolfield_shi_yong_fu_wu_chan_pin_fen_zhen_que_ren', blank=True, verbose_name='使用服务产品')
    boolfield_fu_jia_fu_wu_yao_qiu = models.CharField(max_length=255, null=True, blank=True, verbose_name='附加服务要求')

    class Meta:
        verbose_name = '到店确认'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Yu_yue_que_ren(HsscFormModel):
    boolfield_yu_yue_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='预约时间')
    boolfield_jiu_zhen_wen_ti = models.CharField(max_length=255, null=True, blank=False, verbose_name='就诊问题')
    boolfield_jiu_zhen_ji_gou_ze_ren_ren = models.ForeignKey(Staff, related_name='staff_for_boolfield_jiu_zhen_ji_gou_ze_ren_ren_yu_yue_que_ren', on_delete=models.CASCADE, null=True, blank=True, verbose_name='就诊机构责任人')
    boolfield_shi_yong_fu_wu_chan_pin = models.ManyToManyField(Bao_xian_chan_pin, related_name='bao_xian_chan_pin_for_boolfield_shi_yong_fu_wu_chan_pin_yu_yue_que_ren', blank=True, verbose_name='使用服务产品')
    boolfield_fu_jia_fu_wu_yao_qiu = models.CharField(max_length=255, null=True, blank=True, verbose_name='附加服务要求')
    boolfield_jie_dan_que_ren = models.ForeignKey(Jie_dan_que_ren, related_name='jie_dan_que_ren_for_boolfield_jie_dan_que_ren_yu_yue_que_ren', on_delete=models.CASCADE, null=True, blank=False, verbose_name='接单确认')
    boolfield_ju_jue_jie_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='拒绝接单原因')

    class Meta:
        verbose_name = '预约确认'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Yu_yue_an_pai(HsscFormModel):
    boolfield_yu_yue_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='预约时间')
    boolfield_jiu_zhen_wen_ti = models.CharField(max_length=255, null=True, blank=False, verbose_name='就诊问题')
    boolfield_jiu_zhen_ji_gou_ze_ren_ren = models.ForeignKey(Staff, related_name='staff_for_boolfield_jiu_zhen_ji_gou_ze_ren_ren_yu_yue_an_pai', on_delete=models.CASCADE, null=True, blank=True, verbose_name='就诊机构责任人')
    boolfield_shi_yong_fu_wu_chan_pin = models.ManyToManyField(Bao_xian_chan_pin, related_name='bao_xian_chan_pin_for_boolfield_shi_yong_fu_wu_chan_pin_yu_yue_an_pai', blank=True, verbose_name='使用服务产品')
    boolfield_fu_jia_fu_wu_yao_qiu = models.CharField(max_length=255, null=True, blank=True, verbose_name='附加服务要求')

    class Meta:
        verbose_name = '平台预约安排'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Ji_gou_ji_ben_xin_xi_biao(HsscBaseFormModel):
    boolfield_ji_gou_lian_xi_di_zhi = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构联系地址')
    boolfield_ji_gou_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构编码')
    boolfield_ji_gou_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构名称')
    boolfield_ji_gou_dai_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构代码')
    boolfield_ji_gou_shu_xing = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构属性')
    boolfield_ji_gou_ceng_ji = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构层级')
    boolfield_suo_zai_hang_zheng_qu_hua_dai_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='所在行政区划代码')
    boolfield_xing_zheng_qu_hua_gui_shu = models.CharField(max_length=255, null=True, blank=True, verbose_name='行政区划归属')
    boolfield_fa_ding_fu_ze_ren = models.CharField(max_length=255, null=True, blank=True, verbose_name='法定负责人')
    boolfield_ji_gou_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构联系电话')

    class Meta:
        verbose_name = '机构基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Zhi_yuan_ji_ben_xin_xi_biao(HsscBaseFormModel):
    boolfield_zheng_jian_hao_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='证件号码')
    boolfield_zhi_ye_zi_zhi = models.CharField(max_length=255, null=True, blank=True, verbose_name='执业资质')
    boolfield_zhuan_chang = models.CharField(max_length=255, null=True, blank=True, verbose_name='专长')
    boolfield_zhi_ye_shi_jian = models.CharField(max_length=255, null=True, blank=True, verbose_name='执业时间')
    boolfield_zhi_yuan_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='职员编码')
    boolfield_ji_gou_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构联系电话')
    boolfield_bei_bao_ren_xing_ming = models.CharField(max_length=255, null=True, blank=True, verbose_name='被保人姓名')
    boolfield_suo_shu_ji_gou = models.ForeignKey(Institution, related_name='institution_for_boolfield_suo_shu_ji_gou_zhi_yuan_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='所属机构')
    boolfield_fu_wu_jue_se = models.ManyToManyField(Fu_wu_jue_se, related_name='fu_wu_jue_se_for_boolfield_fu_wu_jue_se_zhi_yuan_ji_ben_xin_xi_biao', blank=True, verbose_name='服务角色')

    class Meta:
        verbose_name = '职员基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_cha(HsscFormModel):

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
    boolfield_ji_gou_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构联系电话')
    boolfield_she_bei_shi_yong_fu_wu_gong_neng = models.ForeignKey(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_she_bei_shi_yong_fu_wu_gong_neng_she_bei_ji_ben_xin_xi_ji_lu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='设备适用服务功能')

    class Meta:
        verbose_name = '设备基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Gong_ying_shang_ji_ben_xin_xi_diao_cha(HsscFormModel):

    class Meta:
        verbose_name = '物料供应商基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Yao_pin_ji_ben_xin_xi_biao(HsscFormModel):

    class Meta:
        verbose_name = '药品基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Ju_min_ji_ben_xin_xi_diao_cha(HsscBaseFormModel):
    boolfield_xu_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='序号')
    boolfield_bao_dan_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='保单号')
    boolfield_zheng_jian_lei_xing = models.ForeignKey(Zheng_jian_lei_xing, related_name='zheng_jian_lei_xing_for_boolfield_zheng_jian_lei_xing_ju_min_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=False, verbose_name='证件类型')
    boolfield_zheng_jian_hao_ma = models.CharField(max_length=255, null=True, blank=False, verbose_name='证件号码')
    boolfield_bei_bao_ren_xing_ming = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人姓名')
    boolfield_bei_bao_ren_xing_bie = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人性别')
    boolfield_chu_sheng_ri_qi = models.DateField(null=True, blank=False, verbose_name='出生日期')
    boolfield_bao_xian_ze_ren = models.CharField(max_length=255, null=True, blank=False, verbose_name='保险责任')
    boolfield_bao_xian_you_xiao_qi = models.DateField(null=True, blank=False, verbose_name='保险有效期')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=False, verbose_name='联系电话')
    boolfield_chang_zhu_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='常住地址')

    class Meta:
        verbose_name = '基本信息调查'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
