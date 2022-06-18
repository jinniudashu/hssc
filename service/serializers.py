from rest_framework import serializers
from .models import *
class Men_zhen_ji_lu_hui_zongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Men_zhen_ji_lu_hui_zong
        fields = '__all__'
class Chong_xin_yu_yue_an_paiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chong_xin_yu_yue_an_pai
        fields = '__all__'
class Zhen_suo_yu_yueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zhen_suo_yu_yue
        fields = '__all__'
class Li_pei_shen_qing_chong_shenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Li_pei_shen_qing_chong_shen
        fields = '__all__'
class Yu_yue_zi_xunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yu_yue_zi_xun
        fields = '__all__'
class Ti_jiao_he_bao_zi_liaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ti_jiao_he_bao_zi_liao
        fields = '__all__'
class Li_pei_shen_qing_fu_wuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Li_pei_shen_qing_fu_wu
        fields = '__all__'
class Li_pei_shen_qing_shu_shen_heSerializer(serializers.ModelSerializer):
    class Meta:
        model = Li_pei_shen_qing_shu_shen_he
        fields = '__all__'
class Man_yi_du_diao_chaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Man_yi_du_diao_cha
        fields = '__all__'
class Zhen_hou_sui_fangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zhen_hou_sui_fang
        fields = '__all__'
class Zhen_jian_sui_fangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zhen_jian_sui_fang
        fields = '__all__'
class Men_zhen_ji_luSerializer(serializers.ModelSerializer):
    class Meta:
        model = Men_zhen_ji_lu
        fields = '__all__'
class Yu_yue_tong_zhiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yu_yue_tong_zhi
        fields = '__all__'
class Fen_zhen_que_renSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fen_zhen_que_ren
        fields = '__all__'
class Yu_yue_que_renSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yu_yue_que_ren
        fields = '__all__'
class Yu_yue_an_paiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yu_yue_an_pai
        fields = '__all__'
class Ji_gou_ji_ben_xin_xi_biaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ji_gou_ji_ben_xin_xi_biao
        fields = '__all__'
class Zhi_yuan_ji_ben_xin_xi_biaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zhi_yuan_ji_ben_xin_xi_biao
        fields = '__all__'
class Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_chaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_cha
        fields = '__all__'
class She_bei_ji_ben_xin_xi_ji_luSerializer(serializers.ModelSerializer):
    class Meta:
        model = She_bei_ji_ben_xin_xi_ji_lu
        fields = '__all__'
class Gong_ying_shang_ji_ben_xin_xi_diao_chaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gong_ying_shang_ji_ben_xin_xi_diao_cha
        fields = '__all__'
class Yao_pin_ji_ben_xin_xi_biaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yao_pin_ji_ben_xin_xi_biao
        fields = '__all__'
class Ju_min_ji_ben_xin_xi_diao_chaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ju_min_ji_ben_xin_xi_diao_cha
        fields = '__all__'
