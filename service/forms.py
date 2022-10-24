from django.forms import ModelForm


from service.models import Ji_gou_ji_ben_xin_xi_biao
class Ji_gou_ji_ben_xin_xi_biao_HeaderForm(ModelForm):
    class Meta:
        model = Ji_gou_ji_ben_xin_xi_biao
        fields = []
        
from service.models import Zhi_yuan_ji_ben_xin_xi_biao
class Zhi_yuan_ji_ben_xin_xi_biao_HeaderForm(ModelForm):
    class Meta:
        model = Zhi_yuan_ji_ben_xin_xi_biao
        fields = []
        
from service.models import She_bei_ji_ben_xin_xi_ji_lu
class She_bei_ji_ben_xin_xi_ji_lu_HeaderForm(ModelForm):
    class Meta:
        model = She_bei_ji_ben_xin_xi_ji_lu
        fields = []
        
from service.models import Gong_ying_shang_ji_ben_xin_xi_diao_cha
class Gong_ying_shang_ji_ben_xin_xi_diao_cha_HeaderForm(ModelForm):
    class Meta:
        model = Gong_ying_shang_ji_ben_xin_xi_diao_cha
        fields = []
        
from service.models import Yao_pin_ji_ben_xin_xi_biao
class Yao_pin_ji_ben_xin_xi_biao_HeaderForm(ModelForm):
    class Meta:
        model = Yao_pin_ji_ben_xin_xi_biao
        fields = []
        
from service.models import Ju_min_ji_ben_xin_xi_diao_cha
class Ju_min_ji_ben_xin_xi_diao_cha_HeaderForm(ModelForm):
    class Meta:
        model = Ju_min_ji_ben_xin_xi_diao_cha
        fields = ['boolfield_xing_ming', 'boolfield_chu_sheng_ri_qi', 'boolfield_xing_bie', 'boolfield_jia_ting_di_zhi', 'boolfield_lian_xi_dian_hua']
        