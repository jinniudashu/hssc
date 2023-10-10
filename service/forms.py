from django.forms import ModelForm
from django.utils import timezone
from core.models import Customer

from service.models import Hui_zhen_zhen_duan_fu_wu_list
class Hui_zhen_zhen_duan_fu_wu_listForm(ModelForm):
    class Meta:
        model = Hui_zhen_zhen_duan_fu_wu_list
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs) 
        if not self.initial.get('boolfield_hui_zhen_ze_ren_ren', None):
            operator_customer = Customer.objects.get(id=self.user.id) if self.user else None
            operator_staff = operator_customer.staff if operator_customer else None
            operator_virtualstaff = operator_staff.virtualstaff if operator_staff else None
            # 判断人员字段的类型
            model_name = self._meta.model._meta.get_field('boolfield_hui_zhen_ze_ren_ren').remote_field.model.__name__
            if model_name == 'VirtualStaff':
                self.initial['boolfield_hui_zhen_ze_ren_ren'] = operator_virtualstaff
            elif model_name == 'Staff':
                self.initial['boolfield_hui_zhen_ze_ren_ren'] = operator_staff
            elif model_name == 'Customer':
                self.initial['boolfield_hui_zhen_ze_ren_ren'] = operator_customer

from service.models import Hui_zhen_jian_yi_fu_wu_list
class Hui_zhen_jian_yi_fu_wu_listForm(ModelForm):
    class Meta:
        model = Hui_zhen_jian_yi_fu_wu_list
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs) 
        if not self.initial.get('boolfield_hui_zhen_ze_ren_ren', None):
            operator_customer = Customer.objects.get(id=self.user.id) if self.user else None
            operator_staff = operator_customer.staff if operator_customer else None
            operator_virtualstaff = operator_staff.virtualstaff if operator_staff else None
            # 判断人员字段的类型
            model_name = self._meta.model._meta.get_field('boolfield_hui_zhen_ze_ren_ren').remote_field.model.__name__
            if model_name == 'VirtualStaff':
                self.initial['boolfield_hui_zhen_ze_ren_ren'] = operator_virtualstaff
            elif model_name == 'Staff':
                self.initial['boolfield_hui_zhen_ze_ren_ren'] = operator_staff
            elif model_name == 'Customer':
                self.initial['boolfield_hui_zhen_ze_ren_ren'] = operator_customer

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
        