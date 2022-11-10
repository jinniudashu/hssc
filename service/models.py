from django.db import models

from icpc.models import *
from dictionaries.models import *
from core.models import HsscFormModel, HsscBaseFormModel, Staff, Institution, Service, ServicePackage, Customer, CycleUnit, Medicine
from core.hsscbase_class import HsscBase

class CustomerSchedulePackage(HsscFormModel):
    servicepackage = models.ForeignKey(ServicePackage, on_delete=models.CASCADE, verbose_name='服务包')
    
    class Meta:
        verbose_name = '安排服务包'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.servicepackage.label

class CustomerScheduleDraft(HsscBase):
    order = models.PositiveSmallIntegerField(default=100, verbose_name='顺序')
    schedule_package = models.ForeignKey(CustomerSchedulePackage, null=True, on_delete=models.CASCADE, verbose_name='服务包')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    cycle_unit = models.ForeignKey(CycleUnit, on_delete=models.CASCADE, default=1, blank=True, null=True, verbose_name='周期单位')
    cycle_frequency = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="每周期频次")
    cycle_times = models.PositiveSmallIntegerField(blank=True, null=True, default=1, verbose_name="天数")
    Default_beginning_time = [(0, '无'), (1, '当前系统时间'), (2, '首个服务开始时间'), (3, '上个服务结束时间'), (4, '客户出生日期')]
    default_beginning_time = models.PositiveSmallIntegerField(choices=Default_beginning_time, default=0, verbose_name='执行时间基准')
    base_interval = models.DurationField(blank=True, null=True, verbose_name='基准间隔', help_text='例如：3 days, 22:00:00')
    scheduled_operator = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True, verbose_name='服务人员')
    overtime = models.DurationField(blank=True, null=True, verbose_name='超期时限')
    
    class Meta:
        verbose_name = '服务项目安排'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.service.label

class CustomerScheduleList(HsscFormModel):
    plan_serial_number = models.CharField(max_length=255, null=True, blank=True, verbose_name='服务计划')
    schedule_package = models.ForeignKey(CustomerSchedulePackage, null=True, on_delete=models.CASCADE, verbose_name='服务包')
    
    class Meta:
        verbose_name = '客户服务计划'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.plan_serial_number

class CustomerSchedule(HsscFormModel):
    customer_schedule_list = models.ForeignKey(CustomerScheduleList, null=True, blank=True, on_delete=models.CASCADE, verbose_name='服务计划')
    schedule_package = models.ForeignKey(CustomerSchedulePackage, null=True, blank=True, on_delete=models.CASCADE, verbose_name='服务包')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name='服务项目')
    scheduled_time = models.DateTimeField(blank=True, null=True, verbose_name='计划执行时间')
    scheduled_operator = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True, verbose_name='服务人员')
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
class Xue_ya_jian_ce_ping_gu(HsscFormModel):
    boolfield_xue_ya_jian_ce_ping_gu = models.ForeignKey(Sui_fang_ping_gu, related_name='sui_fang_ping_gu_for_boolfield_xue_ya_jian_ce_ping_gu_xue_ya_jian_ce_ping_gu', on_delete=models.CASCADE, null=True, blank=False, verbose_name='血压监测评估')

    class Meta:
        verbose_name = '血压监测评估'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Can_hou_2_xiao_shi_xue_tang(HsscFormModel):
    boolfield_can_hou_2_xiao_shi_xue_tang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='餐后2小时血糖')

    class Meta:
        verbose_name = '餐后2小时血糖'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Ji_gou_ji_ben_xin_xi_biao(HsscBaseFormModel):
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

    class Meta:
        verbose_name = '机构基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Zhi_yuan_ji_ben_xin_xi_biao(HsscBaseFormModel):
    boolfield_shen_fen_zheng_hao_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='身份证号码')
    boolfield_zhi_ye_zi_zhi = models.CharField(max_length=255, null=True, blank=True, verbose_name='执业资质')
    boolfield_zhuan_chang = models.CharField(max_length=255, null=True, blank=True, verbose_name='专长')
    boolfield_zhi_ye_shi_jian = models.CharField(max_length=255, null=True, blank=True, verbose_name='执业时间')
    boolfield_zhi_yuan_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='职员编码')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    boolfield_xing_ming = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    boolfield_suo_shu_ji_gou = models.ForeignKey(Institution, related_name='institution_for_boolfield_suo_shu_ji_gou_zhi_yuan_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='所属机构')
    boolfield_fu_wu_jue_se = models.ManyToManyField(Fu_wu_jue_se, related_name='fu_wu_jue_se_for_boolfield_fu_wu_jue_se_zhi_yuan_ji_ben_xin_xi_biao', blank=True, verbose_name='服务角色')

    class Meta:
        verbose_name = '职员基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
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
        return self.customer.name

        
class She_bei_ji_ben_xin_xi_ji_lu(HsscBaseFormModel):
    boolfield_she_bei_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备编码')
    boolfield_sheng_chan_chang_jia = models.CharField(max_length=255, null=True, blank=True, verbose_name='生产厂家')
    boolfield_she_bei_fu_wu_dan_wei_hao_shi = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备服务单位耗时')
    boolfield_she_bei_jian_xiu_zhou_qi = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备检修周期')
    boolfield_she_bei_shi_yong_cheng_ben = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备使用成本')
    boolfield_she_bei_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备名称')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    boolfield_she_bei_shi_yong_fu_wu_gong_neng = models.ForeignKey(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_she_bei_shi_yong_fu_wu_gong_neng_she_bei_ji_ben_xin_xi_ji_lu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='设备适用服务功能')

    class Meta:
        verbose_name = '设备基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Gong_ying_shang_ji_ben_xin_xi_diao_cha(HsscBaseFormModel):
    boolfield_lian_xi_di_zhi = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系地址')
    boolfield_gong_ying_shang_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='供应商编码')
    boolfield_zhu_yao_gong_ying_chan_pin = models.CharField(max_length=255, null=True, blank=True, verbose_name='主要供应产品')
    boolfield_gong_huo_zhou_qi = models.CharField(max_length=255, null=True, blank=True, verbose_name='供货周期')
    boolfield_gong_ying_shang_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='供应商名称')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    boolfield_xin_yu_ping_ji = models.ForeignKey(Xin_yu_ping_ji, related_name='xin_yu_ping_ji_for_boolfield_xin_yu_ping_ji_gong_ying_shang_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='信誉评级')

    class Meta:
        verbose_name = '物料供应商基本信息维护'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Yao_pin_ji_ben_xin_xi_biao(HsscBaseFormModel):
    boolfield_yao_pin_tong_yong_ming = models.CharField(max_length=255, null=True, blank=True, verbose_name='药品通用名')
    boolfield_yao_pin_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='药品名称')
    boolfield_yong_yao_pin_ci = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药频次')
    boolfield_yao_pin_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='药品编码')
    boolfield_yao_pin_gui_ge = models.CharField(max_length=255, null=True, blank=True, verbose_name='药品规格')
    boolfield_chang_yong_chu_fang_liang = models.CharField(max_length=255, null=True, blank=True, verbose_name='常用处方量')
    boolfield_dui_zhao_yi_bao_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='对照医保名称')
    boolfield_dui_zhao_ji_yao_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='对照基药名称')
    boolfield_huan_suan_gui_ze = models.CharField(max_length=255, null=True, blank=True, verbose_name='换算规则')
    boolfield_yong_yao_liao_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药疗程')
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
    boolfield_dang_qian_pai_dui_ren_shu = models.IntegerField(null=True, blank=True, verbose_name='当前排队人数')
    boolfield_yu_ji_deng_hou_shi_jian = models.IntegerField(null=True, blank=True, verbose_name='预计等候时间')
    boolfield_ze_ren_ren = models.ForeignKey(Staff, related_name='staff_for_boolfield_ze_ren_ren_shen_qing_kong_fu_xue_tang_jian_cha_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='责任人')
    boolfield_fu_wu_xiang_mu_ming_cheng = models.ForeignKey(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_fu_wu_xiang_mu_ming_cheng_shen_qing_kong_fu_xue_tang_jian_cha_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='服务项目名称')
    boolfield_an_pai_que_ren = models.ForeignKey(An_pai_que_ren, related_name='an_pai_que_ren_for_boolfield_an_pai_que_ren_shen_qing_kong_fu_xue_tang_jian_cha_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='安排确认')

    class Meta:
        verbose_name = '申请空腹血糖检查服务'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Ju_min_ji_ben_xin_xi_diao_cha(HsscBaseFormModel):
    boolfield_xing_ming = models.CharField(max_length=255, null=True, blank=True, verbose_name='姓名')
    boolfield_chu_sheng_ri_qi = models.DateField(null=True, blank=True, verbose_name='出生日期')
    boolfield_xing_bie = models.ForeignKey(Gender, related_name='gender_for_boolfield_xing_bie_ju_min_ji_ben_xin_xi_diao_cha', on_delete=models.CASCADE, null=True, blank=True, verbose_name='性别')
    boolfield_jia_ting_di_zhi = models.CharField(max_length=255, null=True, blank=True, verbose_name='家庭地址')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=True, verbose_name='联系电话')
    boolfield_shen_fen_zheng_hao_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='身份证号码')
    boolfield_ju_min_dang_an_hao = models.CharField(max_length=255, null=True, blank=True, verbose_name='居民档案号')
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

    class Meta:
        verbose_name = '居民基本信息调查'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Shu_ye_zhu_she(HsscFormModel):
    boolfield_yong_yao_pin_ci = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药频次')
    boolfield_yao_pin_gui_ge = models.CharField(max_length=255, null=True, blank=True, verbose_name='药品规格')
    boolfield_chang_yong_chu_fang_liang = models.CharField(max_length=255, null=True, blank=True, verbose_name='常用处方量')
    boolfield_zhi_xing_qian_ming = models.CharField(max_length=255, null=True, blank=True, verbose_name='执行签名')
    boolfield_yong_yao_liao_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药疗程')
    boolfield_zhu_she_ri_qi = models.DateTimeField(null=True, blank=True, verbose_name='注射日期')
    boolfield_yao_pin_ming = models.ManyToManyField(Medicine, related_name='medicine_for_boolfield_yao_pin_ming_shu_ye_zhu_she', blank=True, verbose_name='药品名')

    class Meta:
        verbose_name = '输液注射'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Qian_yue_fu_wu(HsscFormModel):
    boolfield_jia_ting_qian_yue_fu_wu_xie_yi = models.CharField(max_length=255, null=True, blank=True, verbose_name='家庭签约服务协议')
    boolfield_qian_yue_que_ren = models.ForeignKey(Qian_yue_que_ren, related_name='qian_yue_que_ren_for_boolfield_qian_yue_que_ren_qian_yue_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='签约确认')
    boolfield_ze_ren_ren = models.ForeignKey(Staff, related_name='staff_for_boolfield_ze_ren_ren_qian_yue_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='责任人')

    class Meta:
        verbose_name = '签约服务'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class T9001(HsscFormModel):
    boolfield_ji_bing_ming_cheng = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_ji_bing_ming_cheng_T9001', on_delete=models.CASCADE, null=True, blank=True, verbose_name='疾病名称')
    boolfield_ke_neng_zhen_duan = models.ManyToManyField(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_ke_neng_zhen_duan_T9001', blank=True, verbose_name='可能诊断')
    boolfield_pai_chu_zhen_duan = models.ManyToManyField(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_pai_chu_zhen_duan_T9001', blank=True, verbose_name='排除诊断')

    class Meta:
        verbose_name = '非胰岛素依赖性糖尿病'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Tang_hua_xue_hong_dan_bai_jian_cha_biao(HsscFormModel):
    boolfield_tang_hua_xue_hong_dan_bai = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='糖化血红蛋白')

    class Meta:
        verbose_name = '糖化血红蛋白检查表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Kong_fu_xue_tang_jian_cha(HsscFormModel):
    boolfield_kong_fu_xue_tang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='空腹血糖')

    class Meta:
        verbose_name = '空腹血糖检查'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Xue_ya_jian_ce(HsscFormModel):
    boolfield_shou_suo_ya = models.IntegerField(null=True, blank=True, verbose_name='收缩压')
    boolfield_shu_zhang_ya = models.IntegerField(null=True, blank=True, verbose_name='舒张压')

    class Meta:
        verbose_name = '血压监测'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Tang_niao_bing_cha_ti(HsscFormModel):
    boolfield_yan_di = models.ForeignKey(Normality, related_name='normality_for_boolfield_yan_di_tang_niao_bing_cha_ti', on_delete=models.CASCADE, null=True, blank=True, verbose_name='眼底')
    boolfield_zuo_jiao = models.ForeignKey(Dorsal_artery_pulsation, related_name='dorsal_artery_pulsation_for_boolfield_zuo_jiao_tang_niao_bing_cha_ti', on_delete=models.CASCADE, null=True, blank=True, verbose_name='左脚')
    boolfield_you_jiao = models.ForeignKey(Dorsal_artery_pulsation, related_name='dorsal_artery_pulsation_for_boolfield_you_jiao_tang_niao_bing_cha_ti', on_delete=models.CASCADE, null=True, blank=True, verbose_name='右脚')

    class Meta:
        verbose_name = '糖尿病查体'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class A3502(HsscFormModel):
    boolfield_niao_tang = models.ForeignKey(Niao_tang, related_name='niao_tang_for_boolfield_niao_tang_A3502', on_delete=models.CASCADE, null=True, blank=True, verbose_name='尿糖')
    boolfield_dan_bai_zhi = models.ForeignKey(Dan_bai_zhi, related_name='dan_bai_zhi_for_boolfield_dan_bai_zhi_A3502', on_delete=models.CASCADE, null=True, blank=True, verbose_name='蛋白质')
    boolfield_niao_tong_ti = models.ForeignKey(Tong_ti, related_name='tong_ti_for_boolfield_niao_tong_ti_A3502', on_delete=models.CASCADE, null=True, blank=True, verbose_name='尿酮体')

    class Meta:
        verbose_name = '尿常规检查'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class A6299(HsscFormModel):
    boolfield_yi_chuan_xing_ji_bing = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_yi_chuan_xing_ji_bing_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='遗传性疾病')
    boolfield_yi_chuan_bing_shi_cheng_yuan = models.ManyToManyField(Qin_shu_guan_xi, related_name='qin_shu_guan_xi_for_boolfield_yi_chuan_bing_shi_cheng_yuan_A6299', blank=True, verbose_name='遗传病史成员')
    boolfield_yao_pin_ming = models.ManyToManyField(Medicine, related_name='medicine_for_boolfield_yao_pin_ming_A6299', blank=True, verbose_name='药品名')
    boolfield_jia_zu_xing_ji_bing = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_jia_zu_xing_ji_bing_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='家族性疾病')
    boolfield_jia_zu_bing_shi_cheng_yuan = models.ManyToManyField(Qin_shu_guan_xi, related_name='qin_shu_guan_xi_for_boolfield_jia_zu_bing_shi_cheng_yuan_A6299', blank=True, verbose_name='家族病史成员')
    boolfield_shou_shu_ri_qi = models.DateField(null=True, blank=True, verbose_name='手术日期')
    boolfield_shou_shu_ming_cheng = models.ForeignKey(Icpc7_treatments, related_name='icpc7_treatments_for_boolfield_shou_shu_ming_cheng_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='手术名称')
    boolfield_que_zhen_shi_jian = models.DateTimeField(null=True, blank=True, verbose_name='确诊时间')
    boolfield_ge_ren_bing_shi = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_ge_ren_bing_shi_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='个人病史')
    boolfield_wai_shang_ri_qi = models.DateField(null=True, blank=True, verbose_name='外伤日期')
    boolfield_wai_shang_xing_ji_bing = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_wai_shang_xing_ji_bing_A6299', on_delete=models.CASCADE, null=True, blank=True, verbose_name='外伤性疾病')
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
        return self.customer.name

        
class A6220(HsscFormModel):
    boolfield_kong_fu_xue_tang_ping_jun_zhi = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='空腹血糖平均值')
    boolfield_can_hou_2_xiao_shi_xue_tang_ping_jun_zhi = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='餐后2小时血糖平均值')
    boolfield_tang_niao_bing_kong_zhi_xiao_guo_ping_gu = models.ForeignKey(Tang_niao_bing_kong_zhi_xiao_guo_ping_gu, related_name='tang_niao_bing_kong_zhi_xiao_guo_ping_gu_for_boolfield_tang_niao_bing_kong_zhi_xiao_guo_ping_gu_A6220', on_delete=models.CASCADE, null=True, blank=False, verbose_name='糖尿病控制效果评估')
    boolfield_xue_ya_jian_ce_ping_gu = models.ForeignKey(Sui_fang_ping_gu, related_name='sui_fang_ping_gu_for_boolfield_xue_ya_jian_ce_ping_gu_A6220', on_delete=models.CASCADE, null=True, blank=True, verbose_name='血压监测评估')

    class Meta:
        verbose_name = '糖尿病监测评估'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class A6202(HsscFormModel):
    boolfield_bing_qing_bu_chong_miao_shu = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_A6202', blank=True, verbose_name='症状')

    class Meta:
        verbose_name = '院外辅助问诊'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class T6301(HsscFormModel):
    boolfield_yong_yao_pin_ci = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药频次')
    boolfield_yao_pin_dan_wei = models.ForeignKey(Yao_pin_dan_wei, related_name='yao_pin_dan_wei_for_boolfield_yao_pin_dan_wei_T6301', on_delete=models.CASCADE, null=True, blank=True, verbose_name='药品单位')
    boolfield_yin_jiu_pin_ci = models.ForeignKey(Frequency, related_name='frequency_for_boolfield_yin_jiu_pin_ci_T6301', on_delete=models.CASCADE, null=True, blank=True, verbose_name='饮酒频次')
    boolfield_xi_yan_pin_ci = models.ForeignKey(Frequency, related_name='frequency_for_boolfield_xi_yan_pin_ci_T6301', on_delete=models.CASCADE, null=True, blank=True, verbose_name='吸烟频次')
    boolfield_tang_niao_bing_zheng_zhuang = models.ManyToManyField(Tang_niao_bing_zheng_zhuang, related_name='tang_niao_bing_zheng_zhuang_for_boolfield_tang_niao_bing_zheng_zhuang_T6301', blank=True, verbose_name='糖尿病症状')
    boolfield_yao_pin_ming = models.ManyToManyField(Medicine, related_name='medicine_for_boolfield_yao_pin_ming_T6301', blank=True, verbose_name='药品名')
    boolfield_zuo_jiao = models.ForeignKey(Dorsal_artery_pulsation, related_name='dorsal_artery_pulsation_for_boolfield_zuo_jiao_T6301', on_delete=models.CASCADE, null=True, blank=True, verbose_name='左脚')
    boolfield_you_jiao = models.ForeignKey(Dorsal_artery_pulsation, related_name='dorsal_artery_pulsation_for_boolfield_you_jiao_T6301', on_delete=models.CASCADE, null=True, blank=True, verbose_name='右脚')
    boolfield_yan_di = models.ForeignKey(Normality, related_name='normality_for_boolfield_yan_di_T6301', on_delete=models.CASCADE, null=True, blank=True, verbose_name='眼底')
    boolfield_shou_suo_ya = models.IntegerField(null=True, blank=True, verbose_name='收缩压')
    boolfield_shu_zhang_ya = models.IntegerField(null=True, blank=True, verbose_name='舒张压')
    boolfield_kong_fu_xue_tang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='空腹血糖')

    class Meta:
        verbose_name = '糖尿病一般随访'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class T8901(HsscFormModel):
    boolfield_ji_bing_ming_cheng = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_ji_bing_ming_cheng_T8901', on_delete=models.CASCADE, null=True, blank=True, verbose_name='疾病名称')
    boolfield_ke_neng_zhen_duan = models.ManyToManyField(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_ke_neng_zhen_duan_T8901', blank=True, verbose_name='可能诊断')
    boolfield_pai_chu_zhen_duan = models.ManyToManyField(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_pai_chu_zhen_duan_T8901', blank=True, verbose_name='排除诊断')

    class Meta:
        verbose_name = '胰岛素依赖性糖尿病'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class A6218(HsscFormModel):
    boolfield_bing_qing_bu_chong_miao_shu = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_A6218', blank=True, verbose_name='症状')

    class Meta:
        verbose_name = '门诊医生问诊'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class A6201(HsscFormModel):
    boolfield_bing_qing_bu_chong_miao_shu = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_A6201', blank=True, verbose_name='症状')
    boolfield_chang_yong_zheng_zhuang = models.ManyToManyField(Chang_yong_zheng_zhuang, related_name='chang_yong_zheng_zhuang_for_boolfield_chang_yong_zheng_zhuang_A6201', blank=True, verbose_name='常用症状')

    class Meta:
        verbose_name = '院外咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class A6217(HsscFormModel):
    boolfield_bing_qing_bu_chong_miao_shu = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_A6217', blank=True, verbose_name='症状')

    class Meta:
        verbose_name = '院内辅助问诊'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Tang_niao_bing_zi_wo_jian_ce(HsscFormModel):
    boolfield_kong_fu_xue_tang = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='空腹血糖')

    class Meta:
        verbose_name = '糖尿病自我监测'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Yao_shi_fu_wu(HsscFormModel):
    boolfield_ji_bing_ming_cheng = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_ji_bing_ming_cheng_yao_shi_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='疾病名称')
    boolfield_shi_fou_ji_xu_shi_yong = models.ForeignKey(Ji_xu_shi_yong_qing_kuang, related_name='ji_xu_shi_yong_qing_kuang_for_boolfield_shi_fou_ji_xu_shi_yong_yao_shi_fu_wu', on_delete=models.CASCADE, null=True, blank=True, verbose_name='是否继续使用')
    boolfield_yao_pin_ming = models.ManyToManyField(Medicine, related_name='medicine_for_boolfield_yao_pin_ming_yao_shi_fu_wu', blank=True, verbose_name='药品名')

    class Meta:
        verbose_name = '用药提醒服务'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Tang_niao_bing_zhuan_yong_wen_zhen(HsscFormModel):
    boolfield_bing_qing_bu_chong_miao_shu = models.CharField(max_length=255, null=True, blank=True, verbose_name='病情补充描述')
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_tang_niao_bing_zhuan_yong_wen_zhen', blank=True, verbose_name='症状')
    boolfield_tang_niao_bing_zheng_zhuang = models.ManyToManyField(Tang_niao_bing_zheng_zhuang, related_name='tang_niao_bing_zheng_zhuang_for_boolfield_tang_niao_bing_zheng_zhuang_tang_niao_bing_zhuan_yong_wen_zhen', blank=True, verbose_name='糖尿病症状')

    class Meta:
        verbose_name = '糖尿病专用问诊'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
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

    class Meta:
        verbose_name = '诊前检查'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class A6502(HsscFormModel):
    boolfield_qian_dao_que_ren = models.ForeignKey(Qian_dao_que_ren, related_name='qian_dao_que_ren_for_boolfield_qian_dao_que_ren_A6502', on_delete=models.CASCADE, null=True, blank=False, verbose_name='签到确认')
    boolfield_yu_yue_shi_jian = models.DateTimeField(null=True, blank=True, verbose_name='预约时间')
    boolfield_ze_ren_ren = models.ForeignKey(Staff, related_name='staff_for_boolfield_ze_ren_ren_A6502', on_delete=models.CASCADE, null=True, blank=True, verbose_name='责任人')

    class Meta:
        verbose_name = '门诊分诊'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class A6501(HsscFormModel):
    boolfield_yu_yue_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='预约时间')
    boolfield_ze_ren_ren = models.ForeignKey(Staff, related_name='staff_for_boolfield_ze_ren_ren_A6501', on_delete=models.CASCADE, null=True, blank=True, verbose_name='责任人')

    class Meta:
        verbose_name = '代人预约挂号'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
class Men_zhen_chu_fang_biao(HsscFormModel):
    boolfield_yong_yao_pin_ci = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药频次')
    boolfield_chang_yong_chu_fang_liang = models.CharField(max_length=255, null=True, blank=True, verbose_name='常用处方量')
    boolfield_yong_yao_liao_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='用药疗程')
    boolfield_yong_yao_tu_jing = models.ForeignKey(Yong_yao_tu_jing, related_name='yong_yao_tu_jing_for_boolfield_yong_yao_tu_jing_men_zhen_chu_fang_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='用药途径')
    boolfield_yao_pin_ming = models.ManyToManyField(Medicine, related_name='medicine_for_boolfield_yao_pin_ming_men_zhen_chu_fang_biao', blank=True, verbose_name='药品名')

    class Meta:
        verbose_name = '药物干预'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.customer.name

        
