from django.forms import ModelForm
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit

from .models import *


class User_registry_ModelForm(ModelForm):
	class Meta:
		model = User_registry
		fields = ['name', 'gender', 'age', 'identification_number', 'contact_information', 'contact_address', 'password_setting', 'confirm_password']

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


class Doctor_login_ModelForm(ModelForm):
	class Meta:
		model = Doctor_login
		fields = ['service_role', 'username', 'password']

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


class User_login_ModelForm(ModelForm):
	class Meta:
		model = User_login
		fields = ['username', 'password']

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


class Doctor_registry_ModelForm(ModelForm):
	class Meta:
		model = Doctor_registry
		fields = ['name', 'gender', 'age', 'identification_number', 'contact_information', 'contact_address', 'service_role', 'practice_qualification', 'password_setting', 'confirm_password']

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



class Basic_personal_information_ModelForm(ModelForm):
	class Meta:
		model = Basic_personal_information
		fields = ['family_id', 'family_relationship', 'resident_file_number', 'name', 'gender', 'date_of_birth', 'nationality', 'marital_status', 'education', 'occupational_status', 'identification_number', 'family_address', 'contact_number', 'medical_ic_card_number', 'medical_expenses_burden', 'type_of_residence', 'blood_type', 'contract_signatory', 'signed_family_doctor']

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


class Family_history_ModelForm(ModelForm):
	class Meta:
		model = Family_history
		fields = ['diseases', 'family_relationship']

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


class History_of_infectious_diseases_ModelForm(ModelForm):
	class Meta:
		model = History_of_infectious_diseases
		fields = ['diseases']

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