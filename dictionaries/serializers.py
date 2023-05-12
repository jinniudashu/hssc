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

class PharynxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharynx
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

class Qian_dao_que_renSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qian_dao_que_ren
        fields = 'value'

class Shi_mian_qing_kuangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shi_mian_qing_kuang
        fields = 'value'

class Ya_li_qing_kuangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ya_li_qing_kuang
        fields = 'value'

class Ji_xu_shi_yong_qing_kuangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ji_xu_shi_yong_qing_kuang
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

class Qin_shu_guan_xiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qin_shu_guan_xi
        fields = 'value'

class Tang_niao_bing_kong_zhi_xiao_guo_ping_guSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tang_niao_bing_kong_zhi_xiao_guo_ping_gu
        fields = 'value'

class Deng_hou_shi_jianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deng_hou_shi_jian
        fields = 'value'

class Fu_wu_xiao_guo_ping_jiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fu_wu_xiao_guo_ping_jia
        fields = 'value'

class Ping_fenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ping_fen
        fields = 'value'

class Nin_cong_he_chu_zhi_dao_wo_menSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nin_cong_he_chu_zhi_dao_wo_men
        fields = 'value'

class Shi_fou_yuan_yi_xiang_jia_ren_peng_you_tui_jian_wo_men_de_fu_wuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shi_fou_yuan_yi_xiang_jia_ren_peng_you_tui_jian_wo_men_de_fu_wu
        fields = 'value'
