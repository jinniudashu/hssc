from django.db.models.query import QuerySet
from django.forms import ModelForm, Form,  widgets, fields, RadioSelect, Select, CheckboxSelectMultiple, CheckboxInput, SelectMultiple, NullBooleanSelect
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit

from .models import *

# class UserForm(ModelForm):
# 	pasword = forms.CharField(widget=forms.PasswordInput)
# 	role = forms.ModelChoiceField(queryset=Group.objects.all())


class History_of_trauma_ModelForm(ModelForm):
	class Meta:
		model = History_of_trauma
		fields = ['choose', 'diseases_name', 'date']
		widgets = {"choose": RadioSelect(),}

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


class Out_of_hospital_self_report_survey_ModelForm(ModelForm):
	class Meta:
		model = Out_of_hospital_self_report_survey
		fields = ['symptom_list']
		widgets = {}

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


class Personal_comprehensive_psychological_quality_survey_ModelForm(ModelForm):
	class Meta:
		model = Personal_comprehensive_psychological_quality_survey
		fields = ['personality_tendency', 'is_life_fun']
		widgets = {"is_life_fun": Select(),}

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


class Personal_health_assessment_ModelForm(ModelForm):
	class Meta:
		model = Personal_health_assessment
		fields = ['do_you_feel_healthy']
		widgets = {"do_you_feel_healthy": RadioSelect(),}

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


class Allergies_history_ModelForm(ModelForm):
	class Meta:
		model = Allergies_history
		fields = ['drug_name']
		widgets = {"drug_name": CheckboxSelectMultiple(),}

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


class Personal_health_behavior_survey_ModelForm(ModelForm):
	class Meta:
		model = Personal_health_behavior_survey
		fields = ['is_the_diet_regular', 'is_the_diet_proportion_healthy', 'whether_the_bowel_movements_are_regular', 'whether_to_drink_alcohol', 'drinking_frequency', 'do_you_smoke', 'smoking_frequency', 'average_sleep_duration', 'insomnia', 'duration_of_insomnia']
		widgets = {"is_the_diet_regular": CheckboxSelectMultiple(),"is_the_diet_proportion_healthy": CheckboxSelectMultiple(),"whether_the_bowel_movements_are_regular": CheckboxSelectMultiple(),"whether_to_drink_alcohol": CheckboxSelectMultiple(),"do_you_smoke": Select(),"insomnia": Select(),}

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


class History_of_blood_transfusion_ModelForm(ModelForm):
	class Meta:
		model = History_of_blood_transfusion
		fields = ['date', 'blood_transfusion']
		widgets = {}

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


class Social_environment_assessment_ModelForm(ModelForm):
	class Meta:
		model = Social_environment_assessment
		fields = ['is_the_living_environment_satisfactory', 'is_the_transportation_convenient']
		widgets = {"is_the_living_environment_satisfactory": Select(),"is_the_transportation_convenient": Select(),}

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


class Medical_history_ModelForm(ModelForm):
	class Meta:
		model = Medical_history
		fields = ['disease_name', 'time_of_diagnosis']
		widgets = {}

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


class Major_life_events_ModelForm(ModelForm):
	class Meta:
		model = Major_life_events
		fields = ['major_life', 'date']
		widgets = {"major_life": CheckboxSelectMultiple(),}

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


class Physical_examination_vision_ModelForm(ModelForm):
	class Meta:
		model = Physical_examination_vision
		fields = ['left_eye_vision', 'right_eye_vision']
		widgets = {}

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


class Family_survey_ModelForm(ModelForm):
	class Meta:
		model = Family_survey
		fields = ['diseases', 'family_relationship']
		widgets = {"family_relationship": CheckboxSelectMultiple(),}

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


class History_of_surgery_ModelForm(ModelForm):
	class Meta:
		model = History_of_surgery
		fields = ['name_of_operation', 'date']
		widgets = {}

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


class Blood_pressure_monitoring_ModelForm(ModelForm):
	class Meta:
		model = Blood_pressure_monitoring
		fields = ['systolic_blood_pressure', 'diastolic_blood_pressure']
		widgets = {}

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


class User_registry_ModelForm(ModelForm):
	class Meta:
		model = User_registry
		fields = ['name', 'gender', 'date_of_birth', 'age', 'identification_number', 'contact_information', 'contact_address', 'password_setting', 'confirm_password']
		widgets = {}

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
		fields = ['name', 'gender', 'age', 'identification_number', 'contact_information', 'contact_address', 'service_role', 'practice_qualification', 'password_setting', 'confirm_password', 'expertise', 'practice_time', 'affiliation', 'date_of_birth']
		widgets = {"service_role": CheckboxSelectMultiple(),"affiliation": RadioSelect(),}

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
		widgets = {}

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
		widgets = {}

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


class Vital_signs_check_ModelForm(ModelForm):
	class Meta:
		model = Vital_signs_check
		fields = ['body_temperature', 'pulse', 'respiratory_rate']
		widgets = {}

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


class Physical_examination_hearing_ModelForm(ModelForm):
	class Meta:
		model = Physical_examination_hearing
		fields = ['left_ear_hearing', 'rightearhearing']
		widgets = {"left_ear_hearing": Select(),"rightearhearing": Select(),}

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
		widgets = {"family_relationship": RadioSelect(),"gender": RadioSelect(),"nationality": RadioSelect(),"marital_status": RadioSelect(),"education": RadioSelect(),"occupational_status": RadioSelect(),"medical_expenses_burden": RadioSelect(),"type_of_residence": RadioSelect(),"blood_type": RadioSelect(),"contract_signatory": RadioSelect(),"signed_family_doctor": RadioSelect(),}

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
		fields = ['diseases', 'family_relationship']
		widgets = {"family_relationship": CheckboxSelectMultiple(),}

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


class Physical_examination_ModelForm(ModelForm):
	class Meta:
		model = Physical_examination
		fields = ['hight', 'weight', 'body_mass_index']
		widgets = {}

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


class Personal_adaptability_assessment_ModelForm(ModelForm):
	class Meta:
		model = Personal_adaptability_assessment
		fields = ['do_you_feel_pressured_at_work', 'do_you_often_work_overtime', 'working_hours_per_day', 'are_you_satisfied_with_the_job']
		widgets = {"do_you_feel_pressured_at_work": Select(),"do_you_often_work_overtime": Select(),"are_you_satisfied_with_the_job": Select(),}

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


class Physical_examination_abdomen_ModelForm(ModelForm):
	class Meta:
		model = Physical_examination_abdomen
		fields = ['tenderness']
		widgets = {"tenderness": Select(),}

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


class Physical_examination_athletic_ability_ModelForm(ModelForm):
	class Meta:
		model = Physical_examination_athletic_ability
		fields = ['athletic_ability']
		widgets = {"athletic_ability": Select(),}

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


class Physical_examination_oral_cavity_ModelForm(ModelForm):
	class Meta:
		model = Physical_examination_oral_cavity
		fields = ['lips', 'dentition', 'pharynx']
		widgets = {"lips": RadioSelect(),"dentition": RadioSelect(),"pharynx": Select(),}

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


class Physical_examination_lungs_ModelForm(ModelForm):
	class Meta:
		model = Physical_examination_lungs
		fields = ['barrel_chest']
		widgets = {"barrel_chest": Select(),}

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


class Physical_examination_limbs_ModelForm(ModelForm):
	class Meta:
		model = Physical_examination_limbs
		fields = []
		widgets = {}

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


class Physical_examination_skin_ModelForm(ModelForm):
	class Meta:
		model = Physical_examination_skin
		fields = ['skin']
		widgets = {}

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


class Physical_examination_sclera_ModelForm(ModelForm):
	class Meta:
		model = Physical_examination_sclera
		fields = ['sclera']
		widgets = {}

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


class Physical_examination_lymph_nodes_ModelForm(ModelForm):
	class Meta:
		model = Physical_examination_lymph_nodes
		fields = ['lymph_nodes']
		widgets = {}

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


class Physical_examination_spine_ModelForm(ModelForm):
	class Meta:
		model = Physical_examination_spine
		fields = []
		widgets = {}

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


class Physical_examination_diabetes_ModelForm(ModelForm):
	class Meta:
		model = Physical_examination_diabetes
		fields = ['fundus', 'lower_extremity_edema', 'zbdm']
		widgets = {"fundus": Select(),"zbdm": Select(),}

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