from django.db import models

from icpc.models import *
from dictionaries.models import *
from core.models import HsscFormModel, ManagedEntity, OperationProc, VirtualStaff, Staff, Institution, Service, ServicePackage, Customer, CycleUnit, Medicine
from core.hsscbase_class import HsscBase

from django.db.models import Q, F
from django.utils import timezone
from datetime import timedelta

from pypinyin import lazy_pinyin

def get_profile_name(customer):
    # 获取客户基本信息表model和系统API字段，用于查询hssc_customer_number和hssc_name
    customer_entity = ManagedEntity.objects.get(name='customer')
    customer_profile_model = customer_entity.base_form.service_set.all()[0].name.capitalize()
    api_fields_map = customer_entity.base_form.api_fields
    hssc_name_field = api_fields_map.get('hssc_name', None).get('field_name')
    profile = eval(customer_profile_model).objects.filter(customer=customer).last()
    if profile:
        hssc_name = getattr(profile, hssc_name_field)
        if hssc_name:
            return hssc_name
    return None


class CustomerSchedulePackage(HsscFormModel):
    servicepackage = models.ForeignKey(ServicePackage, on_delete=models.CASCADE, verbose_name='服务包')
    start_time = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name='开始时间')

    class Meta:
        verbose_name = '安排服务包'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.servicepackage.label

class CustomerScheduleList(HsscFormModel):
    plan_serial_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='服务计划')
    schedule_package = models.ForeignKey(CustomerSchedulePackage, null=True, on_delete=models.CASCADE, verbose_name='服务包')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    is_ready = models.BooleanField(default=False, verbose_name='已生成schedules')
    
    class Meta:
        verbose_name = '客户服务计划'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.plan_serial_number

class CustomerScheduleDraft(HsscBase):
    order = models.PositiveSmallIntegerField(default=100, verbose_name='顺序')
    schedule_package = models.ForeignKey(CustomerSchedulePackage, null=True, on_delete=models.CASCADE, verbose_name='服务包')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    cycle_unit = models.ForeignKey(CycleUnit, on_delete=models.CASCADE, default=1, blank=True, null=True, verbose_name='周期单位')
    cycle_frequency = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="每周期频次")
    cycle_times = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="天数")
    Default_beginning_time = [(0, '指定开始时间'), (1, '当前系统时间'), (2, '首个服务开始时间'), (3, '上个服务结束时间'), (4, '客户出生日期')]
    default_beginning_time = models.PositiveSmallIntegerField(choices=Default_beginning_time, default=0, verbose_name='执行时间基准')
    base_interval = models.DurationField(blank=True, null=True, verbose_name='基准间隔', help_text='例如：3 days, 22:00:00')
    # 根据当前service的值动态筛选有服务权限的服务人员
    scheduled_operator = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True, verbose_name='服务人员')
    # 优先操作人员仅限工作小组
    priority_operator = models.ForeignKey(VirtualStaff, on_delete=models.SET_NULL, limit_choices_to={'is_workgroup': True}, blank=True, null=True, verbose_name="优先操作员")
    overtime = models.DurationField(blank=True, null=True, verbose_name='超期时限')
    
    class Meta:
        verbose_name = '服务项目安排'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.service.label

class CustomerSchedule(HsscFormModel):
    customer_schedule_list = models.ForeignKey(CustomerScheduleList, null=True, blank=True, on_delete=models.CASCADE, verbose_name='服务计划')
    schedule_package = models.ForeignKey(CustomerSchedulePackage, null=True, blank=True, on_delete=models.CASCADE, verbose_name='服务包')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    scheduled_time = models.DateTimeField(blank=True, null=True, verbose_name='计划执行时间')
    scheduled_operator = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True, verbose_name='计划服务人员')
    priority_operator = models.ForeignKey(VirtualStaff, on_delete=models.SET_NULL, limit_choices_to={'is_workgroup': True}, blank=True, null=True, verbose_name="优先操作员")
    reference_operation = models.ManyToManyField(OperationProc, blank=True, limit_choices_to=Q(customer=F('customer'), service__service_type=2, created_time__gte=timezone.now() - timedelta(days=7)), verbose_name='引用表单')
    overtime = models.DurationField(blank=True, null=True, verbose_name='超期时限')
    is_assigned = models.BooleanField(default=False, verbose_name='已生成任务')

    class Meta:
        verbose_name = '客户服务日程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.service.label


# **********************************************************************************************************************
# Service基本信息表单Model
# **********************************************************************************************************************
class Fa_yao_tong_zhi(HsscFormModel):
    boolfield_tong_zhi = models.CharField(max_length=255, default="您的处方药已发出，请及时到药房领取。", null=True, blank=True, verbose_name='通知')

    class Meta:
        verbose_name = '发药通知'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Kong_fu_xue_tang_jian_cha_jie_guo_tong_zhi(HsscFormModel):
    boolfield_tong_zhi = models.CharField(max_length=255, default="您的检查结果已出，请及时查看。", null=True, blank=False, verbose_name='通知')

    class Meta:
        verbose_name = '空腹血糖检查结果通知'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Yu_yue_tong_zhi(HsscFormModel):
    boolfield_yu_yue_shi_jian = models.DateTimeField(null=True, blank=True, verbose_name='预约时间')
    boolfield_ze_ren_ren = models.ForeignKey(VirtualStaff, related_name='virtualstaff_for_boolfield_ze_ren_ren_yu_yue_tong_zhi', on_delete=models.CASCADE, null=True, blank=True, verbose_name='责任人')
    boolfield_yu_yue_xu_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='预约序号')
    boolfield_ji_gou_ming_cheng = models.CharField(max_length=255, default="金盘第一社区卫生服务站", null=True, blank=False, verbose_name='机构名称')
    boolfield_lian_xi_di_zhi = models.CharField(max_length=255, default="海口市龙华区金花路2号", null=True, blank=False, verbose_name='联系地址')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, default="66821120", null=True, blank=False, verbose_name='联系电话')
    boolfield_tong_zhi_que_ren = models.ForeignKey(Jie_shou_tong_zhi, related_name='jie_shou_tong_zhi_for_boolfield_tong_zhi_que_ren_yu_yue_tong_zhi', on_delete=models.CASCADE, null=True, blank=False, verbose_name='通知确认')

    class Meta:
        verbose_name = '预约通知'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Shuang_xiang_zhuan_zhen_zhuan_chu(HsscFormModel):
    boolfield_zhuan_zhen_ji_gou_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='转诊机构名称')
    boolfield_zhuan_zhen_shuo_ming = models.CharField(max_length=255, default="现有患者因病情需要，需转入贵单位，请予以接诊。", null=True, blank=True, verbose_name='转诊说明')
    boolfield_chu_bu_yin_xiang = models.CharField(max_length=255, null=True, blank=True, verbose_name='初步印象')
    boolfield_zhu_yao_xian_bing_shi = models.ManyToManyField(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_zhu_yao_xian_bing_shi_shuang_xiang_zhuan_zhen_zhuan_chu', blank=True, verbose_name='主要现病史')
    boolfield_zhu_yao_ji_wang_shi = models.ManyToManyField(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_zhu_yao_ji_wang_shi_shuang_xiang_zhuan_zhen_zhuan_chu', blank=True, verbose_name='主要既往史')
    boolfield_zhuan_zhen_yi_sheng_qian_zi = models.CharField(max_length=255, null=True, blank=True, verbose_name='转诊医生签字')
    boolfield_ji_gou_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构名称')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    boolfield_zhuan_zhen_ri_qi = models.DateField(null=True, blank=True, verbose_name='转诊日期')

    class Meta:
        verbose_name = '双向转诊转出'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Hui_zhen_zhen_duan_fu_wu(HsscFormModel):
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_hui_zhen_zhen_duan_fu_wu', blank=True, verbose_name='症状')
    boolfield_hui_zhen_zhen_duan_jie_guo = models.ManyToManyField(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_hui_zhen_zhen_duan_jie_guo_hui_zhen_zhen_duan_fu_wu', blank=True, verbose_name='会诊诊断结果')

    class Meta:
        verbose_name = '会诊诊断服务'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Hui_zhen_zhen_duan_fu_wu_list(models.Model):
    hui_zhen_zhen_duan_fu_wu = models.ForeignKey(Hui_zhen_zhen_duan_fu_wu, on_delete=models.CASCADE, verbose_name='会诊诊断服务')
    boolfield_hui_zhen_jian_yi = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_hui_zhen_jian_yi_hui_zhen_zhen_duan_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='会诊建议')
    boolfield_qi_ta = models.CharField(max_length=255, null=True, blank=True, verbose_name='其他')
    boolfield_hui_zhen_ze_ren_ren = models.ForeignKey(VirtualStaff, related_name='virtualstaff_for_boolfield_hui_zhen_ze_ren_ren_hui_zhen_zhen_duan_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='会诊责任人')

    class Meta:
        verbose_name = '会诊诊断服务明细'
        verbose_name_plural = verbose_name

class Hui_zhen_jian_yi_fu_wu(HsscFormModel):
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_hui_zhen_jian_yi_fu_wu', blank=True, verbose_name='症状')
    boolfield_hui_zhen_ze_ren_ren = models.ForeignKey(VirtualStaff, related_name='virtualstaff_for_boolfield_hui_zhen_ze_ren_ren_hui_zhen_jian_yi_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='会诊责任人')

    class Meta:
        verbose_name = '会诊建议服务'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Hui_zhen_jian_yi_fu_wu_list(models.Model):
    hui_zhen_jian_yi_fu_wu = models.ForeignKey(Hui_zhen_jian_yi_fu_wu, on_delete=models.CASCADE, verbose_name='会诊建议服务')
    boolfield_hui_zhen_jian_yi = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_hui_zhen_jian_yi_hui_zhen_jian_yi_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='会诊建议')
    boolfield_qi_ta = models.CharField(max_length=255, null=True, blank=True, verbose_name='其他')

    class Meta:
        verbose_name = '会诊建议服务明细'
        verbose_name_plural = verbose_name

class Hui_zhen_shen_qing_fu_wu(HsscFormModel):
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_hui_zhen_shen_qing_fu_wu', blank=True, verbose_name='症状')
    boolfield_hui_zhen_ren = models.ManyToManyField(VirtualStaff, related_name='virtualstaff_for_boolfield_hui_zhen_ren_hui_zhen_shen_qing_fu_wu', blank=True, verbose_name='会诊人')

    class Meta:
        verbose_name = '会诊申请服务'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Yong_yao_hui_fang_fu_wu(HsscFormModel):

    class Meta:
        verbose_name = '用药回访服务'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Tang_niao_bing_jian_kang_jiao_yu_fu_wu(HsscFormModel):
    boolfield_jian_kang_jiao_yu_chu_fang = models.CharField(max_length=255, default="糖尿病是一组以高血糖为特征的代谢性疾病.多饮,多食,多尿,体重下降是其典型症状,合称“三多一少”.", null=True, blank=False, verbose_name='健康教育处方')

    class Meta:
        verbose_name = '糖尿病健康教育服务'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        

def get_yi_xing_tang_niao_bing_zhen_duan_boolfield_ji_bing_ming_cheng_instance():
    return Icpc5_evaluation_and_diagnoses.objects.get(iname="胰岛素依赖型糖尿病")

class Yi_xing_tang_niao_bing_zhen_duan(HsscFormModel):
    boolfield_ji_bing_ming_cheng = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_ji_bing_ming_cheng_yi_xing_tang_niao_bing_zhen_duan', on_delete=models.CASCADE, default=get_yi_xing_tang_niao_bing_zhen_duan_boolfield_ji_bing_ming_cheng_instance, null=True, blank=True, verbose_name='疾病名称')
    boolfield_shi_fou_hui_zhen = models.ForeignKey(Shi_fou_hui_zhen, related_name='shi_fou_hui_zhen_for_boolfield_shi_fou_hui_zhen_yi_xing_tang_niao_bing_zhen_duan', on_delete=models.CASCADE, null=True, blank=True, verbose_name='是否会诊')
    boolfield_shi_fou_zhuan_zhen = models.ForeignKey(Shi_fou_zhuan_zhen, related_name='shi_fou_zhuan_zhen_for_boolfield_shi_fou_zhuan_zhen_yi_xing_tang_niao_bing_zhen_duan', on_delete=models.CASCADE, null=True, blank=True, verbose_name='是否转诊')

    class Meta:
        verbose_name = '一型糖尿病诊断'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Zhu_she_fu_wu(HsscFormModel):
    boolfield_zhi_xing_qian_ming = models.CharField(max_length=255, null=True, blank=True, verbose_name='执行签名')
    boolfield_yong_yao_liao_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药疗程')
    boolfield_zhu_she_ri_qi = models.DateTimeField(null=True, blank=True, verbose_name='注射日期')

    class Meta:
        verbose_name = '门诊注射服务'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Zhu_she_fu_wu_list(models.Model):
    zhu_she_fu_wu = models.ForeignKey(Zhu_she_fu_wu, on_delete=models.CASCADE, verbose_name='门诊注射服务')
    boolfield_yao_pin_ming = models.ForeignKey(Medicine, related_name='medicine_for_boolfield_yao_pin_ming_zhu_she_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='药品名')
    boolfield_yong_yao_pin_ci = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药频次')
    boolfield_gui_ge = models.CharField(max_length=255, null=True, blank=True, verbose_name='规格')
    boolfield_chang_yong_ji_liang = models.CharField(max_length=255, null=True, blank=True, verbose_name='常用剂量')

    class Meta:
        verbose_name = '门诊注射服务明细'
        verbose_name_plural = verbose_name

class Yun_dong_chu_fang(HsscFormModel):
    boolfield_ji_bing_ming_cheng = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_ji_bing_ming_cheng_yun_dong_chu_fang', on_delete=models.CASCADE, null=True, blank=True, verbose_name='疾病名称')
    boolfield_yun_dong_gan_yu = models.ManyToManyField(Icpc8_other_health_interventions, related_name='icpc8_other_health_interventions_for_boolfield_yun_dong_gan_yu_yun_dong_chu_fang', blank=True, verbose_name='运动干预')

    class Meta:
        verbose_name = '运动处方'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Ying_yang_chu_fang(HsscFormModel):
    boolfield_ji_bing_ming_cheng = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_ji_bing_ming_cheng_ying_yang_chu_fang', on_delete=models.CASCADE, null=True, blank=True, verbose_name='疾病名称')
    boolfield_ying_yang_gan_yu = models.ManyToManyField(Icpc8_other_health_interventions, related_name='icpc8_other_health_interventions_for_boolfield_ying_yang_gan_yu_ying_yang_chu_fang', blank=True, verbose_name='营养干预')

    class Meta:
        verbose_name = '营养处方'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Yuan_wai_jian_ce_can_hou_2_xiao_shi_xue_tang(HsscFormModel):
    boolfield_can_hou_2_xiao_shi_xue_tang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='餐后2小时血糖')

    class Meta:
        verbose_name = '院外监测餐后2小时血糖'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Yuan_wai_jian_ce_kong_fu_xue_tang(HsscFormModel):
    boolfield_kong_fu_xue_tang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='空腹血糖')

    class Meta:
        verbose_name = '院外监测空腹血糖'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Man_yi_du_diao_cha(HsscFormModel):
    boolfield_yi_liao_fu_wu_ji_neng_xiang_mu_ping_fen = models.ForeignKey(Ping_fen, related_name='ping_fen_for_boolfield_yi_liao_fu_wu_ji_neng_xiang_mu_ping_fen_man_yi_du_diao_cha', on_delete=models.CASCADE, null=True, blank=False, verbose_name='医疗服务技能项目评分')
    boolfield_ping_tai_fu_wu_xiang_mu_ping_fen = models.ForeignKey(Ping_fen, related_name='ping_fen_for_boolfield_ping_tai_fu_wu_xiang_mu_ping_fen_man_yi_du_diao_cha', on_delete=models.CASCADE, null=True, blank=False, verbose_name='平台服务项目评分')
    boolfield_fu_wu_liu_cheng_ping_fen = models.ForeignKey(Ping_fen, related_name='ping_fen_for_boolfield_fu_wu_liu_cheng_ping_fen_man_yi_du_diao_cha', on_delete=models.CASCADE, null=True, blank=False, verbose_name='服务流程评分')
    boolfield_fu_wu_xiao_lv_ping_fen = models.ForeignKey(Ping_fen, related_name='ping_fen_for_boolfield_fu_wu_xiao_lv_ping_fen_man_yi_du_diao_cha', on_delete=models.CASCADE, null=True, blank=False, verbose_name='服务效率评分')
    boolfield_xi_wang_zeng_jia_de_fu_wu_xiang_mu = models.CharField(max_length=255, null=True, blank=True, verbose_name='希望增加的服务项目')
    boolfield_you_dai_gai_jin_de_fu_wu = models.CharField(max_length=255, null=True, blank=True, verbose_name='有待改进的服务')

    class Meta:
        verbose_name = '满意度调查'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Zhen_hou_sui_fang(HsscFormModel):
    boolfield_zhi_liao_gan_shou_he_xiao_guo_ping_jia = models.ForeignKey(Fu_wu_xiao_guo_ping_jia, related_name='fu_wu_xiao_guo_ping_jia_for_boolfield_zhi_liao_gan_shou_he_xiao_guo_ping_jia_zhen_hou_sui_fang', on_delete=models.CASCADE, null=True, blank=False, verbose_name='治疗感受和效果评价')
    boolfield_deng_hou_qing_kuang = models.ForeignKey(Deng_hou_shi_jian, related_name='deng_hou_shi_jian_for_boolfield_deng_hou_qing_kuang_zhen_hou_sui_fang', on_delete=models.CASCADE, null=True, blank=False, verbose_name='等候情况')
    boolfield_cun_zai_de_wen_ti = models.CharField(max_length=255, null=True, blank=True, verbose_name='存在的问题')
    boolfield_you_dai_gai_jin_de_fu_wu = models.CharField(max_length=255, null=True, blank=True, verbose_name='有待改进的服务')
    boolfield_nin_de_dan_xin_he_gu_lv = models.CharField(max_length=255, null=True, blank=True, verbose_name='您的担心和顾虑')
    boolfield_nin_hai_xu_yao_de_fu_wu = models.CharField(max_length=255, null=True, blank=True, verbose_name='您还需要的服务')
    boolfield_nin_cong_he_chu_zhi_dao_wo_men_de_fu_wu = models.ForeignKey(Nin_cong_he_chu_zhi_dao_wo_men, related_name='nin_cong_he_chu_zhi_dao_wo_men_for_boolfield_nin_cong_he_chu_zhi_dao_wo_men_de_fu_wu_zhen_hou_sui_fang', on_delete=models.CASCADE, null=True, blank=True, verbose_name='您从何处知道我们的服务')
    boolfield_nin_shi_fou_yuan_yi_xiang_ta_ren_tui_jian_wo_men = models.ForeignKey(Shi_fou_yuan_yi_xiang_jia_ren_peng_you_tui_jian_wo_men_de_fu_wu, related_name='shi_fou_yuan_yi_xiang_jia_ren_peng_you_tui_jian_wo_men_de_fu_wu_for_boolfield_nin_shi_fou_yuan_yi_xiang_ta_ren_tui_jian_wo_men_zhen_hou_sui_fang', on_delete=models.CASCADE, null=True, blank=True, verbose_name='您是否愿意向他人推荐我们')
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
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Xue_ya_jian_ce_ping_gu(HsscFormModel):
    boolfield_xue_ya_jian_ce_ping_gu = models.ForeignKey(Sui_fang_ping_gu, related_name='sui_fang_ping_gu_for_boolfield_xue_ya_jian_ce_ping_gu_xue_ya_jian_ce_ping_gu', on_delete=models.CASCADE, null=True, blank=False, verbose_name='血压监测评估')

    class Meta:
        verbose_name = '血压监测评估'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Can_hou_2_xiao_shi_xue_tang(HsscFormModel):
    boolfield_can_hou_2_xiao_shi_xue_tang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='餐后2小时血糖')

    class Meta:
        verbose_name = '门诊餐后2小时血糖'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Ji_gou_ji_ben_xin_xi_biao(HsscFormModel):
    boolfield_lian_xi_di_zhi = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    boolfield_ji_gou_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构编码')
    boolfield_ji_gou_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构名称')
    boolfield_ji_gou_dai_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构代码')
    boolfield_ji_gou_shu_xing = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构属性')
    boolfield_ji_gou_ceng_ji = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构层级')
    boolfield_suo_zai_hang_zheng_qu_hua_dai_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='所在行政区划代码')
    boolfield_xing_zheng_qu_hua_gui_shu = models.CharField(max_length=255, null=True, blank=True, verbose_name='行政区划归属')
    boolfield_fa_ding_fu_ze_ren = models.CharField(max_length=255, null=True, blank=True, verbose_name='法定负责人')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    pym = models.CharField(max_length=255, blank=True, null=True, verbose_name="拼音码")
        

    class Meta:
        verbose_name = '机构基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
    def save(self, *args, **kwargs):
        if self.name:
            self.pym = ''.join(lazy_pinyin(self.label, style=Style.FIRST_LETTER))
        super().save(*args, **kwargs)
    
    def natural_key(self):
        return self.name

        
class Zhi_yuan_ji_ben_xin_xi_biao(HsscFormModel):
    boolfield_shen_fen_zheng_hao_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='身份证号码')
    boolfield_zhi_ye_zi_zhi = models.CharField(max_length=255, null=True, blank=True, verbose_name='执业资质')
    boolfield_zhuan_chang = models.CharField(max_length=255, null=True, blank=True, verbose_name='专长')
    boolfield_zhi_ye_shi_jian = models.CharField(max_length=255, null=True, blank=True, verbose_name='执业时间')
    boolfield_zhi_yuan_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='职员编码')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    boolfield_xing_ming = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    boolfield_suo_shu_ji_gou = models.ForeignKey(Institution, related_name='institution_for_boolfield_suo_shu_ji_gou_zhi_yuan_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='所属机构')
    boolfield_fu_wu_jue_se = models.ManyToManyField(Fu_wu_jue_se, related_name='fu_wu_jue_se_for_boolfield_fu_wu_jue_se_zhi_yuan_ji_ben_xin_xi_biao', blank=True, verbose_name='服务角色')
    pym = models.CharField(max_length=255, blank=True, null=True, verbose_name="拼音码")
        

    class Meta:
        verbose_name = '职员基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
    def save(self, *args, **kwargs):
        if self.name:
            self.pym = ''.join(lazy_pinyin(self.label, style=Style.FIRST_LETTER))
        super().save(*args, **kwargs)
    
    def natural_key(self):
        return self.name

        
class Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_cha(HsscFormModel):
    boolfield_lian_xi_di_zhi = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    boolfield_ji_gou_dai_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构代码')
    boolfield_ji_gou_shu_xing = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构属性')
    boolfield_gong_ying_shang_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='供应商编码')
    boolfield_zhuan_ye_fu_wu = models.CharField(max_length=255, null=True, blank=True, verbose_name='专业服务')
    boolfield_gong_ying_shang_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='供应商名称')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    boolfield_xin_yu_ping_ji = models.ForeignKey(Xin_yu_ping_ji, related_name='xin_yu_ping_ji_for_boolfield_xin_yu_ping_ji_fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='信誉评级')

    class Meta:
        verbose_name = '服务分供机构基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class She_bei_ji_ben_xin_xi_ji_lu(HsscFormModel):
    boolfield_she_bei_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备编码')
    boolfield_sheng_chan_chang_jia = models.CharField(max_length=255, null=True, blank=True, verbose_name='生产厂家')
    boolfield_she_bei_fu_wu_dan_wei_hao_shi = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备服务单位耗时')
    boolfield_she_bei_jian_xiu_zhou_qi = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备检修周期')
    boolfield_she_bei_shi_yong_cheng_ben = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备使用成本')
    boolfield_she_bei_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备名称')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    boolfield_she_bei_shi_yong_fu_wu_gong_neng = models.ForeignKey(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_she_bei_shi_yong_fu_wu_gong_neng_she_bei_ji_ben_xin_xi_ji_lu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='设备适用服务功能')
    pym = models.CharField(max_length=255, blank=True, null=True, verbose_name="拼音码")
        

    class Meta:
        verbose_name = '设备基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
    def save(self, *args, **kwargs):
        if self.name:
            self.pym = ''.join(lazy_pinyin(self.label, style=Style.FIRST_LETTER))
        super().save(*args, **kwargs)
    
    def natural_key(self):
        return self.name

        
class Gong_ying_shang_ji_ben_xin_xi_diao_cha(HsscFormModel):
    boolfield_lian_xi_di_zhi = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    boolfield_gong_ying_shang_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='供应商编码')
    boolfield_zhu_yao_gong_ying_chan_pin = models.CharField(max_length=255, null=True, blank=True, verbose_name='主要供应产品')
    boolfield_gong_huo_zhou_qi = models.CharField(max_length=255, null=True, blank=True, verbose_name='供货周期')
    boolfield_gong_ying_shang_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='供应商名称')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    boolfield_xin_yu_ping_ji = models.ForeignKey(Xin_yu_ping_ji, related_name='xin_yu_ping_ji_for_boolfield_xin_yu_ping_ji_gong_ying_shang_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='信誉评级')
    pym = models.CharField(max_length=255, blank=True, null=True, verbose_name="拼音码")
        

    class Meta:
        verbose_name = '物料供应商基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
    def save(self, *args, **kwargs):
        if self.name:
            self.pym = ''.join(lazy_pinyin(self.label, style=Style.FIRST_LETTER))
        super().save(*args, **kwargs)
    
    def natural_key(self):
        return self.name

        
class Yao_pin_ji_ben_xin_xi_biao(HsscFormModel):
    boolfield_yao_pin_bian_ma = models.CharField(max_length=255, null=True, blank=False, verbose_name='药品编码')
    boolfield_pin_yin_ma = models.CharField(max_length=255, null=True, blank=False, verbose_name='拼音码')
    boolfield_yao_pin_ming_cheng = models.CharField(max_length=255, null=True, blank=False, verbose_name='药品名称')
    boolfield_gui_ge = models.CharField(max_length=255, null=True, blank=False, verbose_name='规格')
    boolfield_chu_fang_ji_liang_dan_wei = models.CharField(max_length=255, null=True, blank=False, verbose_name='处方计量单位')
    boolfield_chang_yong_ji_liang = models.CharField(max_length=255, null=True, blank=False, verbose_name='常用剂量')
    boolfield_yong_yao_tu_jing = models.CharField(max_length=255, null=True, blank=False, verbose_name='用药途径')
    boolfield_yong_yao_pin_ci = models.CharField(max_length=255, null=True, blank=False, verbose_name='用药频次')
    boolfield_yong_yao_bei_zhu = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药备注')
    boolfield_yao_ji_lei_xing = models.ForeignKey(Yao_ji_lei_xing, related_name='yao_ji_lei_xing_for_boolfield_yao_ji_lei_xing_yao_pin_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='药剂类型')
    boolfield_yao_pin_fen_lei = models.ForeignKey(Yao_pin_fen_lei, related_name='yao_pin_fen_lei_for_boolfield_yao_pin_fen_lei_yao_pin_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='药品分类')
    boolfield_yao_pin_guan_li_shu_xing = models.ManyToManyField(Yao_pin_guan_li_shu_xing, related_name='yao_pin_guan_li_shu_xing_for_boolfield_yao_pin_guan_li_shu_xing_yao_pin_ji_ben_xin_xi_biao', blank=False, verbose_name='药品管理属性')
    boolfield_yao_pin_tong_yong_ming_cheng = models.CharField(max_length=255, null=True, blank=False, verbose_name='药品通用名称')
    boolfield_guo_jia_ji_ben_yao_pin_mu_lu_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='国家基本药品目录名称')
    boolfield_yi_bao_yao_pin_mu_lu_dui_ying_yao_pin_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='医保药品目录对应药品编码')
    boolfield_yi_bao_bao_xiao_lei_bie = models.ForeignKey(Yi_bao_bao_xiao_lei_bie, related_name='yi_bao_bao_xiao_lei_bie_for_boolfield_yi_bao_bao_xiao_lei_bie_yao_pin_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='医保报销类别')
    boolfield_shi_ying_zheng = models.ManyToManyField(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_shi_ying_zheng_yao_pin_ji_ben_xin_xi_biao', blank=False, verbose_name='适应症')
    boolfield_bu_shi_ying_zheng = models.ManyToManyField(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_bu_shi_ying_zheng_yao_pin_ji_ben_xin_xi_biao', blank=False, verbose_name='不适应症')
    boolfield_bu_liang_fan_ying = models.CharField(max_length=255, null=True, blank=False, verbose_name='不良反应')
    pym = models.CharField(max_length=255, blank=True, null=True, verbose_name="拼音码")
        

    class Meta:
        verbose_name = '药品基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
    def save(self, *args, **kwargs):
        if self.name:
            self.pym = ''.join(lazy_pinyin(self.label, style=Style.FIRST_LETTER))
        super().save(*args, **kwargs)
    
    def natural_key(self):
        return self.name

        
class Shen_qing_kong_fu_xue_tang_jian_cha_fu_wu(HsscFormModel):
    boolfield_dang_qian_pai_dui_ren_shu = models.IntegerField(null=True, blank=True, verbose_name='当前排队人数')
    boolfield_yu_ji_deng_hou_shi_jian = models.IntegerField(null=True, blank=True, verbose_name='预计等候时间')
    boolfield_fu_wu_xiang_mu_ming_cheng = models.ForeignKey(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_fu_wu_xiang_mu_ming_cheng_shen_qing_kong_fu_xue_tang_jian_cha_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='服务项目名称')
    boolfield_an_pai_que_ren = models.ForeignKey(An_pai_que_ren, related_name='an_pai_que_ren_for_boolfield_an_pai_que_ren_shen_qing_kong_fu_xue_tang_jian_cha_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='安排确认')

    class Meta:
        verbose_name = '申请空腹血糖检查服务'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Ju_min_ji_ben_xin_xi_diao_cha(HsscFormModel):
    boolfield_xing_ming = models.CharField(max_length=255, null=True, blank=False, verbose_name='姓名')
    boolfield_chu_sheng_ri_qi = models.DateField(null=True, blank=True, verbose_name='出生日期')
    boolfield_xing_bie = models.ForeignKey(Gender, related_name='gender_for_boolfield_xing_bie_ju_min_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='性别')
    boolfield_jia_ting_di_zhi = models.CharField(max_length=255, null=True, blank=True, verbose_name='家庭地址')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    boolfield_shen_fen_zheng_hao_ma = models.CharField(max_length=255, null=True, blank=False, verbose_name='身份证号码')
    boolfield_ju_min_dang_an_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='居民档案号')
    boolfield_yi_liao_ic_ka_hao = models.CharField(max_length=255, null=True, blank=True, verbose_name='医疗ic卡号')
    boolfield_min_zu = models.ForeignKey(Nationality, related_name='nationality_for_boolfield_min_zu_ju_min_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='民族')
    boolfield_hun_yin_zhuang_kuang = models.ForeignKey(Marital_status, related_name='marital_status_for_boolfield_hun_yin_zhuang_kuang_ju_min_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='婚姻状况')
    boolfield_wen_hua_cheng_du = models.ForeignKey(Education, related_name='education_for_boolfield_wen_hua_cheng_du_ju_min_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='文化程度')
    boolfield_zhi_ye_zhuang_kuang = models.ForeignKey(Occupational_status, related_name='occupational_status_for_boolfield_zhi_ye_zhuang_kuang_ju_min_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='职业状况')
    boolfield_yi_liao_fei_yong_fu_dan = models.ManyToManyField(Medical_expenses_burden, related_name='medical_expenses_burden_for_boolfield_yi_liao_fei_yong_fu_dan_ju_min_ji_ben_xin_xi_diao_cha', blank=True, verbose_name='医疗费用负担')
    boolfield_ju_zhu_lei_xing = models.ForeignKey(Type_of_residence, related_name='type_of_residence_for_boolfield_ju_zhu_lei_xing_ju_min_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='居住类型')
    boolfield_xue_xing = models.ForeignKey(Blood_type, related_name='blood_type_for_boolfield_xue_xing_ju_min_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='血型')
    boolfield_qian_yue_jia_ting_yi_sheng = models.ForeignKey(Staff, related_name='staff_for_boolfield_qian_yue_jia_ting_yi_sheng_ju_min_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='签约家庭医生')
    boolfield_jia_ting_cheng_yuan_guan_xi = models.ForeignKey(Family_relationship, related_name='family_relationship_for_boolfield_jia_ting_cheng_yuan_guan_xi_ju_min_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='家庭成员关系')
    pym = models.CharField(max_length=255, blank=True, null=True, verbose_name="拼音码")
        

    class Meta:
        verbose_name = '居民基本信息调查'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
    def save(self, *args, **kwargs):
        if self.name:
            self.pym = ''.join(lazy_pinyin(self.label, style=Style.FIRST_LETTER))
        super().save(*args, **kwargs)
    
    def natural_key(self):
        return self.name

        
class Shu_ye_zhu_she(HsscFormModel):
    boolfield_zhi_xing_qian_ming = models.CharField(max_length=255, null=True, blank=True, verbose_name='执行签名')
    boolfield_yong_yao_liao_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药疗程')
    boolfield_zhu_she_ri_qi = models.DateTimeField(null=True, blank=True, verbose_name='注射日期')
    boolfield_shang_men_fu_wu_xiang_mu = models.ManyToManyField(Icpc7_treatments, related_name='icpc7_treatments_for_boolfield_shang_men_fu_wu_xiang_mu_shu_ye_zhu_she', blank=True, verbose_name='上门服务项目')
    boolfield_jia_ting_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='家庭地址')
    boolfield_shang_men_fu_wu_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='上门服务时间')

    class Meta:
        verbose_name = '上门代注服务'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Shu_ye_zhu_she_list(models.Model):
    shu_ye_zhu_she = models.ForeignKey(Shu_ye_zhu_she, on_delete=models.CASCADE, verbose_name='上门代注服务')
    boolfield_yao_pin_ming = models.ForeignKey(Medicine, related_name='medicine_for_boolfield_yao_pin_ming_shu_ye_zhu_she', on_delete=models.CASCADE, null=True, blank=True, verbose_name='药品名')
    boolfield_yong_yao_pin_ci = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药频次')
    boolfield_gui_ge = models.CharField(max_length=255, null=True, blank=True, verbose_name='规格')
    boolfield_chang_yong_ji_liang = models.CharField(max_length=255, null=True, blank=True, verbose_name='常用剂量')

    class Meta:
        verbose_name = '上门代注服务明细'
        verbose_name_plural = verbose_name

class Qian_yue_fu_wu(HsscFormModel):
    boolfield_jia_ting_qian_yue_fu_wu_xie_yi = models.CharField(max_length=255, null=True, blank=True, verbose_name='家庭签约服务协议')
    boolfield_qian_yue_que_ren = models.ForeignKey(Qian_yue_que_ren, related_name='qian_yue_que_ren_for_boolfield_qian_yue_que_ren_qian_yue_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='签约确认')

    class Meta:
        verbose_name = '签约服务'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        

def get_T9001_boolfield_ji_bing_ming_cheng_instance():
    return Icpc5_evaluation_and_diagnoses.objects.get(iname="非胰岛素依赖型糖尿病")

class T9001(HsscFormModel):
    boolfield_ji_bing_ming_cheng = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_ji_bing_ming_cheng_T9001', on_delete=models.CASCADE, default=get_T9001_boolfield_ji_bing_ming_cheng_instance, null=True, blank=True, verbose_name='疾病名称')
    boolfield_shi_fou_hui_zhen = models.ForeignKey(Shi_fou_hui_zhen, related_name='shi_fou_hui_zhen_for_boolfield_shi_fou_hui_zhen_T9001', on_delete=models.CASCADE, null=True, blank=True, verbose_name='是否会诊')
    boolfield_shi_fou_zhuan_zhen = models.ForeignKey(Shi_fou_zhuan_zhen, related_name='shi_fou_zhuan_zhen_for_boolfield_shi_fou_zhuan_zhen_T9001', on_delete=models.CASCADE, null=True, blank=True, verbose_name='是否转诊')

    class Meta:
        verbose_name = '二型糖尿病诊断'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Tang_hua_xue_hong_dan_bai_jian_cha_biao(HsscFormModel):
    boolfield_tang_hua_xue_hong_dan_bai = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='糖化血红蛋白')

    class Meta:
        verbose_name = '糖化血红蛋白检查表'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Kong_fu_xue_tang_jian_cha(HsscFormModel):
    boolfield_kong_fu_xue_tang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='空腹血糖')

    class Meta:
        verbose_name = '门诊空腹血糖检查'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Xue_ya_jian_ce(HsscFormModel):
    boolfield_shou_suo_ya = models.IntegerField(null=True, blank=True, verbose_name='收缩压')
    boolfield_shu_zhang_ya = models.IntegerField(null=True, blank=True, verbose_name='舒张压')

    class Meta:
        verbose_name = '血压监测'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Tang_niao_bing_cha_ti(HsscFormModel):
    boolfield_yan_di = models.ForeignKey(Normality, related_name='normality_for_boolfield_yan_di_tang_niao_bing_cha_ti', on_delete=models.CASCADE, null=True, blank=True, verbose_name='眼底')
    boolfield_zuo_jiao = models.ForeignKey(Dorsal_artery_pulsation, related_name='dorsal_artery_pulsation_for_boolfield_zuo_jiao_tang_niao_bing_cha_ti', on_delete=models.CASCADE, null=True, blank=True, verbose_name='左脚')
    boolfield_you_jiao = models.ForeignKey(Dorsal_artery_pulsation, related_name='dorsal_artery_pulsation_for_boolfield_you_jiao_tang_niao_bing_cha_ti', on_delete=models.CASCADE, null=True, blank=True, verbose_name='右脚')

    class Meta:
        verbose_name = '糖尿病查体'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class A3502(HsscFormModel):
    boolfield_niao_tang = models.ForeignKey(Niao_tang, related_name='niao_tang_for_boolfield_niao_tang_A3502', on_delete=models.CASCADE, null=True, blank=True, verbose_name='尿糖')
    boolfield_dan_bai_zhi = models.ForeignKey(Dan_bai_zhi, related_name='dan_bai_zhi_for_boolfield_dan_bai_zhi_A3502', on_delete=models.CASCADE, null=True, blank=True, verbose_name='蛋白质')
    boolfield_niao_tong_ti = models.ForeignKey(Tong_ti, related_name='tong_ti_for_boolfield_niao_tong_ti_A3502', on_delete=models.CASCADE, null=True, blank=True, verbose_name='尿酮体')

    class Meta:
        verbose_name = '尿常规检查'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class A6299(HsscFormModel):
    boolfield_yi_chuan_xing_ji_bing = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_yi_chuan_xing_ji_bing_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='遗传性疾病')
    boolfield_yi_chuan_bing_shi_cheng_yuan = models.ManyToManyField(Qin_shu_guan_xi, related_name='qin_shu_guan_xi_for_boolfield_yi_chuan_bing_shi_cheng_yuan_A6299', blank=True, verbose_name='遗传病史成员')
    boolfield_guo_min_yao_wu = models.ManyToManyField(Medicine, related_name='medicine_for_boolfield_guo_min_yao_wu_A6299', blank=True, verbose_name='过敏药物')
    boolfield_jia_zu_xing_ji_bing = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_jia_zu_xing_ji_bing_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='家族性疾病')
    boolfield_jia_zu_bing_shi_cheng_yuan = models.ManyToManyField(Qin_shu_guan_xi, related_name='qin_shu_guan_xi_for_boolfield_jia_zu_bing_shi_cheng_yuan_A6299', blank=True, verbose_name='家族病史成员')
    boolfield_shou_shu_ming_cheng = models.ForeignKey(Icpc7_treatments, related_name='icpc7_treatments_for_boolfield_shou_shu_ming_cheng_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='手术名称')
    boolfield_shou_shu_ri_qi = models.DateField(null=True, blank=True, verbose_name='手术日期')
    boolfield_ge_ren_bing_shi = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_ge_ren_bing_shi_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='个人病史')
    boolfield_que_zhen_shi_jian = models.DateTimeField(null=True, blank=True, verbose_name='确诊时间')
    boolfield_wai_shang_xing_ji_bing = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_wai_shang_xing_ji_bing_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='外伤性疾病')
    boolfield_wai_shang_ri_qi = models.DateField(null=True, blank=True, verbose_name='外伤日期')
    boolfield_shu_xue_liang = models.IntegerField(null=True, blank=True, verbose_name='输血量')
    boolfield_shu_xue_ri_qi = models.DateField(null=True, blank=True, verbose_name='输血日期')
    boolfield_xing_ge_qing_xiang = models.ForeignKey(Character, related_name='character_for_boolfield_xing_ge_qing_xiang_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='性格倾向')
    boolfield_shi_mian_qing_kuang = models.ForeignKey(Shi_mian_qing_kuang, related_name='shi_mian_qing_kuang_for_boolfield_shi_mian_qing_kuang_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='失眠情况')
    boolfield_sheng_huo_gong_zuo_ya_li_qing_kuang = models.ForeignKey(Ya_li_qing_kuang, related_name='ya_li_qing_kuang_for_boolfield_sheng_huo_gong_zuo_ya_li_qing_kuang_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='生活工作压力情况')
    boolfield_mei_tian_gong_zuo_ji_gong_zuo_wang_fan_zong_shi_chang = models.TextField(max_length=255, null=True, blank=True, verbose_name='每天工作及工作往返总时长')
    boolfield_dui_mu_qian_sheng_huo_he_gong_zuo_man_yi_ma = models.ForeignKey(Satisfaction, related_name='satisfaction_for_boolfield_dui_mu_qian_sheng_huo_he_gong_zuo_man_yi_ma_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='对目前生活和工作满意吗')
    boolfield_dui_zi_ji_de_shi_ying_neng_li_man_yi_ma = models.ForeignKey(Satisfaction, related_name='satisfaction_for_boolfield_dui_zi_ji_de_shi_ying_neng_li_man_yi_ma_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='对自己的适应能力满意吗')
    boolfield_jue_de_zi_shen_jian_kang_zhuang_kuang_ru_he = models.ForeignKey(State_degree, related_name='state_degree_for_boolfield_jue_de_zi_shen_jian_kang_zhuang_kuang_ru_he_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='觉得自身健康状况如何')
    boolfield_jiao_zhi_guo_qu_yi_nian_zhuang_tai_ru_he = models.ForeignKey(Comparative_expression, related_name='comparative_expression_for_boolfield_jiao_zhi_guo_qu_yi_nian_zhuang_tai_ru_he_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='较之过去一年状态如何')
    boolfield_yun_dong_pian_hao = models.ForeignKey(Sports_preference, related_name='sports_preference_for_boolfield_yun_dong_pian_hao_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='运动偏好')
    boolfield_yun_dong_shi_chang = models.ForeignKey(Exercise_time, related_name='exercise_time_for_boolfield_yun_dong_shi_chang_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='运动时长')
    boolfield_jin_lai_you_wu_shen_ti_bu_shi_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_jin_lai_you_wu_shen_ti_bu_shi_zheng_zhuang_A6299', blank=True, verbose_name='近来有无身体不适症状')
    boolfield_ping_jun_shui_mian_shi_chang = models.CharField(max_length=255, null=True, blank=True, verbose_name='平均睡眠时长')
    boolfield_chi_xu_shi_mian_shi_jian = models.CharField(max_length=255, null=True, blank=True, verbose_name='持续失眠时间')
    boolfield_yin_jiu_pin_ci = models.ForeignKey(Frequency, related_name='frequency_for_boolfield_yin_jiu_pin_ci_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='饮酒频次')
    boolfield_xi_yan_pin_ci = models.ForeignKey(Frequency, related_name='frequency_for_boolfield_xi_yan_pin_ci_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='吸烟频次')
    boolfield_nin_dui_ju_zhu_huan_jing_man_yi_ma = models.ForeignKey(Satisfaction, related_name='satisfaction_for_boolfield_nin_dui_ju_zhu_huan_jing_man_yi_ma_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='您对居住环境满意吗')
    boolfield_nin_suo_zai_de_she_qu_jiao_tong_fang_bian_ma = models.ForeignKey(Convenience, related_name='convenience_for_boolfield_nin_suo_zai_de_she_qu_jiao_tong_fang_bian_ma_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='您所在的社区交通方便吗')

    class Meta:
        verbose_name = '居民健康信息调查'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class A6220(HsscFormModel):
    boolfield_kong_fu_xue_tang_ping_jun_zhi = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='空腹血糖平均值')
    boolfield_can_hou_2_xiao_shi_xue_tang_ping_jun_zhi = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='餐后2小时血糖平均值')
    boolfield_tang_niao_bing_kong_zhi_xiao_guo_ping_gu = models.ForeignKey(Tang_niao_bing_kong_zhi_xiao_guo_ping_gu, related_name='tang_niao_bing_kong_zhi_xiao_guo_ping_gu_for_boolfield_tang_niao_bing_kong_zhi_xiao_guo_ping_gu_A6220', on_delete=models.CASCADE, null=True, blank=False, verbose_name='糖尿病控制效果评估')
    boolfield_xue_ya_jian_ce_ping_gu = models.ForeignKey(Sui_fang_ping_gu, related_name='sui_fang_ping_gu_for_boolfield_xue_ya_jian_ce_ping_gu_A6220', on_delete=models.CASCADE, null=True, blank=True, verbose_name='血压监测评估')

    class Meta:
        verbose_name = '糖尿病监测评估'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class A6202(HsscFormModel):
    boolfield_bing_qing_bu_chong_miao_shu = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_A6202', blank=True, verbose_name='症状')

    class Meta:
        verbose_name = '院外辅助问诊'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class T6301(HsscFormModel):
    boolfield_yong_yao_pin_ci = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药频次')
    boolfield_yin_jiu_pin_ci = models.ForeignKey(Frequency, related_name='frequency_for_boolfield_yin_jiu_pin_ci_T6301', on_delete=models.CASCADE, null=True, blank=True, verbose_name='饮酒频次')
    boolfield_xi_yan_pin_ci = models.ForeignKey(Frequency, related_name='frequency_for_boolfield_xi_yan_pin_ci_T6301', on_delete=models.CASCADE, null=True, blank=True, verbose_name='吸烟频次')
    boolfield_tang_niao_bing_zheng_zhuang = models.ManyToManyField(Tang_niao_bing_zheng_zhuang, related_name='tang_niao_bing_zheng_zhuang_for_boolfield_tang_niao_bing_zheng_zhuang_T6301', blank=True, verbose_name='糖尿病症状')
    boolfield_yao_pin_ming = models.ForeignKey(Medicine, related_name='medicine_for_boolfield_yao_pin_ming_T6301', on_delete=models.CASCADE, null=True, blank=True, verbose_name='药品名')
    boolfield_zuo_jiao = models.ForeignKey(Dorsal_artery_pulsation, related_name='dorsal_artery_pulsation_for_boolfield_zuo_jiao_T6301', on_delete=models.CASCADE, null=True, blank=True, verbose_name='左脚')
    boolfield_you_jiao = models.ForeignKey(Dorsal_artery_pulsation, related_name='dorsal_artery_pulsation_for_boolfield_you_jiao_T6301', on_delete=models.CASCADE, null=True, blank=True, verbose_name='右脚')
    boolfield_yan_di = models.ForeignKey(Normality, related_name='normality_for_boolfield_yan_di_T6301', on_delete=models.CASCADE, null=True, blank=True, verbose_name='眼底')
    boolfield_shou_suo_ya = models.IntegerField(null=True, blank=True, verbose_name='收缩压')
    boolfield_shu_zhang_ya = models.IntegerField(null=True, blank=True, verbose_name='舒张压')
    boolfield_kong_fu_xue_tang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='空腹血糖')

    class Meta:
        verbose_name = '糖尿病一般随访'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class A6218(HsscFormModel):
    boolfield_bing_qing_bu_chong_miao_shu = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_A6218', blank=True, verbose_name='症状')

    class Meta:
        verbose_name = '门诊医生问诊'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class A6201(HsscFormModel):
    boolfield_bing_qing_bu_chong_miao_shu = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_A6201', blank=True, verbose_name='症状')

    class Meta:
        verbose_name = '院外咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class A6217(HsscFormModel):
    boolfield_bing_qing_bu_chong_miao_shu = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_A6217', blank=True, verbose_name='症状')

    class Meta:
        verbose_name = '院内辅助问诊'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Yao_shi_fu_wu(HsscFormModel):
    boolfield_ji_bing_ming_cheng = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_ji_bing_ming_cheng_yao_shi_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='疾病名称')
    boolfield_shi_fou_ji_xu_shi_yong = models.ForeignKey(Ji_xu_shi_yong_qing_kuang, related_name='ji_xu_shi_yong_qing_kuang_for_boolfield_shi_fou_ji_xu_shi_yong_yao_shi_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='是否继续使用')
    boolfield_yao_pin_ming = models.ForeignKey(Medicine, related_name='medicine_for_boolfield_yao_pin_ming_yao_shi_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='药品名')

    class Meta:
        verbose_name = '用药提醒服务'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Tang_niao_bing_zhuan_yong_wen_zhen(HsscFormModel):
    boolfield_bing_qing_bu_chong_miao_shu = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')
    boolfield_tang_niao_bing_zheng_zhuang = models.ManyToManyField(Tang_niao_bing_zheng_zhuang, related_name='tang_niao_bing_zheng_zhuang_for_boolfield_tang_niao_bing_zheng_zhuang_tang_niao_bing_zhuan_yong_wen_zhen', blank=True, verbose_name='糖尿病症状')

    class Meta:
        verbose_name = '糖尿病专用问诊'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class A3101(HsscFormModel):
    boolfield_ti_wen = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='体温')
    boolfield_mai_bo = models.IntegerField(null=True, blank=True, verbose_name='脉搏')
    boolfield_hu_xi_pin_lv = models.IntegerField(null=True, blank=True, verbose_name='呼吸频率')
    boolfield_shen_gao = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='身高')
    boolfield_ti_zhong = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='体重')
    boolfield_ti_zhi_zhi_shu = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='体质指数')
    boolfield_shou_suo_ya = models.IntegerField(null=True, blank=True, verbose_name='收缩压')
    boolfield_shu_zhang_ya = models.IntegerField(null=True, blank=True, verbose_name='舒张压')
    boolfield_yao_wei = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='腰围')
    boolfield_yan_bu = models.ForeignKey(Pharynx, related_name='pharynx_for_boolfield_yan_bu_A3101', on_delete=models.CASCADE, null=True, blank=True, verbose_name='咽部')
    boolfield_xia_zhi_shui_zhong = models.ForeignKey(Edema, related_name='edema_for_boolfield_xia_zhi_shui_zhong_A3101', on_delete=models.CASCADE, null=True, blank=True, verbose_name='下肢水肿')
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_A3101', blank=True, verbose_name='症状')

    class Meta:
        verbose_name = '诊前检查'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class A6502(HsscFormModel):
    boolfield_qian_dao_que_ren = models.ForeignKey(Qian_dao_que_ren, related_name='qian_dao_que_ren_for_boolfield_qian_dao_que_ren_A6502', on_delete=models.CASCADE, null=True, blank=False, verbose_name='签到确认')
    boolfield_yu_yue_shi_jian = models.DateTimeField(null=True, blank=True, verbose_name='预约时间')
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_A6502', blank=True, verbose_name='症状')

    class Meta:
        verbose_name = '门诊分诊'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class A6501(HsscFormModel):
    boolfield_yu_yue_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='预约时间')
    boolfield_ze_ren_ren = models.ForeignKey(VirtualStaff, related_name='virtualstaff_for_boolfield_ze_ren_ren_A6501', on_delete=models.CASCADE, null=True, blank=True, verbose_name='责任人')
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_A6501', blank=True, verbose_name='症状')

    class Meta:
        verbose_name = '预约挂号'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Men_zhen_chu_fang_biao(HsscFormModel):
    boolfield_ji_bing_ming_cheng = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_ji_bing_ming_cheng_men_zhen_chu_fang_biao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='疾病名称')
    boolfield_yong_yao_liao_cheng = models.CharField(max_length=255, null=True, blank=False, verbose_name='用药疗程')

    class Meta:
        verbose_name = '药品处方'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = get_profile_name(self.customer)
        return name if name else self.customer.user.username

        
class Men_zhen_chu_fang_biao_list(models.Model):
    men_zhen_chu_fang_biao = models.ForeignKey(Men_zhen_chu_fang_biao, on_delete=models.CASCADE, verbose_name='药品处方')
    boolfield_yao_pin_ming = models.ForeignKey(Medicine, related_name='medicine_for_boolfield_yao_pin_ming_men_zhen_chu_fang_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='药品名')
    boolfield_yong_yao_tu_jing = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药途径')
    boolfield_yong_yao_pin_ci = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药频次')
    boolfield_chang_yong_ji_liang = models.CharField(max_length=255, null=True, blank=True, verbose_name='常用剂量')
    boolfield_zu_bie = models.IntegerField(null=True, blank=True, verbose_name='组别')
    boolfield_yong_yao_bei_zhu = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药备注')

    class Meta:
        verbose_name = '药品处方明细'
        verbose_name_plural = verbose_name

