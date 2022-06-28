from django.forms import ModelForm, inlineformset_factory

from core.models import Customer
from service.models import CustomerSchedule
class CustomerForScheduleForm(ModelForm):
    class Meta:
        model = Customer
        fields = ('name',)
CustomerScheduleFormSet = inlineformset_factory(Customer, CustomerSchedule, fields=('service', 'scheduled_time', 'scheduled_operator',), extra=0, can_delete=False)

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
        
from service.models import Ju_min_ji_ben_xin_xi_diao_cha
class Ju_min_ji_ben_xin_xi_diao_cha_HeaderForm(ModelForm):
    class Meta:
        model = Ju_min_ji_ben_xin_xi_diao_cha
        fields = ['boolfield_bei_bao_ren_xing_ming', 'boolfield_bei_bao_ren_xing_bie', 'boolfield_chu_sheng_ri_qi', 'boolfield_chang_zhu_di_zhi']
        