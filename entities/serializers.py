from rest_framework import serializers
from .models import *

class A6203Serializer(serializers.ModelSerializer):
    class Meta:
        model = A6203
        fields = '__all__'

class Yao_pin_ji_ben_xin_xi_biaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yao_pin_ji_ben_xin_xi_biao
        fields = '__all__'

class Zhi_yuan_ji_ben_xin_xi_biaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zhi_yuan_ji_ben_xin_xi_biao
        fields = '__all__'

class Ji_gou_ji_ben_xin_xi_biaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ji_gou_ji_ben_xin_xi_biao
        fields = '__all__'

class She_bei_ji_ben_xin_xi_biaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = She_bei_ji_ben_xin_xi_biao
        fields = '__all__'

class Wu_liu_gong_ying_shang_ji_ben_xin_xi_biaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wu_liu_gong_ying_shang_ji_ben_xin_xi_biao
        fields = '__all__'
