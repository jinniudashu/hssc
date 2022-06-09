from django.db import models
from django.forms.models import model_to_dict
from datetime import timedelta
import uuid
import re
from pypinyin import Style, lazy_pinyin

# 自定义管理器：设计数据备份、恢复
class HsscBackupManager(models.Manager):
    def backup_data(self):
        backup_data = []
        for item in self.all():
            item_dict = model_to_dict(item)

            # 遍历模型非多对多字段，如果是外键，则用外键的hssc_id替换外键id
            for field in self.model._meta.fields:
                # if item_dict[field.name] or field.__class__.__name__ == 'DurationField':  # 如果字段不为空或字段为DurationField类型，进行检查替换
                if item_dict[field.name]:  # 如果字段不为空或字段为DurationField类型，进行检查替换
                    if field.name in ['name_icpc', 'icpc']:  # 如果是ICPC外键，获取icpc_code
                        _object = field.related_model.objects.get(id=item_dict[field.name])
                        item_dict[field.name] = _object.icpc_code
                    else:
                        if (field.one_to_one or field.many_to_one):  # 一对一、多对一字段, 获取外键的hssc_id
                            _object = field.related_model.objects.get(id=item_dict[field.name])
                            item_dict[field.name] = _object.hssc_id
                        elif field.__class__.__name__ == 'DurationField':  # duration字段
                            item_dict[field.name] = str(item_dict[field.name])


            # 遍历模型多对多字段，用hssc_id或icpc_code替换外键id
            for field in self.model._meta.many_to_many:
                if item_dict[field.name]:  # 如果字段不为空，进行检查替换
                    # 先获取多对多字段对象的id List
                    _ids = []
                    for _field in item_dict[field.name]:
                        _ids.append(_field.id)
                    ids = []
                    for _object in field.related_model.objects.filter(id__in=_ids):
                        # 如果是ICPC外键，获取icpc_code，否则获取hssc_id
                        if field.name in ['name_icpc', 'icpc']:
                            ids.append(_object.icpc_code)
                        else:
                            ids.append(_object.hssc_id)
                    item_dict[field.name] = ids

            item_dict.pop('id')  # 删除id字段
            backup_data.append(item_dict)
        return backup_data

    def restore_data(self, data):
        if data is None or len(data) == 0:
            return 'No data to restore'

        print('开始恢复：', self.model.__name__)
        self.all().delete()
        for item_dict in data:
            item = {}
            # 遍历模型非多对多字段，如果是外键，则用外键的hssc_id找回关联对象
            for field in self.model._meta.fields:
                if item_dict.get(field.name) is not None:  # 如果字段不为空，进行检查替换                    
                    if field.name in ['name_icpc', 'icpc']:  # 如果是ICPC外键，用icpc_code获取对象
                        _object = field.related_model.objects.get(icpc_code=item_dict[field.name])
                        item[field.name] = _object
                    else:
                        if (field.one_to_one or field.many_to_one):  # 一对一、多对一字段, 用hssc_id获取对象
                            try:
                                _object = field.related_model.objects.get(hssc_id=item_dict[field.name])
                            except field.related_model.DoesNotExist:  # ManagedEntity.base_form中的hssc_id可能为空
                                _object = None
                            item[field.name] = _object
                        elif field.__class__.__name__ == 'DurationField':  # duration字段
                            item[field.name] = self._parse_timedelta(item_dict[field.name])
                        else:
                            item[field.name] = item_dict[field.name]

            # 插入构造好的记录，不包括多对多字段
            _instance=self.model.objects.create(**item)

            # 遍历模型多对多字段，用hssc_id或icpc_code获取对象
            for field in self.model._meta.many_to_many:
                if item_dict.get(field.name):  # 如果字段不为空，进行检查替换
                    objects = []
                    # 如果是ICPC外键，用icpc_code获取对象，否则用hssc_id获取对象
                    if field.name in ['name_icpc', 'icpc']:
                        for _object in field.related_model.objects.filter(icpc_code__in=item_dict[field.name]):
                            objects.append(_object)
                    else:
                        for _object in field.related_model.objects.filter(hssc_id__in=item_dict[field.name]):
                            objects.append(_object)

                    # 将对象添加到多对多字段中
                    eval(f'_instance.{field.name}').set(objects)
            
        return f'{self.model} 已恢复'

    @staticmethod
    def _parse_timedelta(stamp):
    # 转换string to timedelta
        if 'day' in stamp:
            m = re.match(r'(?P<d>[-\d]+) day[s]*, (?P<h>\d+):'
                        r'(?P<m>\d+):(?P<s>\d[\.\d+]*)', stamp)
        else:
            m = re.match(r'(?P<h>\d+):(?P<m>\d+):'
                        r'(?P<s>\d[\.\d+]*)', stamp)
        if not m:
            return ''

        time_dict = {key: float(val) for key, val in m.groupdict().items()}
        if 'd' in time_dict:
            return timedelta(days=time_dict['d'], hours=time_dict['h'],
                            minutes=time_dict['m'], seconds=time_dict['s'])
        else:
            return timedelta(hours=time_dict['h'],
                            minutes=time_dict['m'], seconds=time_dict['s'])


# Hssc基类
class HsscBase(models.Model):
    label = models.CharField(max_length=255, null=True, verbose_name="名称")
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="name")
    hssc_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="hsscID")
    objects = HsscBackupManager()

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if self.hssc_id is None:
            self.hssc_id = uuid.uuid1()
        super().save(*args, **kwargs)


class HsscPymBase(HsscBase):
    pym = models.CharField(max_length=255, blank=True, null=True, verbose_name="拼音码")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.label:
            self.pym = ''.join(lazy_pinyin(self.label, style=Style.FIRST_LETTER))
            if self.name is None or self.name=='':
                self.name = "_".join(lazy_pinyin(self.label))
        super().save(*args, **kwargs)


from enum import Enum
class FieldsType(Enum):
    boolfield_yao_pin_tong_yong_zi_duan = "String"  # 药品通用名
    boolfield_yao_pin_ming_cheng = "String"  # 药品名称
    boolfield_fu_yong_pin_ci = "String"  # 用药频次
    characterfield_right_eye_vision = "String"  # 右眼视力
    characterfield_supplementary_description_of_the_condition = "String"  # 病情补充描述
    characterfield_working_hours_per_day = "String"  # 每天工作及工作往返总时长
    characterfield_average_sleep_duration = "String"  # 平均睡眠时长
    characterfield_duration_of_insomnia = "String"  # 持续失眠时间
    characterfield_practice_qualification = "String"  # 执业资质
    characterfield_password_setting = "String"  # 密码设置
    characterfield_confirm_password = "String"  # 确认密码
    characterfield_expertise = "String"  # 专长
    characterfield_practice_time = "String"  # 执业时间
    characterfield_username = "String"  # 用户名
    characterfield_password = "String"  # 密码
    characterfield_left_eye_vision = "String"  # 左眼视力
    characterfield_resident_file_number = "String"  # 居民档案号
    characterfield_family_address = "String"  # 家庭地址
    characterfield_medical_ic_card_number = "String"  # 医疗ic卡号
    characterfield_jian_kang_dang_an_bian_hao = "String"  # 健康档案编号
    boolfield_jia_ting_qian_yue_fu_wu_xie_yi = "String"  # 家庭签约服务协议
    boolfield_yao_pin_bian_ma = "String"  # 药品编码
    boolfield_yao_pin_gui_ge = "String"  # 药品规格
    boolfield_zhi_yuan_bian_ma = "String"  # 职员编码
    boolfield_ji_gou_bian_ma = "String"  # 机构编码
    boolfield_ji_gou_ming_cheng = "String"  # 机构名称
    boolfield_ji_gou_dai_ma = "String"  # 机构代码
    boolfield_ji_gou_shu_xing = "String"  # 机构属性
    boolfield_ji_gou_ceng_ji = "String"  # 机构层级
    boolfield_suo_zai_hang_zheng_qu_hua_dai_ma = "String"  # 所在行政区划代码
    boolfield_xing_zheng_qu_hua_gui_shu = "String"  # 行政区划归属
    boolfield_fa_ding_fu_ze_ren = "String"  # 法定负责人
    boolfield_gong_ying_shang_bian_ma = "String"  # 供应商编码
    boolfield_zhu_yao_gong_ying_chan_pin = "String"  # 主要供应产品
    boolfield_gong_huo_zhou_qi = "String"  # 供货周期
    boolfield_zhuan_ye_fu_wu = "String"  # 专业服务
    boolfield_she_bei_bian_ma = "String"  # 设备编码
    boolfield_sheng_chan_chang_jia = "String"  # 生产厂家
    boolfield_she_bei_fu_wu_dan_wei_hao_shi = "String"  # 设备服务单位耗时
    boolfield_she_bei_jian_xiu_zhou_qi = "String"  # 设备检修周期
    boolfield_she_bei_shi_yong_cheng_ben = "String"  # 设备使用成本
    boolfield_chang_yong_chu_fang_liang = "String"  # 常用处方量
    boolfield_dui_zhao_yi_bao_ming_cheng = "String"  # 对照医保名称
    boolfield_dui_zhao_ji_yao_ming_cheng = "String"  # 对照基药名称
    boolfield_huan_suan_gui_ze = "String"  # 换算规则
    boolfield_zhi_xing_qian_ming = "String"  # 执行签名
    boolfield_yong_yao_zhou_qi = "String"  # 用药疗程
    boolfield_she_bei_ming_cheng = "String"  # 设备名称
    boolfield_gong_ying_shang_ming_cheng = "String"  # 供应商名称
    characterfield_contact_number = "String"  # 机构联系电话
    characterfield_gender = "String"  # 被保人性别
    characterfield_contact_address = "String"  # 机构联系地址
    characterhssc_identification_number = "String"  # 证件号码
    characterfield_age = "String"  # 年龄
    characterfield_name = "String"  # 被保人姓名
    boolfield_xu_hao = "String"  # 序号
    boolfield_bao_dan_hao = "String"  # 保单号
    boolfield_bao_xian_ze_ren = "String"  # 保险责任
    boolfield_jiu_zhen_wen_ti = "String"  # 就诊问题
    boolfield_fu_jia_fu_wu_yao_qiu = "String"  # 附加服务要求
    boolfield_yong_hu_ming = "String"  # 用户名
    boolfield_mi_ma_she_zhi = "String"  # 密码设置
    boolfield_que_ren_mi_ma = "String"  # 确认密码
    boolfield_shen_fen_xin_xi_yan_zheng = "String"  # 身份信息验证
    boolfield_jiu_zhen_yi_sheng = "String"  # 就诊医生
    boolfield_yu_yue_xu_hao = "String"  # 预约序号
    boolfield_cun_zai_de_wen_ti = "String"  # 存在的问题
    boolfield_qi_ta_xu_qiu = "String"  # 其他需求
    boolfield_nin_de_dan_xin_he_gu_lv = "String"  # 您的担心和顾虑
    boolfield_nin_xiang_yao_de_bang_zhu = "String"  # 您想要的帮助
    boolfield_shen_qing_ren_xing_ming = "String"  # 申请人姓名
    boolfield_zheng_jian_you_xiao_qi = "String"  # 证件有效期
    boolfield_hang_ye = "String"  # 行业
    boolfield_zhi_ye = "String"  # 职业
    boolfield_chang_zhu_di_zhi = "String"  # 常住地址
    boolfield_lian_xi_dian_hua = "String"  # 联系电话
    boolfield_bao_an_ren_lian_xi_dian_hua = "String"  # 报案人联系电话
    boolfield_chu_xian_ren_xing_ming = "String"  # 出险人姓名
    boolfield_chu_xian_di_dian = "String"  # 出险地点
    boolfield_shi_gu_gai_kuo = "String"  # 事故概括
    boolfield_bei_bao_xian_ren_zheng_jian_hao_ma = "String"  # 被保险人证件号码
    boolfield_gui_shu_cheng_shi = "String"  # 归属城市
    boolfield_yi_yuan_xin_xi = "String"  # 医院信息
    boolfield_ji_bing_xin_xi = "String"  # 疾病信息
    boolfield_li_pei_fang_shi = "String"  # 理赔方式
    boolfield_bei_zhu = "String"  # 备注
    boolfield_you_dai_gai_jin_de_fu_wu = "String"  # 有待改进的服务
    boolfield_nin_hai_xu_yao_de_fu_wu = "String"  # 您还需要的服务
    boolfield_xi_wang_zeng_jia_de_fu_wu_xiang_mu = "String"  # 希望增加的服务项目
    boolfield_bao_an_ren = "String"  # 报案人
    boolfield_guo_ji_di_qu = "String"  # 国籍/地区
    boolfield_li_pei_jin_e_bao_xiao_jian_mian_jin_e = "String"  # 理赔金额_报销/减免金额
    boolfield_chu_xian_di_dian_shi_ji_bie = "String"  # 出险地点_市级别
    boolfield_chu_xian_di_dian_sheng_ji_bie = "String"  # 出险地点_省级别
    boolfield_tui_dan_yuan_yin = "String"  # 人身险理赔申请书退单原因
    boolfield_li_pei_dui_zhang_dan_tui_dan_yuan_yin = "String"  # 理赔对账单退单原因
    boolfield_li_pei_fei_yong_hui_zong_dan_tui_dan_yuan_yin = "String"  # 理赔费用汇总单退单原因
    boolfield_men_zhen_ji_lu_dan_tui_dan_yuan_yin = "String"  # 门诊记录单退单原因
    boolfield_li_pei_shen_qing_tui_hui_yuan_yin = "String"  # 理赔申请退回原因
    numberfield_body_temperature = "Numbers"  # 体温
    numberfield_pulse = "Numbers"  # 脉搏
    numberfield_respiratory_rate = "Numbers"  # 呼吸频率
    numberfield_hight = "Numbers"  # 身高
    numberfield_weight = "Numbers"  # 体重
    numberfield_body_mass_index = "Numbers"  # 体质指数
    numberfield_blood_transfusion = "Numbers"  # 输血量
    numberfield_systolic_blood_pressure = "Numbers"  # 收缩压
    numberfield_tang_hua_xue_hong_dan_bai = "Numbers"  # 糖化血红蛋白
    numberfield_kong_fu_xue_tang = "Numbers"  # 空腹血糖
    numberfield_diastolic_blood_pressure = "Numbers"  # 舒张压
    A3501 = "Numbers"  # 尿微量白蛋白
    boolfield_yao_wei = "Numbers"  # 腰围
    boolfield_dang_qian_pai_dui_ren_shu = "Numbers"  # 当前排队人数
    boolfield_yu_ji_deng_hou_shi_jian = "Numbers"  # 预计等候时间
    boolfield_fei_yong_he_ji = "Numbers"  # 费用合计
    boolfield_fei_yong = "Numbers"  # 保单内服务费用
    boolfield_bao_dan_wai_fu_wu_fei_yong = "Numbers"  # 保单外服务费用
    datetimefield_date = "Date"  # 手术日期
    boolfield_shu_xue_ri_qi = "Date"  # 输血日期
    boolfield_wai_shang_ri_qi = "Date"  # 外伤日期
    datetimefield_time_of_diagnosis = "Datetime"  # 确诊时间
    boolfield_bao_zhi_qi = "Date"  # 保质期
    datetimefield_date_of_birth = "Date"  # 出生日期
    datetimefield_ri_qi_shi_jian = "Datetime"  # 预约时间
    boolfield_zhu_she_ri_qi = "Datetime"  # 注射日期
    boolfield_bao_xian_you_xiao_qi = "Date"  # 保险有效期
    boolfield_bao_an_shi_jian = "Datetime"  # 报案时间
    boolfield_chu_xian_shi_jian = "Datetime"  # 出险时间
    boolfield_yao_pin_dan_wei = "dictionaries.Yao_pin_dan_wei"  # 药品单位
    boolfield_xin_yu_ping_ji = "dictionaries.Xin_yu_ping_ji"  # 信誉评级
    boolfield_chu_fang_ji_liang_dan_wei = "dictionaries.Yao_pin_dan_wei"  # 处方计量单位
    boolfield_ru_ku_ji_liang_dan_wei = "dictionaries.Yao_pin_dan_wei"  # 入库计量单位
    boolfield_xiao_shou_ji_liang_dan_wei = "dictionaries.Yao_pin_dan_wei"  # 销售计量单位
    boolfield_she_bei_shi_yong_fu_wu_gong_neng = "icpc.Icpc4_physical_examination_and_tests"  # 设备适用服务功能
    relatedfield_affiliation = "entities.Ji_gou_ji_ben_xin_xi_biao"  # 所属机构
    relatedfield_symptom_list = "icpc.Icpc3_symptoms_and_problems"  # 症状
    relatedfield_gender = "dictionaries.Gender"  # 性别
    relatedfield_nationality = "dictionaries.Nationality"  # 民族
    relatedfield_marital_status = "dictionaries.Marital_status"  # 婚姻状况
    relatedfield_education = "dictionaries.Education"  # 文化程度
    relatedfield_occupational_status = "dictionaries.Occupational_status"  # 职业状况
    relatedfield_medical_expenses_burden = "dictionaries.Medical_expenses_burden"  # 医疗费用负担
    relatedfield_type_of_residence = "dictionaries.Type_of_residence"  # 居住类型
    relatedfield_blood_type = "dictionaries.Blood_type"  # 血型
    relatedfield_signed_family_doctor = "entities.Zhi_yuan_ji_ben_xin_xi_biao"  # 签约家庭医生
    relatedfield_athletic_ability = "dictionaries.Exercise_time"  # 运动能力
    relatedfield_personality_tendency = "dictionaries.Character"  # 性格倾向
    relatedfield_are_you_satisfied_with_the_job_and_life = "dictionaries.Satisfaction"  # 对目前生活和工作满意吗
    relatedfield_are_you_satisfied_with_your_adaptability = "dictionaries.Satisfaction"  # 对自己的适应能力满意吗
    relatedfield_can_you_get_encouragement_and_support_from_family = "dictionaries.Frequency"  # 是否能得到家人朋友的鼓励和支持
    relatedfield_drinking_frequency = "dictionaries.Frequency"  # 饮酒频次
    relatedfield_smoking_frequency = "dictionaries.Frequency"  # 吸烟频次
    relatedfield_own_health = "dictionaries.State_degree"  # 觉得自身健康状况如何
    relatedfield_compared_to_last_year = "dictionaries.Comparative_expression"  # 较之过去一年状态如何
    relatedfield_sports_preference = "dictionaries.Sports_preference"  # 运动偏好
    relatedfield_exercise_time = "dictionaries.Exercise_time"  # 运动时长
    relatedfield_have_any_recent_symptoms_of_physical_discomfort = "icpc.Icpc3_symptoms_and_problems"  # 近来有无身体不适症状
    relatedfield_is_the_living_environment_satisfactory = "dictionaries.Satisfaction"  # 您对居住环境满意吗
    relatedfield_is_the_transportation_convenient = "dictionaries.Convenience"  # 您所在的社区交通方便吗
    relatedfield_family_relationship = "dictionaries.Family_relationship"  # 家庭成员关系
    relatedfield_disease_name = "icpc.Icpc5_evaluation_and_diagnoses"  # 疾病名称
    relatedfield_fundus = "dictionaries.Normality"  # 眼底
    relatedfield_left_foot = "dictionaries.Dorsal_artery_pulsation"  # 左脚
    relatedfield_right_foot = "dictionaries.Dorsal_artery_pulsation"  # 右脚
    relatedfield_left_ear_hearing = "dictionaries.Hearing"  # 左耳听力
    relatedfield_right_ear_hearing = "dictionaries.Hearing"  # 右耳听力
    relatedfield_name_of_operation = "icpc.Icpc7_treatments"  # 手术名称
    relatedfield_lips = "dictionaries.Lips"  # 口唇
    relatedfield_dentition = "dictionaries.Dentition"  # 齿列
    relatedfield_pharynx = "dictionaries.Pharynx"  # 咽部
    relatedfield_major_life = "dictionaries.Life_event"  # 生活事件
    relatedfield_lower_extremity_edema = "dictionaries.Edema"  # 下肢水肿
    relatedfield_yi_lou_zhen_duan = "icpc.Icpc5_evaluation_and_diagnoses"  # 可能诊断
    relatedfield_pai_chu_zhen_duan = "icpc.Icpc5_evaluation_and_diagnoses"  # 排除诊断
    relatedfield_di_yi_zhen_duan = "icpc.Icpc5_evaluation_and_diagnoses"  # 第一诊断
    T4504 = "icpc.Icpc8_other_health_interventions"  # 健康教育
    boolfield_chang_yong_zheng_zhuang = "dictionaries.Chang_yong_zheng_zhuang"  # 常用症状
    boolfield_tang_niao_bing_zheng_zhuang = "dictionaries.Tang_niao_bing_zheng_zhuang"  # 糖尿病症状
    boolfield_yin_jiu_qing_kuang = "dictionaries.Yin_jiu_qing_kuang"  # 饮酒情况
    boolfield_xi_yan_qing_kuang = "dictionaries.Xi_yan_qing_kuang"  # 吸烟情况
    boolfield_shi_mian_qing_kuang = "dictionaries.Shi_mian_qing_kuang"  # 失眠情况
    boolfield_fen_zhen_que_ren = "dictionaries.Qian_dao_que_ren"  # 到达确认
    boolfield_da_bian_qing_kuang = "dictionaries.Da_bian_qing_kuang"  # 大便情况
    boolfield_sheng_huo_gong_zuo_ya_li_qing_kuang = "dictionaries.Ya_li_qing_kuang"  # 生活工作压力情况
    boolfield_kong_qi_wu_ran_qing_kuang = "dictionaries.Kong_qi_wu_ran_qing_kuang"  # 空气污染情况
    T4501 = "icpc.Icpc8_other_health_interventions"  # 营养干预
    boolfield_zao_sheng_wu_ran_qing_kuang = "dictionaries.Zao_sheng_wu_ran_qing_kuang"  # 噪声污染情况
    boolfield_shi_pin_he_yin_shui_an_quan_qing_kuang = "dictionaries.Shi_pin_he_yin_shui_an_quan_qing_kuang"  # 食品和饮水安全情况
    boolfield_yin_shi_gui_lv_qing_kuang = "dictionaries.Yin_shi_gui_lv_qing_kuang"  # 饮食规律情况
    boolfield_qi_ta_huan_jing_wu_ran_qing_kuang = "dictionaries.Qi_ta_huan_jing_wu_ran_qing_kuang"  # 其他环境污染情况
    boolfield_qian_yue_yong_hu = "dictionaries.Qian_yue_qing_kuang"  # 签约用户
    boolfield_shi_fou_ji_xu_shi_yong = "dictionaries.Ji_xu_shi_yong_qing_kuang"  # 是否继续使用
    boolfield_you_fou_you_man_xing_ji_bing = "dictionaries.Man_bing_diao_cha"  # 有否有慢性疾病
    boolfield_jian_kang_zhuang_kuang_zi_wo_ping_jia = "dictionaries.Jian_kang_zi_wo_ping_jia"  # 健康状况自我评价
    T4502 = "icpc.Icpc8_other_health_interventions"  # 运动干预
    boolfield_qian_yue_que_ren = "dictionaries.Qian_yue_que_ren"  # 签约确认
    boolfield_yuan_wai_jian_kang_ping_gu = "dictionaries.Sui_fang_ping_gu"  # 监测评估
    boolfield_niao_tang = "dictionaries.Niao_tang"  # 尿糖
    boolfield_dan_bai_zhi = "dictionaries.Dan_bai_zhi"  # 蛋白质
    boolfield_tong_ti = "dictionaries.Tong_ti"  # 尿酮体
    boolfield_yong_yao_tu_jing = "dictionaries.Yong_yao_tu_jing"  # 用药途径
    boolfield_yao_pin_fen_lei = "dictionaries.Yao_pin_fen_lei"  # 药品分类
    relatedfield_service_role = "dictionaries.Fu_wu_jue_se"  # 服务角色
    boolfield_ge_ren_bing_shi = "icpc.Icpc5_evaluation_and_diagnoses"  # 个人病史
    boolfield_yi_chuan_ji_bing = "icpc.Icpc5_evaluation_and_diagnoses"  # 遗传性疾病
    boolfield_jia_zu_xing_ji_bing = "icpc.Icpc5_evaluation_and_diagnoses"  # 家族性疾病
    boolfield_wai_shang_xing_ji_bing = "icpc.Icpc5_evaluation_and_diagnoses"  # 外伤性疾病
    boolfield_jia_zu_bing_shi_cheng_yuan = "dictionaries.Qin_shu_guan_xi"  # 家族病史成员
    boolfield_yi_chuan_bing_shi_cheng_yuan = "dictionaries.Qin_shu_guan_xi"  # 遗传病史成员
    boolfield_fu_wu_xiang_mu_ming_cheng = "icpc.Icpc4_physical_examination_and_tests"  # 服务项目名称
    boolfield_an_pai_que_ren = "dictionaries.An_pai_que_ren"  # 安排确认
    relatedfield_drug_name = "entities.None"  # 药品名
    boolfield_zheng_jian_lei_xing = "dictionaries.Zheng_jian_lei_xing"  # 证件类型
    boolfield_ze_ren_ren = "entities.Ji_gou_ji_ben_xin_xi_biao"  # 就诊机构
    boolfield_shi_yong_bao_xian_chan_pin = "dictionaries.Bao_xian_chan_pin"  # 使用服务产品
    boolfield_qian_dao_que_ren = "dictionaries.Jie_dan_que_ren"  # 接单确认
    boolfield_zhen_duan = "icpc.Icpc5_evaluation_and_diagnoses"  # 诊断
    boolfield_jian_cha_xiang_mu = "icpc.Icpc4_physical_examination_and_tests"  # 检查项目
    boolfield_zhi_liao_xiang_mu = "icpc.Icpc7_treatments"  # 治疗项目
    boolfield_yong_yao = "icpc.Icpc6_prescribe_medicines"  # 用药
    boolfield_qi_ta_fu_wu_xiang_mu = "icpc.Icpc8_other_health_interventions"  # 其他健康干预服务
    boolfield_fu_wu_xiao_lv_ping_fen = "dictionaries.Ping_fen"  # 服务效率评分
    boolfield_zhi_liao_jian_gou_tong_qing_kuang = "dictionaries.Gou_tong_qing_kuang"  # 治疗间沟通情况
    boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu = "dictionaries.Fu_wu_xiang_mu"  # 保单内服务收费项目
    boolfield_jie_dai_fu_wu = "dictionaries.Jie_dai_fu_wu"  # 接待服务
    boolfield_deng_hou_qing_kuang = "dictionaries.Deng_hou_shi_jian"  # 等候情况
    boolfield_fu_wu_xiao_guo_ping_jia = "dictionaries.Fu_wu_xiao_guo_ping_jia"  # 治疗感受/效果评价
    boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu = "dictionaries.Fu_wu_xiang_mu"  # 保单外服务收费项目
    boolfield_yu_chu_xian_ren_guan_xi = "dictionaries.Yu_chu_xian_ren_guan_xi"  # 与出险人关系
    boolfield_yi_liao_fu_wu_ji_neng_xiang_mu_ping_fen = "dictionaries.Ping_fen"  # 医疗服务技能项目评分
    boolfield_ping_tai_fu_wu_xiang_mu_ping_fen = "dictionaries.Ping_fen"  # 平台服务项目评分
    boolfield_fu_wu_liu_cheng_ping_fen = "dictionaries.Ping_fen"  # 服务流程评分
    boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu = "dictionaries.Qian_shu_que_ren"  # 理赔费用汇总单签署
    boolfield_qian_shu_que_ren = "dictionaries.Qian_shu_que_ren"  # 理赔对账单签署
    boolfield_li_pei_men_zhen_ji_lu_qian_shu = "dictionaries.Qian_shu_que_ren"  # 理赔门诊记录签署
    boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu = "dictionaries.Qian_shu_que_ren"  # 人身险理赔申请书签署
    boolfield_shi_fou_tong_guo_he_bao = "dictionaries.Shi_fou_shen_he_tong_guo"  # 是否审核通过
    boolfield_jiu_zhen_ji_gou_ze_ren_ren = "entities.Zhi_yuan_ji_ben_xin_xi_biao"  # 就诊机构责任人
    boolfield_shen_fen_zheng_jian_fu_jian = "None"  # 身份证件附件
    boolfield_fei_yong_qing_dan_fu_jian = "None"  # 汇总费用清单附件
    boolfield_men_zhen_bing_li_fu_jian = "None"  # 门诊病历附件
    boolfield_que_ren_ji_ben_xin_xi = "dictionaries.Xin_xi_que_ren"  # 是否绑定被保人信息
    boolfield_ju_jue_bang_ding_yuan_yin = "String"  # 拒绝绑定原因
    boolfield_ju_jue_jie_dan_yuan_yin = "String"  # 拒绝接单原因
    boolfield_shen_qing_ren_zheng_jian_fu_jian = "None"  # 申请人证件附件
    boolfield_bei_bao_ren_zheng_jian_fu_jian = "None"  # 被保人证件附件
    boolfield_dao_dian_shen_fen_yan_zheng = "None"  # 到店身份验证
    boolfield_nin_cong_he_chu_zhi_dao_wo_men_de_fu_wu = "dictionaries.Nin_cong_he_chu_zhi_dao_wo_men"  # 您从何处知道我们的服务
    boolfield_nin_shi_fou_yuan_yi_xiang_qin_peng_hao_you_tui_jian_wo_men_de_fu_wu = "dictionaries.Shi_fou_yuan_yi_xiang_jia_ren_peng_you_tui_jian_wo_men_de_fu_wu"  # 您是否愿意向亲朋好友推荐我们的服务