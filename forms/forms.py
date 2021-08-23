from django.forms import ModelForm
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit

from .models import *


class Metadata_follow_up_form_ModelForm(ModelForm):
	class Meta:
		model = Metadata_follow_up_form
		fields = ['name', 'serial_number', 'method', 'classification', 'opinion', 'agency', 'doctor_signature', 'date', 'next_date']

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


class Classification_checklist_ModelForm(ModelForm):
	class Meta:
		model = Classification_checklist
		fields = ['inspection_item']

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


class Routine_physical_examination_ModelForm(ModelForm):
	class Meta:
		model = Routine_physical_examination
		fields = ['name', 'gender', 'age', 'height', 'weight', 'bmi', 'test_comments']

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


class Classification_survey_list_ModelForm(ModelForm):
	class Meta:
		model = Classification_survey_list
		fields = ['surver_items']

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