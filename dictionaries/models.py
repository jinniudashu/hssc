from django.db import models
from pypinyin import Style, lazy_pinyin


class DictBase(models.Model):
    label = models.CharField(max_length=255, null=True, verbose_name="名称")
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="name")
    hssc_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="hsscID")
    value = models.CharField(max_length=255, null=True, blank=True, verbose_name="值")
    icpc = models.CharField(max_length=5, null=True, blank=True, verbose_name="ICPC编码")
    pym = models.CharField(max_length=255, blank=True, null=True, verbose_name="拼音码")

    class Meta:
        abstract = True

    def __str__(self):
        return self.value

    def natural_key(self):
        return self.value

    def save(self, *args, **kwargs):
        if self.label:
            self.pym = ''.join(lazy_pinyin(self.label, style=Style.FIRST_LETTER))
            if self.name is None or self.name=='':
                self.name = "_".join(lazy_pinyin(self.label))
        super().save(*args, **kwargs)




class An_pai_que_ren(DictBase):
    class Meta:
        verbose_name = '安排确认'
        verbose_name_plural = verbose_name


class Character(DictBase):
    class Meta:
        verbose_name = '性格'
        verbose_name_plural = verbose_name


class Satisfaction(DictBase):
    class Meta:
        verbose_name = '满意度'
        verbose_name_plural = verbose_name


class Frequency(DictBase):
    class Meta:
        verbose_name = '频次'
        verbose_name_plural = verbose_name


class State_degree(DictBase):
    class Meta:
        verbose_name = '状态程度'
        verbose_name_plural = verbose_name


class Comparative_expression(DictBase):
    class Meta:
        verbose_name = '比较表达'
        verbose_name_plural = verbose_name


class Sports_preference(DictBase):
    class Meta:
        verbose_name = '运动类型'
        verbose_name_plural = verbose_name


class Exercise_time(DictBase):
    class Meta:
        verbose_name = '运动时长'
        verbose_name_plural = verbose_name


class Convenience(DictBase):
    class Meta:
        verbose_name = '便捷程度'
        verbose_name_plural = verbose_name


class Family_relationship(DictBase):
    class Meta:
        verbose_name = '家庭成员关系'
        verbose_name_plural = verbose_name


class Normality(DictBase):
    class Meta:
        verbose_name = '正常性判断'
        verbose_name_plural = verbose_name


class Dorsal_artery_pulsation(DictBase):
    class Meta:
        verbose_name = '足背动脉搏动情况'
        verbose_name_plural = verbose_name


class Pharynx(DictBase):
    class Meta:
        verbose_name = '咽部'
        verbose_name_plural = verbose_name


class Edema(DictBase):
    class Meta:
        verbose_name = '水肿情况'
        verbose_name_plural = verbose_name


class Gender(DictBase):
    class Meta:
        verbose_name = '性别'
        verbose_name_plural = verbose_name


class Nationality(DictBase):
    class Meta:
        verbose_name = '民族'
        verbose_name_plural = verbose_name


class Marital_status(DictBase):
    class Meta:
        verbose_name = '婚姻状况'
        verbose_name_plural = verbose_name


class Education(DictBase):
    class Meta:
        verbose_name = '文化程度'
        verbose_name_plural = verbose_name


class Occupational_status(DictBase):
    class Meta:
        verbose_name = '职业状况'
        verbose_name_plural = verbose_name


class Medical_expenses_burden(DictBase):
    class Meta:
        verbose_name = '医疗费用负担'
        verbose_name_plural = verbose_name


class Type_of_residence(DictBase):
    class Meta:
        verbose_name = '居住类型'
        verbose_name_plural = verbose_name


class Blood_type(DictBase):
    class Meta:
        verbose_name = '血型'
        verbose_name_plural = verbose_name


class Tang_niao_bing_zheng_zhuang(DictBase):
    class Meta:
        verbose_name = '糖尿病症状'
        verbose_name_plural = verbose_name


class Qian_dao_que_ren(DictBase):
    class Meta:
        verbose_name = '签到确认'
        verbose_name_plural = verbose_name


class Shi_mian_qing_kuang(DictBase):
    class Meta:
        verbose_name = '失眠情况'
        verbose_name_plural = verbose_name


class Ya_li_qing_kuang(DictBase):
    class Meta:
        verbose_name = '压力情况'
        verbose_name_plural = verbose_name


class Ji_xu_shi_yong_qing_kuang(DictBase):
    class Meta:
        verbose_name = '继续使用情况'
        verbose_name_plural = verbose_name


class Qian_yue_que_ren(DictBase):
    class Meta:
        verbose_name = '签约确认'
        verbose_name_plural = verbose_name


class Sui_fang_ping_gu(DictBase):
    class Meta:
        verbose_name = '血压监测评估'
        verbose_name_plural = verbose_name


class Tong_ti(DictBase):
    class Meta:
        verbose_name = '酮体'
        verbose_name_plural = verbose_name


class Niao_tang(DictBase):
    class Meta:
        verbose_name = '尿糖'
        verbose_name_plural = verbose_name


class Dan_bai_zhi(DictBase):
    class Meta:
        verbose_name = '蛋白质'
        verbose_name_plural = verbose_name


class Xin_yu_ping_ji(DictBase):
    class Meta:
        verbose_name = '信誉评级'
        verbose_name_plural = verbose_name


class Yao_pin_fen_lei(DictBase):
    class Meta:
        verbose_name = '药品分类'
        verbose_name_plural = verbose_name


class Fu_wu_jue_se(DictBase):
    class Meta:
        verbose_name = '服务角色'
        verbose_name_plural = verbose_name


class Qin_shu_guan_xi(DictBase):
    class Meta:
        verbose_name = '亲属关系'
        verbose_name_plural = verbose_name


class Tang_niao_bing_kong_zhi_xiao_guo_ping_gu(DictBase):
    class Meta:
        verbose_name = '糖尿病控制效果评估'
        verbose_name_plural = verbose_name


class Deng_hou_shi_jian(DictBase):
    class Meta:
        verbose_name = '等候时间'
        verbose_name_plural = verbose_name


class Fu_wu_xiao_guo_ping_jia(DictBase):
    class Meta:
        verbose_name = '治疗效果评价'
        verbose_name_plural = verbose_name


class Ping_fen(DictBase):
    class Meta:
        verbose_name = '评分'
        verbose_name_plural = verbose_name


class Nin_cong_he_chu_zhi_dao_wo_men(DictBase):
    class Meta:
        verbose_name = '您从何处知道我们的服务'
        verbose_name_plural = verbose_name


class Shi_fou_yuan_yi_xiang_jia_ren_peng_you_tui_jian_wo_men_de_fu_wu(DictBase):
    class Meta:
        verbose_name = '是否愿意向他人推荐我们'
        verbose_name_plural = verbose_name


class Yao_pin_guan_li_shu_xing(DictBase):
    class Meta:
        verbose_name = '药品管理属性'
        verbose_name_plural = verbose_name


class Yi_bao_bao_xiao_lei_bie(DictBase):
    class Meta:
        verbose_name = '医保报销类别'
        verbose_name_plural = verbose_name


class Yao_ji_lei_xing(DictBase):
    class Meta:
        verbose_name = '药剂类型'
        verbose_name_plural = verbose_name


class Shi_fou_zhuan_zhen(DictBase):
    class Meta:
        verbose_name = '是否转诊'
        verbose_name_plural = verbose_name


class Shi_fou_hui_zhen(DictBase):
    class Meta:
        verbose_name = '是否会诊'
        verbose_name_plural = verbose_name


class Jie_shou_tong_zhi(DictBase):
    class Meta:
        verbose_name = '通知确认'
        verbose_name_plural = verbose_name