from django.db import models
from django.forms.models import model_to_dict
from datetime import timedelta
import uuid
import re
from pypinyin import Style, lazy_pinyin

# 自定义管理器：设计数据备份、恢复
class HsscBackupManager(models.Manager):
    def backup_data(self, queryset=None):
        backup_data = []
        # 如果没有指定查询集，则备份所有记录
        if queryset is None:
            queryset = self.all()
            
        for item in queryset:
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
        print('开始恢复：', self.model.__name__)
        self.all().delete()

        if data is None or len(data) == 0:
            return 'No data to restore'

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

    def merge_data(self, data):
        if data is None or len(data) == 0:
            return 'No data to restore'

        print('开始合并：', self.model.__name__)
        new_data_hssc_id = []
        for item_dict in data:
            # 用hssc_id判断当前记录是否已存在
            try:
                if self.model.__name__ == 'FormComponentsSetting':                    
                    print('formcomponentssetting:', item_dict)
                    new_data_hssc_id.append(item_dict['hssc_id'])
                else:
                    _instance = self.get(hssc_id=item_dict['hssc_id'])
            except self.model.DoesNotExist:
                _instance = None
                print('正在合并：',item_dict)
                
                # 保存添加记录的hssc_id，用于生成queryset
                new_data_hssc_id.append(item_dict['hssc_id'])
                
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

        # 返回新增记录的hssc_id
        return new_data_hssc_id


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
    # 手工添加CustomerSchedule字段数据类型
    scheduled_time = "Datetime"  # 计划执行时间
    overtime = "Datetime"  # 超期时限
    scheduled_operator = "entities.Stuff"  # 计划执行人员
    service = "core.Service"  # 服务
    is_assigned = 'Boolean'  # 是否已生成任务

    # 自动生成字段数据类型
    boolfield_yao_pin_tong_yong_ming = "String"  # 药品通用名
    boolfield_shen_fen_zheng_hao_ma = "String"  # 身份证号码
    boolfield_yao_pin_ming_cheng = "String"  # 药品名称
    boolfield_yong_yao_pin_ci = "String"  # 用药频次
    boolfield_bing_qing_bu_chong_miao_shu = "String"  # 病情补充描述
    boolfield_mei_tian_gong_zuo_ji_gong_zuo_wang_fan_zong_shi_chang = "String"  # 每天工作及工作往返总时长
    boolfield_ping_jun_shui_mian_shi_chang = "String"  # 平均睡眠时长
    boolfield_chi_xu_shi_mian_shi_jian = "String"  # 持续失眠时间
    boolfield_lian_xi_di_zhi = "String"  # 联系地址
    boolfield_zhi_ye_zi_zhi = "String"  # 执业资质
    boolfield_mi_ma_she_zhi = "String"  # 密码设置
    boolfield_que_ren_mi_ma = "String"  # 确认密码
    boolfield_zhuan_chang = "String"  # 专长
    boolfield_zhi_ye_shi_jian = "String"  # 执业时间
    boolfield_yong_hu_ming = "String"  # 用户名
    boolfield_mi_ma = "String"  # 密码
    boolfield_ju_min_dang_an_hao = "String"  # 居民档案号
    boolfield_jia_ting_di_zhi = "String"  # 家庭地址
    boolfield_yi_liao_ic_ka_hao = "String"  # 医疗ic卡号
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
    boolfield_yong_yao_liao_cheng = "String"  # 用药疗程
    boolfield_she_bei_ming_cheng = "String"  # 设备名称
    boolfield_gong_ying_shang_ming_cheng = "String"  # 供应商名称
    boolfield_lian_xi_dian_hua = "String"  # 联系电话
    boolfield_xing_ming = "String"  # 姓名
    boolfield_nian_ling = "String"  # 年龄
    boolfield_ti_wen = "Numbers"  # 体温
    boolfield_mai_bo = "Numbers"  # 脉搏
    boolfield_hu_xi_pin_lv = "Numbers"  # 呼吸频率
    boolfield_shen_gao = "Numbers"  # 身高
    boolfield_ti_zhong = "Numbers"  # 体重
    boolfield_ti_zhi_zhi_shu = "Numbers"  # 体质指数
    boolfield_shu_xue_liang = "Numbers"  # 输血量
    boolfield_shou_suo_ya = "Numbers"  # 收缩压
    boolfield_tang_hua_xue_hong_dan_bai = "Numbers"  # 糖化血红蛋白
    boolfield_kong_fu_xue_tang = "Numbers"  # 空腹血糖
    boolfield_shu_zhang_ya = "Numbers"  # 舒张压
    boolfield_yao_wei = "Numbers"  # 腰围
    boolfield_dang_qian_pai_dui_ren_shu = "Numbers"  # 当前排队人数
    boolfield_yu_ji_deng_hou_shi_jian = "Numbers"  # 预计等候时间
    boolfield_kong_fu_xue_tang_ping_jun_zhi = "Numbers"  # 空腹血糖平均值
    boolfield_can_hou_2_xiao_shi_xue_tang_ping_jun_zhi = "Numbers"  # 餐后2小时血糖平均值
    boolfield_can_hou_2_xiao_shi_xue_tang = "Numbers"  # 餐后2小时血糖
    boolfield_shou_shu_ri_qi = "Date"  # 手术日期
    boolfield_shu_xue_ri_qi = "Date"  # 输血日期
    boolfield_wai_shang_ri_qi = "Date"  # 外伤日期
    boolfield_que_zhen_shi_jian = "Datetime"  # 确诊时间
    boolfield_chu_sheng_ri_qi = "Date"  # 出生日期
    boolfield_yu_yue_shi_jian = "Datetime"  # 预约时间
    boolfield_zhu_she_ri_qi = "Datetime"  # 注射日期
    boolfield_yao_pin_dan_wei = "dictionaries.Yao_pin_dan_wei"  # 药品单位
    boolfield_xin_yu_ping_ji = "dictionaries.Xin_yu_ping_ji"  # 信誉评级
    boolfield_chu_fang_ji_liang_dan_wei = "dictionaries.Yao_pin_dan_wei"  # 处方计量单位
    boolfield_ru_ku_ji_liang_dan_wei = "dictionaries.Yao_pin_dan_wei"  # 入库计量单位
    boolfield_xiao_shou_ji_liang_dan_wei = "dictionaries.Yao_pin_dan_wei"  # 销售计量单位
    boolfield_she_bei_shi_yong_fu_wu_gong_neng = "icpc.Icpc4_physical_examination_and_tests"  # 设备适用服务功能
    boolfield_suo_shu_ji_gou = "entities.Ji_gou_ji_ben_xin_xi_biao"  # 所属机构
    boolfield_zheng_zhuang = "icpc.Icpc3_symptoms_and_problems"  # 症状
    boolfield_xing_bie = "dictionaries.Gender"  # 性别
    boolfield_min_zu = "dictionaries.Nationality"  # 民族
    boolfield_hun_yin_zhuang_kuang = "dictionaries.Marital_status"  # 婚姻状况
    boolfield_wen_hua_cheng_du = "dictionaries.Education"  # 文化程度
    boolfield_zhi_ye_zhuang_kuang = "dictionaries.Occupational_status"  # 职业状况
    boolfield_yi_liao_fei_yong_fu_dan = "dictionaries.Medical_expenses_burden"  # 医疗费用负担
    boolfield_ju_zhu_lei_xing = "dictionaries.Type_of_residence"  # 居住类型
    boolfield_xue_xing = "dictionaries.Blood_type"  # 血型
    boolfield_qian_yue_jia_ting_yi_sheng = "entities.Zhi_yuan_ji_ben_xin_xi_biao"  # 签约家庭医生
    boolfield_xing_ge_qing_xiang = "dictionaries.Character"  # 性格倾向
    boolfield_dui_mu_qian_sheng_huo_he_gong_zuo_man_yi_ma = "dictionaries.Satisfaction"  # 对目前生活和工作满意吗
    boolfield_dui_zi_ji_de_shi_ying_neng_li_man_yi_ma = "dictionaries.Satisfaction"  # 对自己的适应能力满意吗
    boolfield_yin_jiu_pin_ci = "dictionaries.Frequency"  # 饮酒频次
    boolfield_xi_yan_pin_ci = "dictionaries.Frequency"  # 吸烟频次
    boolfield_jue_de_zi_shen_jian_kang_zhuang_kuang_ru_he = "dictionaries.State_degree"  # 觉得自身健康状况如何
    boolfield_jiao_zhi_guo_qu_yi_nian_zhuang_tai_ru_he = "dictionaries.Comparative_expression"  # 较之过去一年状态如何
    boolfield_yun_dong_pian_hao = "dictionaries.Sports_preference"  # 运动偏好
    boolfield_yun_dong_shi_chang = "dictionaries.Exercise_time"  # 运动时长
    boolfield_jin_lai_you_wu_shen_ti_bu_shi_zheng_zhuang = "icpc.Icpc3_symptoms_and_problems"  # 近来有无身体不适症状
    boolfield_nin_dui_ju_zhu_huan_jing_man_yi_ma = "dictionaries.Satisfaction"  # 您对居住环境满意吗
    boolfield_nin_suo_zai_de_she_qu_jiao_tong_fang_bian_ma = "dictionaries.Convenience"  # 您所在的社区交通方便吗
    boolfield_jia_ting_cheng_yuan_guan_xi = "dictionaries.Family_relationship"  # 家庭成员关系
    boolfield_ji_bing_ming_cheng = "icpc.Icpc5_evaluation_and_diagnoses"  # 疾病名称
    boolfield_yan_di = "dictionaries.Normality"  # 眼底
    boolfield_zuo_jiao = "dictionaries.Dorsal_artery_pulsation"  # 左脚
    boolfield_you_jiao = "dictionaries.Dorsal_artery_pulsation"  # 右脚
    boolfield_shou_shu_ming_cheng = "icpc.Icpc7_treatments"  # 手术名称
    boolfield_yan_bu = "dictionaries.Pharynx"  # 咽部
    boolfield_xia_zhi_shui_zhong = "dictionaries.Edema"  # 下肢水肿
    boolfield_ke_neng_zhen_duan = "icpc.Icpc5_evaluation_and_diagnoses"  # 可能诊断
    boolfield_pai_chu_zhen_duan = "icpc.Icpc5_evaluation_and_diagnoses"  # 排除诊断
    boolfield_chang_yong_zheng_zhuang = "dictionaries.Chang_yong_zheng_zhuang"  # 常用症状
    boolfield_tang_niao_bing_zheng_zhuang = "dictionaries.Tang_niao_bing_zheng_zhuang"  # 糖尿病症状
    boolfield_qian_dao_que_ren = "dictionaries.Qian_dao_que_ren"  # 签到确认
    boolfield_shi_mian_qing_kuang = "dictionaries.Shi_mian_qing_kuang"  # 失眠情况
    boolfield_sheng_huo_gong_zuo_ya_li_qing_kuang = "dictionaries.Ya_li_qing_kuang"  # 生活工作压力情况
    boolfield_shi_fou_ji_xu_shi_yong = "dictionaries.Ji_xu_shi_yong_qing_kuang"  # 是否继续使用
    boolfield_qian_yue_que_ren = "dictionaries.Qian_yue_que_ren"  # 签约确认
    boolfield_ze_ren_ren = "entities.Zhi_yuan_ji_ben_xin_xi_biao"  # 责任人
    boolfield_xue_ya_jian_ce_ping_gu = "dictionaries.Sui_fang_ping_gu"  # 血压监测评估
    boolfield_niao_tang = "dictionaries.Niao_tang"  # 尿糖
    boolfield_dan_bai_zhi = "dictionaries.Dan_bai_zhi"  # 蛋白质
    boolfield_niao_tong_ti = "dictionaries.Tong_ti"  # 尿酮体
    boolfield_yong_yao_tu_jing = "dictionaries.Yong_yao_tu_jing"  # 用药途径
    boolfield_yao_pin_fen_lei = "dictionaries.Yao_pin_fen_lei"  # 药品分类
    boolfield_fu_wu_jue_se = "dictionaries.Fu_wu_jue_se"  # 服务角色
    boolfield_ge_ren_bing_shi = "icpc.Icpc5_evaluation_and_diagnoses"  # 个人病史
    boolfield_yi_chuan_xing_ji_bing = "icpc.Icpc5_evaluation_and_diagnoses"  # 遗传性疾病
    boolfield_jia_zu_xing_ji_bing = "icpc.Icpc5_evaluation_and_diagnoses"  # 家族性疾病
    boolfield_wai_shang_xing_ji_bing = "icpc.Icpc5_evaluation_and_diagnoses"  # 外伤性疾病
    boolfield_jia_zu_bing_shi_cheng_yuan = "dictionaries.Qin_shu_guan_xi"  # 家族病史成员
    boolfield_yi_chuan_bing_shi_cheng_yuan = "dictionaries.Qin_shu_guan_xi"  # 遗传病史成员
    boolfield_fu_wu_xiang_mu_ming_cheng = "icpc.Icpc4_physical_examination_and_tests"  # 服务项目名称
    boolfield_an_pai_que_ren = "dictionaries.An_pai_que_ren"  # 安排确认
    boolfield_yao_pin_ming = "entities.Yao_pin_ji_ben_xin_xi_biao"  # 药品名
    boolfield_tang_niao_bing_kong_zhi_xiao_guo_ping_gu = "dictionaries.Tang_niao_bing_kong_zhi_xiao_guo_ping_gu"  # 糖尿病控制效果评估