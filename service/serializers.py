from rest_framework import serializers
from .models import *
from icpc.serializers import *

class Men_zhen_chu_fang_biaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Men_zhen_chu_fang_biao
        fields = '__all__'

class A6501Serializer(serializers.ModelSerializer):
    class Meta:
        model = A6501
        fields = '__all__'

class A6502Serializer(serializers.ModelSerializer):
    class Meta:
        model = A6502
        fields = '__all__'

class A3101Serializer(serializers.ModelSerializer):
    class Meta:
        model = A3101
        fields = '__all__'

class Tang_niao_bing_zhuan_yong_wen_zhenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tang_niao_bing_zhuan_yong_wen_zhen
        fields = '__all__'

class Yao_shi_fu_wuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yao_shi_fu_wu
        fields = '__all__'

class Tang_niao_bing_zi_wo_jian_ceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tang_niao_bing_zi_wo_jian_ce
        fields = '__all__'

class A6217Serializer(serializers.ModelSerializer):
    class Meta:
        model = A6217
        fields = '__all__'

class A6201Serializer(serializers.ModelSerializer):
    class Meta:
        model = A6201
        fields = '__all__'

class A6218Serializer(serializers.ModelSerializer):
    icpc3_symptoms_and_problems_iname = serializers.CharField(source='icpc3_symptoms_and_problems_for_relatedfield_symptom_list_A6218.iname')
    # icpc3_symptoms_and_problems_iname = serializers.CharField(source='icpc3_symptoms_and_problems.iname')
    class Meta:
        model = A6218
        fields = ('characterfield_name', 'relatedfield_symptom_list', 'icpc3_symptoms_and_problems_iname')

class T8901Serializer(serializers.ModelSerializer):
    class Meta:
        model = T8901
        fields = '__all__'

class T6301Serializer(serializers.ModelSerializer):
    class Meta:
        model = T6301
        fields = '__all__'

class A6202Serializer(serializers.ModelSerializer):
    class Meta:
        model = A6202
        fields = '__all__'

class A6220Serializer(serializers.ModelSerializer):
    class Meta:
        model = A6220
        fields = '__all__'

class A6299Serializer(serializers.ModelSerializer):
    class Meta:
        model = A6299
        fields = '__all__'

class A3502Serializer(serializers.ModelSerializer):
    class Meta:
        model = A3502
        fields = '__all__'

class Tang_niao_bing_cha_tiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tang_niao_bing_cha_ti
        fields = '__all__'

class Xue_ya_jian_ceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xue_ya_jian_ce
        fields = '__all__'

class Kong_fu_xue_tang_jian_chaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kong_fu_xue_tang_jian_cha
        fields = '__all__'

class Tang_hua_xue_hong_dan_bai_jian_cha_biaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tang_hua_xue_hong_dan_bai_jian_cha_biao
        fields = '__all__'

class T9001Serializer(serializers.ModelSerializer):
    class Meta:
        model = T9001
        fields = '__all__'

class Qian_yue_fu_wuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qian_yue_fu_wu
        fields = '__all__'

class Shu_ye_zhu_sheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shu_ye_zhu_she
        fields = '__all__'

class Ju_min_ji_ben_xin_xi_diao_chaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ju_min_ji_ben_xin_xi_diao_cha
        fields = '__all__'
