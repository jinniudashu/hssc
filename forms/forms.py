from django.db.models.query import QuerySet
from django.forms import ModelForm, Form,  widgets, fields, RadioSelect, Select, CheckboxSelectMultiple, CheckboxInput, SelectMultiple, NullBooleanSelect
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit

from .models import *

# class UserForm(ModelForm):
# 	pasword = forms.CharField(widget=forms.PasswordInput)
# 	role = forms.ModelChoiceField(queryset=Group.objects.all())