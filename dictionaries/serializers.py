from rest_framework import serializers
from .models import *

class An_pai_que_renSerializer(serializers.ModelSerializer):
    class Meta:
        model = An_pai_que_ren
        fields = 'value'

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = 'value'

class SatisfactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Satisfaction
        fields = 'value'

class FrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Frequency
        fields = 'value'

class State_degreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = State_degree
        fields = 'value'

class Comparative_expressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comparative_expression
        fields = 'value'

class Sports_preferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sports_preference
        fields = 'value'

class Exercise_timeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise_time
        fields = 'value'

class ConvenienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convenience
        fields = 'value'

class Family_relationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Family_relationship
        fields = 'value'

class NormalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Normality
        fields = 'value'

class Dorsal_artery_pulsationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dorsal_artery_pulsation
        fields = 'value'

class HearingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hearing
        fields = 'value'

class LipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lips
        fields = 'value'

class DentitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dentition
        fields = 'value'

class PharynxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharynx
        fields = 'value'

class Life_eventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Life_event
        fields = 'value'

class EdemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edema
        fields = 'value'

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = 'value'

class NationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationality
        fields = 'value'

class Marital_statusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marital_status
        fields = 'value'

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = 'value'

class Occupational_statusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupational_status
        fields = 'value'

class Medical_expenses_burdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medical_expenses_burden
        fields = 'value'

class Type_of_residenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_of_residence
        fields = 'value'

class Blood_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blood_type
        fields = 'value'

class Chang_yong_zheng_zhuangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chang_yong_zheng_zhuang
        fields = 'value'

class Tang_niao_bing_zheng_zhuangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tang_niao_bing_zheng_zhuang
        fields = 'value'

class Xi_yan_qing_kuangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xi_yan_qing_kuang
        fields = 'value'

class Yin_jiu_qing_kuangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yin_jiu_qing_kuang
        fields = 'value'

class Qian_dao_que_renSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qian_dao_que_ren
        fields = 'value'

class Shi_mian_qing_kuangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shi_mian_qing_kuang
        fields = 'value'

class Da_bian_qing_kuangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Da_bian_qing_kuang
        fields = 'value'

class Ya_li_qing_kuangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ya_li_qing_kuang
        fields = 'value'

class Kong_qi_wu_ran_qing_kuangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kong_qi_wu_ran_qing_kuang
        fields = 'value'

class Zao_sheng_wu_ran_qing_kuangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zao_sheng_wu_ran_qing_kuang
        fields = 'value'

class Shi_pin_he_yin_shui_an_quan_qing_kuangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shi_pin_he_yin_shui_an_quan_qing_kuang
        fields = 'value'

class Yin_shi_gui_lv_qing_kuangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yin_shi_gui_lv_qing_kuang
        fields = 'value'

class Qi_ta_huan_jing_wu_ran_qing_kuangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qi_ta_huan_jing_wu_ran_qing_kuang
        fields = 'value'

class Ji_xu_shi_yong_qing_kuangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ji_xu_shi_yong_qing_kuang
        fields = 'value'

class Qian_yue_qing_kuangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qian_yue_qing_kuang
        fields = 'value'

class Man_bing_diao_chaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Man_bing_diao_cha
        fields = 'value'

class Jian_kang_zi_wo_ping_jiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jian_kang_zi_wo_ping_jia
        fields = 'value'

class Qian_yue_que_renSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qian_yue_que_ren
        fields = 'value'

class Sui_fang_ping_guSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sui_fang_ping_gu
        fields = 'value'

class Tong_tiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tong_ti
        fields = 'value'

class Niao_tangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Niao_tang
        fields = 'value'

class Dan_bai_zhiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dan_bai_zhi
        fields = 'value'

class Yong_yao_tu_jingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yong_yao_tu_jing
        fields = 'value'

class Xin_yu_ping_jiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xin_yu_ping_ji
        fields = 'value'

class Yao_pin_dan_weiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yao_pin_dan_wei
        fields = 'value'

class Yao_pin_fen_leiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yao_pin_fen_lei
        fields = 'value'

class Fu_wu_jue_seSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fu_wu_jue_se
        fields = 'value'

class She_bei_shi_yong_fu_wu_gong_nengSerializer(serializers.ModelSerializer):
    class Meta:
        model = She_bei_shi_yong_fu_wu_gong_neng
        fields = 'value'

class Qin_shu_guan_xiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qin_shu_guan_xi
        fields = 'value'

class Bao_xian_chan_pinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bao_xian_chan_pin
        fields = 'value'

class Jie_dan_que_renSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jie_dan_que_ren
        fields = 'value'

class Gou_tong_qing_kuangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gou_tong_qing_kuang
        fields = 'value'

class Deng_hou_shi_jianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deng_hou_shi_jian
        fields = 'value'

class Jie_dai_fu_wuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jie_dai_fu_wu
        fields = 'value'

class Fu_wu_xiao_guo_ping_jiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fu_wu_xiao_guo_ping_jia
        fields = 'value'

class Fu_wu_xiang_muSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fu_wu_xiang_mu
        fields = 'value'

class Yu_chu_xian_ren_guan_xiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yu_chu_xian_ren_guan_xi
        fields = 'value'

class Ping_fenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ping_fen
        fields = 'value'

class Zheng_jian_lei_xingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zheng_jian_lei_xing
        fields = 'value'

class Qian_shu_que_renSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qian_shu_que_ren
        fields = 'value'

class Shi_fou_tong_guoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shi_fou_tong_guo
        fields = 'value'

class Xin_xi_que_renSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xin_xi_que_ren
        fields = 'value'
