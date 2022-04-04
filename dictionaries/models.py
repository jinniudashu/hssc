from django.db import models


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


class Hearing(DictBase):
    class Meta:
        verbose_name = '听力'
        verbose_name_plural = verbose_name


class Lips(DictBase):
    class Meta:
        verbose_name = '口唇'
        verbose_name_plural = verbose_name


class Dentition(DictBase):
    class Meta:
        verbose_name = '齿列'
        verbose_name_plural = verbose_name


class Pharynx(DictBase):
    class Meta:
        verbose_name = '咽部'
        verbose_name_plural = verbose_name


class Life_event(DictBase):
    class Meta:
        verbose_name = '生活事件'
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


class Chang_yong_zheng_zhuang(DictBase):
    class Meta:
        verbose_name = '常用症状'
        verbose_name_plural = verbose_name


class Tang_niao_bing_zheng_zhuang(DictBase):
    class Meta:
        verbose_name = '糖尿病症状'
        verbose_name_plural = verbose_name


class Xi_yan_qing_kuang(DictBase):
    class Meta:
        verbose_name = '吸烟情况'
        verbose_name_plural = verbose_name


class Yin_jiu_qing_kuang(DictBase):
    class Meta:
        verbose_name = '饮酒情况'
        verbose_name_plural = verbose_name


class Qian_dao_que_ren(DictBase):
    class Meta:
        verbose_name = '签到确认'
        verbose_name_plural = verbose_name


class Shi_mian_qing_kuang(DictBase):
    class Meta:
        verbose_name = '失眠情况'
        verbose_name_plural = verbose_name


class Da_bian_qing_kuang(DictBase):
    class Meta:
        verbose_name = '大便情况'
        verbose_name_plural = verbose_name


class Ya_li_qing_kuang(DictBase):
    class Meta:
        verbose_name = '压力情况'
        verbose_name_plural = verbose_name


class Kong_qi_wu_ran_qing_kuang(DictBase):
    class Meta:
        verbose_name = '空气污染情况'
        verbose_name_plural = verbose_name


class Zao_sheng_wu_ran_qing_kuang(DictBase):
    class Meta:
        verbose_name = '噪声污染情况'
        verbose_name_plural = verbose_name


class Shi_pin_he_yin_shui_an_quan_qing_kuang(DictBase):
    class Meta:
        verbose_name = '食品和饮水安全情况'
        verbose_name_plural = verbose_name


class Yin_shi_gui_lv_qing_kuang(DictBase):
    class Meta:
        verbose_name = '饮食规律情况'
        verbose_name_plural = verbose_name


class Qi_ta_huan_jing_wu_ran_qing_kuang(DictBase):
    class Meta:
        verbose_name = '其他环境污染情况'
        verbose_name_plural = verbose_name


class Ji_xu_shi_yong_qing_kuang(DictBase):
    class Meta:
        verbose_name = '继续使用情况'
        verbose_name_plural = verbose_name


class Qian_yue_qing_kuang(DictBase):
    class Meta:
        verbose_name = '签约情况'
        verbose_name_plural = verbose_name


class Man_bing_diao_cha(DictBase):
    class Meta:
        verbose_name = '慢病调查'
        verbose_name_plural = verbose_name


class Jian_kang_zi_wo_ping_jia(DictBase):
    class Meta:
        verbose_name = '健康自我评价'
        verbose_name_plural = verbose_name


class Qian_yue_que_ren(DictBase):
    class Meta:
        verbose_name = '签约确认'
        verbose_name_plural = verbose_name


class Sui_fang_ping_gu(DictBase):
    class Meta:
        verbose_name = '监测评估'
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