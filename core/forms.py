from django import forms
from django.forms import formset_factory

class OperationForm(forms.Form):
    customer_number = forms.CharField(max_length=20, required=False, label='居民档案号')
    customer_name = forms.CharField(max_length=20, label='姓名')
    service_label = forms.CharField(max_length=40, label='服务项目')
    customer_phone = forms.CharField(max_length=20, label='联系电话')
    customer_address = forms.CharField(max_length=40, label='家庭地址')
OperationFormSet = formset_factory(OperationForm, extra=2)
