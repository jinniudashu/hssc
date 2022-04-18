from django import forms
from django.forms import formset_factory

class OperationForm(forms.Form):
    archive_number = forms.CharField(max_length=20, required=False, label='居民档案号')
    customer__name = forms.CharField(max_length=20, label='姓名')
    service__name = forms.CharField(max_length=40, label='服务项目')
    phone = forms.CharField(max_length=20, label='联系电话')
    address = forms.CharField(max_length=40, label='家庭地址')
OperationFormSet = formset_factory(OperationForm, extra=2)


class OperationItemForm(forms.Form):
    service__name = forms.CharField(max_length=40, label='服务项目')
OperationItemFormSet = formset_factory(OperationItemForm, extra=2)