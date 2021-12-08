from django.forms import ModelForm, Form,  widgets, fields, RadioSelect, Select, CheckboxSelectMultiple, CheckboxInput, SelectMultiple, NullBooleanSelect
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit

from .models import *

class Ge_ren_ji_ben_xin_xi_1638359483_baseform_ModelForm(ModelForm):
    class Meta:
        model = Ge_ren_ji_ben_xin_xi_1638359483
        fields = ['xing_ming_1638358955', 'di_zhi_1638358983', 'dian_hua_1638358998', 'shen_gao_1638359066', 'ti_zhong_1638359087', 'ri_qi_1638359153', 'chu_sheng_ri_qi_1638359167', 'xing_bie_1638359238', 'xue_xing_1638359282', 'zheng_zhuang_1638359376', ]
        widgets = {'xing_bie_1638359238': RadioSelect, 'xue_xing_1638359282': Select, 'zheng_zhuang_1638359376': Select, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Ji_bing_shi_1638359530_baseform_ModelForm(ModelForm):
    class Meta:
        model = Ji_bing_shi_1638359530
        fields = ['xing_ming_1638358955', 'ri_qi_1638359153', 'zhen_duan_1638359350', ]
        widgets = {'zhen_duan_1638359350': SelectMultiple, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Ge_ren_ji_ben_xin_xi_1638359483_baseform_query_1638359584_ModelForm(ModelForm):
    class Meta:
        model = Ge_ren_ji_ben_xin_xi_1638359483
        fields = ['xing_ming_1638358955', 'chu_sheng_ri_qi_1638359167', 'xing_bie_1638359238', 'xue_xing_1638359282', ]
        widgets = {'xing_bie_1638359238': RadioSelect, 'xue_xing_1638359282': Select, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug

class Ge_ren_ji_ben_xin_xi_1638359483_baseform_query_1638361337_ModelForm(ModelForm):
    class Meta:
        model = Ge_ren_ji_ben_xin_xi_1638359483
        fields = ['xing_ming_1638358955', 'xing_bie_1638359238', ]
        widgets = {'xing_bie_1638359238': RadioSelect, }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.layout = Layout(HTML("<hr />"))
        for field in self.Meta().fields:
            helper.layout.append(Field(field, wrapper_class="row"))
        helper.layout.append(Submit("submit", "保存", css_class="btn-success"))
        helper.field_class = "col-8"
        helper.label_class = "col-2"
        return helper

    def clean_slug(self):
        new_slug = self.cleaned_data.get("slug").lower()
        if new_slug == "create":
            raise ValidationError("Slug may not be create")
        return new_slug
