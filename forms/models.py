from django.db import models
from django.shortcuts import reverse
import json

from icpc.models import *
from dictionaries.models import *
from core.models import HsscFormModel, Staff


class Li_pei_dui_zhang_dan(HsscFormModel):
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
    boolfield_zheng_jian_lei_xing = models.ForeignKey(Zheng_jian_lei_xing, related_name='zheng_jian_lei_xing_for_boolfield_zheng_jian_lei_xing_li_pei_dui_zhang_dan', on_delete=models.CASCADE, null=True, blank=False, verbose_name='证件类型')
    boolfield_bei_bao_xian_ren_zheng_jian_hao_ma = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保险人证件号码')
    boolfield_xing_bie = models.ForeignKey(Gender, related_name='gender_for_boolfield_xing_bie_li_pei_dui_zhang_dan', on_delete=models.CASCADE, null=True, blank=False, verbose_name='性别')
    boolfield_nian_ling = models.CharField(max_length=255, null=True, blank=False, verbose_name='年龄')
    boolfield_chu_sheng_ri_qi = models.DateField(null=True, blank=False, verbose_name='出生日期')
    boolfield_gui_shu_cheng_shi = models.CharField(max_length=255, null=True, blank=False, verbose_name='归属城市')
    boolfield_yi_yuan_xin_xi = models.CharField(max_length=255, null=True, blank=False, verbose_name='医院信息')
    boolfield_ji_bing_xin_xi = models.CharField(max_length=255, null=True, blank=False, verbose_name='疾病信息')
    boolfield_li_pei_jin_e = models.CharField(max_length=255, null=True, blank=False, verbose_name='理赔金额')
    boolfield_li_pei_fang_shi = models.CharField(max_length=255, null=True, blank=False, verbose_name='理赔方式')
    boolfield_bei_zhu = models.CharField(max_length=255, null=True, blank=False, verbose_name='备注')
    boolfield_bei_bao_ren_zheng_jian_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='被保人证件附件')
    class Meta:
        verbose_name = '理赔对账单'
        verbose_name_plural = verbose_name
        

class Bang_ding_que_ren_biao(HsscFormModel):
    boolfield_shi_fou_bang_ding_bei_bao_ren_xin_xi = models.ForeignKey(Xin_xi_que_ren, related_name='xin_xi_que_ren_for_boolfield_shi_fou_bang_ding_bei_bao_ren_xin_xi_bang_ding_que_ren_biao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='是否绑定被保人信息')
    boolfield_ju_jue_bang_ding_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='拒绝绑定原因')
    class Meta:
        verbose_name = '绑定确认表'
        verbose_name_plural = verbose_name
        

class He_bao_dan(HsscFormModel):
    boolfield_shi_fou_shen_he_tong_guo = models.ForeignKey(Shi_fou_shen_he_tong_guo, related_name='shi_fou_shen_he_tong_guo_for_boolfield_shi_fou_shen_he_tong_guo_he_bao_dan', on_delete=models.CASCADE, null=True, blank=False, verbose_name='是否审核通过')
    boolfield_li_pei_shen_qing_tui_hui_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='理赔申请退回原因')
    class Meta:
        verbose_name = '保险审核单'
        verbose_name_plural = verbose_name
        

class Yu_yue_tong_zhi_dan(HsscFormModel):
    boolfield_ji_gou_ming_cheng = models.CharField(max_length=255, null=True, blank=False, verbose_name='机构名称')
    boolfield_yu_yue_xu_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='预约序号')
    boolfield_ji_gou_lian_xi_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='机构联系地址')
    boolfield_ji_gou_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=False, verbose_name='机构联系电话')
    boolfield_jiu_zhen_yi_sheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='就诊医生')
    class Meta:
        verbose_name = '预约通知单'
        verbose_name_plural = verbose_name
        

class Zhen_jian_sui_fang_biao(HsscFormModel):
    boolfield_deng_hou_qing_kuang = models.ForeignKey(Deng_hou_shi_jian, related_name='deng_hou_shi_jian_for_boolfield_deng_hou_qing_kuang_zhen_jian_sui_fang_biao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='等候情况')
    boolfield_jie_dai_fu_wu = models.ForeignKey(Jie_dai_fu_wu, related_name='jie_dai_fu_wu_for_boolfield_jie_dai_fu_wu_zhen_jian_sui_fang_biao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='接待服务')
    boolfield_zhi_liao_jian_gou_tong_qing_kuang = models.ForeignKey(Gou_tong_qing_kuang, related_name='gou_tong_qing_kuang_for_boolfield_zhi_liao_jian_gou_tong_qing_kuang_zhen_jian_sui_fang_biao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='治疗间沟通情况')
    boolfield_zhi_liao_gan_shou_he_xiao_guo_ping_jia = models.ForeignKey(Fu_wu_xiao_guo_ping_jia, related_name='fu_wu_xiao_guo_ping_jia_for_boolfield_zhi_liao_gan_shou_he_xiao_guo_ping_jia_zhen_jian_sui_fang_biao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='治疗感受和效果评价')
    boolfield_nin_de_dan_xin_he_gu_lv = models.CharField(max_length=255, null=True, blank=True, verbose_name='您的担心和顾虑')
    boolfield_cun_zai_de_wen_ti = models.CharField(max_length=255, null=True, blank=True, verbose_name='存在的问题')
    boolfield_nin_xiang_yao_de_bang_zhu = models.CharField(max_length=255, null=True, blank=True, verbose_name='您想要的帮助')
    boolfield_qi_ta_xu_qiu = models.CharField(max_length=255, null=True, blank=True, verbose_name='其他需求')
    class Meta:
        verbose_name = '诊间随访表'
        verbose_name_plural = verbose_name
        

class A6401(HsscFormModel):
    boolfield_yu_yue_shi_jian = models.DateTimeField(null=True, blank=False, verbose_name='预约时间')
    boolfield_jiu_zhen_wen_ti = models.CharField(max_length=255, null=True, blank=False, verbose_name='就诊问题')
    boolfield_jiu_zhen_ji_gou_ze_ren_ren = models.ForeignKey(Jiu_zhen_ji_gou_fu_ze_ren, related_name='jiu_zhen_ji_gou_fu_ze_ren_for_boolfield_jiu_zhen_ji_gou_ze_ren_ren_A6401', on_delete=models.CASCADE, null=True, blank=True, verbose_name='就诊机构责任人')
    boolfield_shi_yong_fu_wu_chan_pin = models.ManyToManyField(Bao_xian_chan_pin, related_name='bao_xian_chan_pin_for_boolfield_shi_yong_fu_wu_chan_pin_A6401', blank=True, verbose_name='使用服务产品')
    boolfield_fu_jia_fu_wu_yao_qiu = models.CharField(max_length=255, null=True, blank=True, verbose_name='附加服务要求')
    class Meta:
        verbose_name = '预约单'
        verbose_name_plural = verbose_name
        

class A6203(HsscFormModel):
    boolfield_xu_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='序号')
    boolfield_bao_dan_hao = models.CharField(max_length=255, null=True, blank=False, verbose_name='保单号')
    boolfield_zheng_jian_lei_xing = models.ForeignKey(Zheng_jian_lei_xing, related_name='zheng_jian_lei_xing_for_boolfield_zheng_jian_lei_xing_A6203', on_delete=models.CASCADE, null=True, blank=False, verbose_name='证件类型')
    boolfield_zheng_jian_hao_ma = models.CharField(max_length=255, null=True, blank=False, verbose_name='证件号码')
    boolfield_bei_bao_ren_xing_ming = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人姓名')
    boolfield_bei_bao_ren_xing_bie = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人性别')
    boolfield_chu_sheng_ri_qi = models.DateField(null=True, blank=False, verbose_name='出生日期')
    boolfield_bao_xian_ze_ren = models.CharField(max_length=255, null=True, blank=False, verbose_name='保险责任')
    boolfield_bao_xian_you_xiao_qi = models.DateField(null=True, blank=False, verbose_name='保险有效期')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=False, verbose_name='联系电话')
    boolfield_chang_zhu_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='常住地址')
    class Meta:
        verbose_name = '个人基本信息表'
        verbose_name_plural = verbose_name
        

class Zhen_hou_hui_fang_dan(HsscFormModel):
    boolfield_zhi_liao_gan_shou_he_xiao_guo_ping_jia = models.ForeignKey(Fu_wu_xiao_guo_ping_jia, related_name='fu_wu_xiao_guo_ping_jia_for_boolfield_zhi_liao_gan_shou_he_xiao_guo_ping_jia_zhen_hou_hui_fang_dan', on_delete=models.CASCADE, null=True, blank=False, verbose_name='治疗感受和效果评价')
    boolfield_deng_hou_qing_kuang = models.ForeignKey(Deng_hou_shi_jian, related_name='deng_hou_shi_jian_for_boolfield_deng_hou_qing_kuang_zhen_hou_hui_fang_dan', on_delete=models.CASCADE, null=True, blank=False, verbose_name='等候情况')
    boolfield_cun_zai_de_wen_ti = models.CharField(max_length=255, null=True, blank=True, verbose_name='存在的问题')
    boolfield_you_dai_gai_jin_de_fu_wu = models.CharField(max_length=255, null=True, blank=True, verbose_name='有待改进的服务')
    boolfield_nin_de_dan_xin_he_gu_lv = models.CharField(max_length=255, null=True, blank=True, verbose_name='您的担心和顾虑')
    boolfield_nin_hai_xu_yao_de_fu_wu = models.CharField(max_length=255, null=True, blank=True, verbose_name='您还需要的服务')
    boolfield_nin_cong_he_chu_zhi_dao_wo_men_de_fu_wu = models.ForeignKey(Nin_cong_he_chu_zhi_dao_wo_men, related_name='nin_cong_he_chu_zhi_dao_wo_men_for_boolfield_nin_cong_he_chu_zhi_dao_wo_men_de_fu_wu_zhen_hou_hui_fang_dan', on_delete=models.CASCADE, null=True, blank=True, verbose_name='您从何处知道我们的服务')
    boolfield_nin_shi_fou_yuan_yi_xiang_ta_ren_tui_jian_wo_men = models.ForeignKey(Shi_fou_yuan_yi_xiang_jia_ren_peng_you_tui_jian_wo_men_de_fu_wu, related_name='shi_fou_yuan_yi_xiang_jia_ren_peng_you_tui_jian_wo_men_de_fu_wu_for_boolfield_nin_shi_fou_yuan_yi_xiang_ta_ren_tui_jian_wo_men_zhen_hou_hui_fang_dan', on_delete=models.CASCADE, null=True, blank=True, verbose_name='您是否愿意向他人推荐我们')
    class Meta:
        verbose_name = '诊后回访单'
        verbose_name_plural = verbose_name
        

class Tou_su_jian_yi_biao(HsscFormModel):
    boolfield_tou_su_jian_yi = models.TextField(max_length=255, null=True, blank=True, verbose_name='投诉建议')
    class Meta:
        verbose_name = '投诉建议表'
        verbose_name_plural = verbose_name
        

class Yi_an_pai_fu_wu_cha_xun_biao(HsscFormModel):
    boolfield_fu_wu_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='服务名称')
    boolfield_fu_wu_shi_jian = models.DateTimeField(null=True, blank=True, verbose_name='服务时间')
    boolfield_jiu_zhen_ji_gou_ze_ren_ren = models.ForeignKey(Jiu_zhen_ji_gou_fu_ze_ren, related_name='jiu_zhen_ji_gou_fu_ze_ren_for_boolfield_jiu_zhen_ji_gou_ze_ren_ren_yi_an_pai_fu_wu_cha_xun_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='就诊机构责任人')
    class Meta:
        verbose_name = '服务安排查询表'
        verbose_name_plural = verbose_name
        

class Kou_qiang_jian_cha_ji_zhen_duan(HsscFormModel):
    boolfield_kou_qiang_jian_cha_ji_zhen_duan = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='口腔检查及诊断')
    boolfield_shi_fou_an_pai_zhi_liao_ji_hua = models.ForeignKey(Shi_fou_an_pai_zhi_liao_ji_hua, related_name='shi_fou_an_pai_zhi_liao_ji_hua_for_boolfield_shi_fou_an_pai_zhi_liao_ji_hua_kou_qiang_jian_cha_ji_zhen_duan', on_delete=models.CASCADE, null=True, blank=False, verbose_name='是否安排治疗计划')
    class Meta:
        verbose_name = '口腔检查及诊断'
        verbose_name_plural = verbose_name
        

class Tui_bao_shen_qing_biao(HsscFormModel):
    boolfield_shen_qing_ren_xing_ming = models.CharField(max_length=255, null=True, blank=False, verbose_name='申请人姓名')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=False, verbose_name='联系电话')
    boolfield_bei_bao_ren_xing_ming = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保人姓名')
    boolfield_bei_bao_xian_ren_zheng_jian_hao_ma = models.CharField(max_length=255, null=True, blank=False, verbose_name='被保险人证件号码')
    boolfield_shi_yong_fu_wu_chan_pin = models.ManyToManyField(Bao_xian_chan_pin, related_name='bao_xian_chan_pin_for_boolfield_shi_yong_fu_wu_chan_pin_tui_bao_shen_qing_biao', blank=False, verbose_name='使用服务产品')
    boolfield_shen_qing_tui_bao_yuan_yin = models.TextField(max_length=255, null=True, blank=False, verbose_name='申请退保原因')
    boolfield_shen_fen_zheng_jian_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='身份证件附件')
    boolfield_kou_qiang_jian_cha_ji_zhen_duan = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='口腔检查及诊断')
    class Meta:
        verbose_name = '退保申请表'
        verbose_name_plural = verbose_name
        

class Tui_bao_que_ren_dan(HsscFormModel):
    boolfield_ke_hu_tui_bao_shen_qing_shi_fou_tong_guo = models.ForeignKey(Qian_shu_que_ren, related_name='qian_shu_que_ren_for_boolfield_ke_hu_tui_bao_shen_qing_shi_fou_tong_guo_tui_bao_que_ren_dan', on_delete=models.CASCADE, null=True, blank=False, verbose_name='客户退保申请是否通过')
    class Meta:
        verbose_name = '退保确认单'
        verbose_name_plural = verbose_name
        

class Ji_gou_ji_ben_xin_xi_biao(HsscFormModel):
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
        verbose_name = '机构基本信息表'
        verbose_name_plural = verbose_name
        

class Zhi_yuan_ji_ben_xin_xi_biao(HsscFormModel):
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
        verbose_name = '职员基本信息表'
        verbose_name_plural = verbose_name
        

class She_bei_ji_ben_xin_xi_biao(HsscFormModel):
    boolfield_she_bei_bian_ma = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备编码')
    boolfield_sheng_chan_chang_jia = models.CharField(max_length=255, null=True, blank=True, verbose_name='生产厂家')
    boolfield_she_bei_fu_wu_dan_wei_hao_shi = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备服务单位耗时')
    boolfield_she_bei_jian_xiu_zhou_qi = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备检修周期')
    boolfield_she_bei_shi_yong_cheng_ben = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备使用成本')
    boolfield_she_bei_ming_cheng = models.CharField(max_length=255, null=True, blank=True, verbose_name='设备名称')
    boolfield_ji_gou_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=True, verbose_name='机构联系电话')
    boolfield_she_bei_shi_yong_fu_wu_gong_neng = models.ForeignKey(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_she_bei_shi_yong_fu_wu_gong_neng_she_bei_ji_ben_xin_xi_biao', on_delete=models.CASCADE, null=True, blank=True, verbose_name='设备适用服务功能')
    class Meta:
        verbose_name = '设备基本信息表'
        verbose_name_plural = verbose_name
        

class Zhi_liao_fei_yong_hui_zong_dan(HsscFormModel):
    boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu = models.ManyToManyField(Fu_wu_xiang_mu, related_name='fu_wu_xiang_mu_for_boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu_zhi_liao_fei_yong_hui_zong_dan', blank=False, verbose_name='保单内服务收费项目')
    boolfield_bao_dan_nei_fu_wu_fei_yong = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='保单内服务费用')
    boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu = models.ManyToManyField(Fu_wu_xiang_mu, related_name='fu_wu_xiang_mu_for_boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu_zhi_liao_fei_yong_hui_zong_dan', blank=False, verbose_name='保单外服务收费项目')
    boolfield_bao_dan_wai_fu_wu_fei_yong = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='保单外服务费用')
    boolfield_fei_yong_he_ji = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='费用合计')
    boolfield_hui_zong_fei_yong_qing_dan_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='汇总费用清单附件')
    class Meta:
        verbose_name = '治疗费用汇总单'
        verbose_name_plural = verbose_name
        

class Man_yi_du_diao_cha_biao(HsscFormModel):
    boolfield_yi_liao_fu_wu_ji_neng_xiang_mu_ping_fen = models.ForeignKey(Ping_fen, related_name='ping_fen_for_boolfield_yi_liao_fu_wu_ji_neng_xiang_mu_ping_fen_man_yi_du_diao_cha_biao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='医疗服务技能项目评分')
    boolfield_ping_tai_fu_wu_xiang_mu_ping_fen = models.ForeignKey(Ping_fen, related_name='ping_fen_for_boolfield_ping_tai_fu_wu_xiang_mu_ping_fen_man_yi_du_diao_cha_biao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='平台服务项目评分')
    boolfield_fu_wu_liu_cheng_ping_fen = models.ForeignKey(Ping_fen, related_name='ping_fen_for_boolfield_fu_wu_liu_cheng_ping_fen_man_yi_du_diao_cha_biao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='服务流程评分')
    boolfield_xi_wang_zeng_jia_de_fu_wu_xiang_mu = models.CharField(max_length=255, null=True, blank=True, verbose_name='希望增加的服务项目')
    boolfield_fu_wu_xiao_lv_ping_fen = models.ForeignKey(Ping_fen, related_name='ping_fen_for_boolfield_fu_wu_xiao_lv_ping_fen_man_yi_du_diao_cha_biao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='服务效率评分')
    boolfield_you_dai_gai_jin_de_fu_wu = models.CharField(max_length=255, null=True, blank=True, verbose_name='有待改进的服务')
    class Meta:
        verbose_name = '满意度调查表'
        verbose_name_plural = verbose_name
        

class Qian_shu_que_ren_dan(HsscFormModel):
    boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu = models.ForeignKey(Qian_shu_que_ren, related_name='qian_shu_que_ren_for_boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu_qian_shu_que_ren_dan', on_delete=models.CASCADE, null=True, blank=False, verbose_name='人身险理赔申请书签署')
    boolfield_ren_shen_xian_li_pei_shen_qing_shu_tui_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='人身险理赔申请书退单原因')
    class Meta:
        verbose_name = '人身险理赔申请书审核单'
        verbose_name_plural = verbose_name
        

class Men_zhen_ji_lu_dan_shen_he_dan(HsscFormModel):
    boolfield_men_zhen_ji_lu_dan_tui_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='门诊记录单退单原因')
    boolfield_li_pei_men_zhen_ji_lu_qian_shu = models.ForeignKey(Qian_shu_que_ren, related_name='qian_shu_que_ren_for_boolfield_li_pei_men_zhen_ji_lu_qian_shu_men_zhen_ji_lu_dan_shen_he_dan', on_delete=models.CASCADE, null=True, blank=False, verbose_name='理赔门诊记录签署')
    class Meta:
        verbose_name = '门诊记录单审核单'
        verbose_name_plural = verbose_name
        

class Li_pei_dui_zhang_dan_shen_he_dan(HsscFormModel):
    boolfield_li_pei_dui_zhang_dan_qian_shu = models.ForeignKey(Qian_shu_que_ren, related_name='qian_shu_que_ren_for_boolfield_li_pei_dui_zhang_dan_qian_shu_li_pei_dui_zhang_dan_shen_he_dan', on_delete=models.CASCADE, null=True, blank=False, verbose_name='理赔对账单签署')
    boolfield_li_pei_dui_zhang_dan_tui_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='理赔对账单退单原因')
    class Meta:
        verbose_name = '理赔对账单审核单'
        verbose_name_plural = verbose_name
        

class Zhi_liao_ji_hua_biao(HsscFormModel):
    boolfield_zhi_liao_ji_hua = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='治疗计划')
    class Meta:
        verbose_name = '治疗计划表'
        verbose_name_plural = verbose_name
        

class Li_pei_fei_yong_hui_zong_dan_shen_he(HsscFormModel):
    boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu = models.ForeignKey(Qian_shu_que_ren, related_name='qian_shu_que_ren_for_boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu_li_pei_fei_yong_hui_zong_dan_shen_he', on_delete=models.CASCADE, null=True, blank=False, verbose_name='理赔费用汇总单签署')
    boolfield_li_pei_fei_yong_hui_zong_dan_tui_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='理赔费用汇总单退单原因')
    class Meta:
        verbose_name = '理赔费用汇总单审核'
        verbose_name_plural = verbose_name
        

class A6502(HsscFormModel):
    boolfield_jie_dan_que_ren = models.ForeignKey(Jie_dan_que_ren, related_name='jie_dan_que_ren_for_boolfield_jie_dan_que_ren_A6502', on_delete=models.CASCADE, null=True, blank=False, verbose_name='接单确认')
    boolfield_ju_jue_jie_dan_yuan_yin = models.CharField(max_length=255, null=True, blank=True, verbose_name='拒绝接单原因')
    class Meta:
        verbose_name = '接单确认表'
        verbose_name_plural = verbose_name
        

class Ren_shen_xian_li_pei_shen_qing_shu(HsscFormModel):
    boolfield_shen_qing_ren_xing_ming = models.CharField(max_length=255, null=True, blank=False, verbose_name='申请人姓名')
    boolfield_xing_bie = models.ForeignKey(Gender, related_name='gender_for_boolfield_xing_bie_ren_shen_xian_li_pei_shen_qing_shu', on_delete=models.CASCADE, null=True, blank=False, verbose_name='性别')
    boolfield_yu_chu_xian_ren_guan_xi = models.ForeignKey(Yu_chu_xian_ren_guan_xi, related_name='yu_chu_xian_ren_guan_xi_for_boolfield_yu_chu_xian_ren_guan_xi_ren_shen_xian_li_pei_shen_qing_shu', on_delete=models.CASCADE, null=True, blank=False, verbose_name='与出险人关系')
    boolfield_zheng_jian_lei_xing = models.ForeignKey(Zheng_jian_lei_xing, related_name='zheng_jian_lei_xing_for_boolfield_zheng_jian_lei_xing_ren_shen_xian_li_pei_shen_qing_shu', on_delete=models.CASCADE, null=True, blank=False, verbose_name='证件类型')
    boolfield_zheng_jian_hao_ma = models.CharField(max_length=255, null=True, blank=False, verbose_name='证件号码')
    boolfield_zheng_jian_you_xiao_qi = models.CharField(max_length=255, null=True, blank=False, verbose_name='证件有效期')
    boolfield_guo_ji_di_qu = models.CharField(max_length=255, null=True, blank=False, verbose_name='国籍地区')
    boolfield_hang_ye = models.CharField(max_length=255, null=True, blank=False, verbose_name='行业')
    boolfield_zhi_ye = models.CharField(max_length=255, null=True, blank=False, verbose_name='职业')
    boolfield_lian_xi_dian_hua = models.CharField(max_length=255, null=True, blank=False, verbose_name='联系电话')
    boolfield_chang_zhu_di_zhi = models.CharField(max_length=255, null=True, blank=False, verbose_name='常住地址')
    boolfield_shen_qing_ren_zheng_jian_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='申请人证件附件')
    class Meta:
        verbose_name = '人身险理赔申请书'
        verbose_name_plural = verbose_name
        

class Fen_zhen_que_ren_biao(HsscFormModel):
    boolfield_dao_da_que_ren = models.ForeignKey(Qian_dao_que_ren, related_name='qian_dao_que_ren_for_boolfield_dao_da_que_ren_fen_zhen_que_ren_biao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='到达确认')
    class Meta:
        verbose_name = '到店确认表'
        verbose_name_plural = verbose_name
        

class Shou_ci_dao_dian_que_ren_biao(HsscFormModel):
    boolfield_dao_da_que_ren = models.ForeignKey(Qian_dao_que_ren, related_name='qian_dao_que_ren_for_boolfield_dao_da_que_ren_shou_ci_dao_dian_que_ren_biao', on_delete=models.CASCADE, null=True, blank=False, verbose_name='到达确认')
    boolfield_shen_fen_xin_xi_yan_zheng = models.CharField(max_length=255, null=True, blank=False, verbose_name='身份信息验证')
    class Meta:
        verbose_name = '首次到店确认表'
        verbose_name_plural = verbose_name
        

class Men_zhen_fu_wu_ji_lu_2(HsscFormModel):
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_men_zhen_fu_wu_ji_lu_2', blank=True, verbose_name='症状')
    boolfield_jian_cha_xiang_mu = models.ManyToManyField(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_jian_cha_xiang_mu_men_zhen_fu_wu_ji_lu_2', blank=True, verbose_name='检查项目')
    boolfield_zhen_duan = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_zhen_duan_men_zhen_fu_wu_ji_lu_2', on_delete=models.CASCADE, null=True, blank=False, verbose_name='诊断')
    boolfield_zhi_liao_xiang_mu = models.ManyToManyField(Icpc7_treatments, related_name='icpc7_treatments_for_boolfield_zhi_liao_xiang_mu_men_zhen_fu_wu_ji_lu_2', blank=False, verbose_name='治疗项目')
    boolfield_qi_ta_jian_kang_gan_yu_fu_wu = models.ManyToManyField(Icpc8_other_health_interventions, related_name='icpc8_other_health_interventions_for_boolfield_qi_ta_jian_kang_gan_yu_fu_wu_men_zhen_fu_wu_ji_lu_2', blank=True, verbose_name='其他健康干预服务')
    boolfield_fei_yong_he_ji = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='费用合计')
    boolfield_men_zhen_bing_li_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='门诊病历附件')
    class Meta:
        verbose_name = '门诊复诊病例'
        verbose_name_plural = verbose_name
        

class Men_zhen_fu_wu_ji_lu_dan(HsscFormModel):
    boolfield_zheng_zhuang = models.ManyToManyField(Icpc3_symptoms_and_problems, related_name='icpc3_symptoms_and_problems_for_boolfield_zheng_zhuang_men_zhen_fu_wu_ji_lu_dan', blank=True, verbose_name='症状')
    boolfield_jian_cha_xiang_mu = models.ManyToManyField(Icpc4_physical_examination_and_tests, related_name='icpc4_physical_examination_and_tests_for_boolfield_jian_cha_xiang_mu_men_zhen_fu_wu_ji_lu_dan', blank=True, verbose_name='检查项目')
    boolfield_zhen_duan = models.ForeignKey(Icpc5_evaluation_and_diagnoses, related_name='icpc5_evaluation_and_diagnoses_for_boolfield_zhen_duan_men_zhen_fu_wu_ji_lu_dan', on_delete=models.CASCADE, null=True, blank=False, verbose_name='诊断')
    boolfield_zhi_liao_xiang_mu = models.ManyToManyField(Icpc7_treatments, related_name='icpc7_treatments_for_boolfield_zhi_liao_xiang_mu_men_zhen_fu_wu_ji_lu_dan', blank=False, verbose_name='治疗项目')
    boolfield_qi_ta_jian_kang_gan_yu_fu_wu = models.ManyToManyField(Icpc8_other_health_interventions, related_name='icpc8_other_health_interventions_for_boolfield_qi_ta_jian_kang_gan_yu_fu_wu_men_zhen_fu_wu_ji_lu_dan', blank=True, verbose_name='其他健康干预服务')
    boolfield_fei_yong_he_ji = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='费用合计')
    boolfield_men_zhen_bing_li_fu_jian = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='门诊病历附件')
    class Meta:
        verbose_name = '门诊病例'
        verbose_name_plural = verbose_name
        

