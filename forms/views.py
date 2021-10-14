from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, resolve_url
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, RedirectView
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin

from core.models import Operation_proc

from .utils import DetailObjectMixin, CreateObjectMixin, UpdateObjectMixin, DeleteObjectMixin

from .models import *
from .forms import *

# class TestDetailView(DetailView):
# 	a = 'a'
# 	def get_object(self):
# 		slug = self.kwargs.get('slug')
# 		return get_object_or_404(Test, slug=slug)

class Index_view(ListView):
	model = Operation_proc
	template_name = 'index.html'

	# def get(self, request, *args, **kwargs):
	# 	self.object = self.get_object(queryset=Operation_proc.objects.exclude(state=4))

	def get_context_data(self, **kwargs):
		procs = Operation_proc.objects.exclude(state=4)
		todos = []
		for proc in procs:
			todo = {}
			todo['operation'] = proc.operation.label
			todo['url'] = f'{proc.operation.name}_update_url'
			todo['slug'] = proc.entry
			todos.append(todo)
		context = super().get_context_data(**kwargs)
		context['todos'] = todos
		return context

	# def get_queryset(self):
	# 	return Operation_proc.objects.exclude(state=4)


class History_of_trauma_ListView(ListView):
	model = History_of_trauma
	context_object_name = "history_of_traumas"
	template_name = "history_of_trauma_list.html"


class History_of_trauma_CreateView(SuccessMessageMixin, CreateView):
	template_name = "history_of_trauma_edit.html"
	form_class = History_of_trauma_ModelForm
	success_message = "保存成功！"


class History_of_trauma_DetailView(DetailView):
	model = History_of_trauma
	context_object_name = "history_of_trauma"
	template_name = "history_of_trauma_detail.html"

	def get_object(self):
		history_of_trauma = super(History_of_trauma_DetailView, self).get_object()
		form = History_of_trauma_ModelForm(instance=history_of_trauma)
		return form


class History_of_trauma_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "history_of_trauma_edit.html"
	form_class = History_of_trauma_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return History_of_trauma.objects.all()


class History_of_trauma_DeleteView(DeleteObjectMixin, View):
	model = History_of_trauma
	template = "history_of_trauma_delete.html"
	redirect_url = "history_of_trauma_list_url"
	raise_exception = True


class Out_of_hospital_self_report_survey_ListView(ListView):
	model = Out_of_hospital_self_report_survey
	context_object_name = "out_of_hospital_self_report_surveys"
	template_name = "out_of_hospital_self_report_survey_list.html"


class Out_of_hospital_self_report_survey_CreateView(SuccessMessageMixin, CreateView):
	template_name = "out_of_hospital_self_report_survey_edit.html"
	form_class = Out_of_hospital_self_report_survey_ModelForm
	success_message = "保存成功！"


class Out_of_hospital_self_report_survey_DetailView(DetailView):
	model = Out_of_hospital_self_report_survey
	context_object_name = "out_of_hospital_self_report_survey"
	template_name = "out_of_hospital_self_report_survey_detail.html"

	def get_object(self):
		out_of_hospital_self_report_survey = super(Out_of_hospital_self_report_survey_DetailView, self).get_object()
		form = Out_of_hospital_self_report_survey_ModelForm(instance=out_of_hospital_self_report_survey)
		return form


class Out_of_hospital_self_report_survey_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "out_of_hospital_self_report_survey_edit.html"
	form_class = Out_of_hospital_self_report_survey_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Out_of_hospital_self_report_survey.objects.all()


class Out_of_hospital_self_report_survey_DeleteView(DeleteObjectMixin, View):
	model = Out_of_hospital_self_report_survey
	template = "out_of_hospital_self_report_survey_delete.html"
	redirect_url = "out_of_hospital_self_report_survey_list_url"
	raise_exception = True


class Personal_comprehensive_psychological_quality_survey_ListView(ListView):
	model = Personal_comprehensive_psychological_quality_survey
	context_object_name = "personal_comprehensive_psychological_quality_surveys"
	template_name = "personal_comprehensive_psychological_quality_survey_list.html"


class Personal_comprehensive_psychological_quality_survey_CreateView(SuccessMessageMixin, CreateView):
	template_name = "personal_comprehensive_psychological_quality_survey_edit.html"
	form_class = Personal_comprehensive_psychological_quality_survey_ModelForm
	success_message = "保存成功！"


class Personal_comprehensive_psychological_quality_survey_DetailView(DetailView):
	model = Personal_comprehensive_psychological_quality_survey
	context_object_name = "personal_comprehensive_psychological_quality_survey"
	template_name = "personal_comprehensive_psychological_quality_survey_detail.html"

	def get_object(self):
		personal_comprehensive_psychological_quality_survey = super(Personal_comprehensive_psychological_quality_survey_DetailView, self).get_object()
		form = Personal_comprehensive_psychological_quality_survey_ModelForm(instance=personal_comprehensive_psychological_quality_survey)
		return form


class Personal_comprehensive_psychological_quality_survey_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "personal_comprehensive_psychological_quality_survey_edit.html"
	form_class = Personal_comprehensive_psychological_quality_survey_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Personal_comprehensive_psychological_quality_survey.objects.all()


class Personal_comprehensive_psychological_quality_survey_DeleteView(DeleteObjectMixin, View):
	model = Personal_comprehensive_psychological_quality_survey
	template = "personal_comprehensive_psychological_quality_survey_delete.html"
	redirect_url = "personal_comprehensive_psychological_quality_survey_list_url"
	raise_exception = True


class Personal_health_assessment_ListView(ListView):
	model = Personal_health_assessment
	context_object_name = "personal_health_assessments"
	template_name = "personal_health_assessment_list.html"


class Personal_health_assessment_CreateView(SuccessMessageMixin, CreateView):
	template_name = "personal_health_assessment_edit.html"
	form_class = Personal_health_assessment_ModelForm
	success_message = "保存成功！"


class Personal_health_assessment_DetailView(DetailView):
	model = Personal_health_assessment
	context_object_name = "personal_health_assessment"
	template_name = "personal_health_assessment_detail.html"

	def get_object(self):
		personal_health_assessment = super(Personal_health_assessment_DetailView, self).get_object()
		form = Personal_health_assessment_ModelForm(instance=personal_health_assessment)
		return form


class Personal_health_assessment_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "personal_health_assessment_edit.html"
	form_class = Personal_health_assessment_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Personal_health_assessment.objects.all()


class Personal_health_assessment_DeleteView(DeleteObjectMixin, View):
	model = Personal_health_assessment
	template = "personal_health_assessment_delete.html"
	redirect_url = "personal_health_assessment_list_url"
	raise_exception = True


class Allergies_history_ListView(ListView):
	model = Allergies_history
	context_object_name = "allergies_historys"
	template_name = "allergies_history_list.html"


class Allergies_history_CreateView(SuccessMessageMixin, CreateView):
	template_name = "allergies_history_edit.html"
	form_class = Allergies_history_ModelForm
	success_message = "保存成功！"


class Allergies_history_DetailView(DetailView):
	model = Allergies_history
	context_object_name = "allergies_history"
	template_name = "allergies_history_detail.html"

	def get_object(self):
		allergies_history = super(Allergies_history_DetailView, self).get_object()
		form = Allergies_history_ModelForm(instance=allergies_history)
		return form


class Allergies_history_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "allergies_history_edit.html"
	form_class = Allergies_history_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Allergies_history.objects.all()


class Allergies_history_DeleteView(DeleteObjectMixin, View):
	model = Allergies_history
	template = "allergies_history_delete.html"
	redirect_url = "allergies_history_list_url"
	raise_exception = True


class Personal_health_behavior_survey_ListView(ListView):
	model = Personal_health_behavior_survey
	context_object_name = "personal_health_behavior_surveys"
	template_name = "personal_health_behavior_survey_list.html"


class Personal_health_behavior_survey_CreateView(SuccessMessageMixin, CreateView):
	template_name = "personal_health_behavior_survey_edit.html"
	form_class = Personal_health_behavior_survey_ModelForm
	success_message = "保存成功！"


class Personal_health_behavior_survey_DetailView(DetailView):
	model = Personal_health_behavior_survey
	context_object_name = "personal_health_behavior_survey"
	template_name = "personal_health_behavior_survey_detail.html"

	def get_object(self):
		personal_health_behavior_survey = super(Personal_health_behavior_survey_DetailView, self).get_object()
		form = Personal_health_behavior_survey_ModelForm(instance=personal_health_behavior_survey)
		return form


class Personal_health_behavior_survey_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "personal_health_behavior_survey_edit.html"
	form_class = Personal_health_behavior_survey_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Personal_health_behavior_survey.objects.all()


class Personal_health_behavior_survey_DeleteView(DeleteObjectMixin, View):
	model = Personal_health_behavior_survey
	template = "personal_health_behavior_survey_delete.html"
	redirect_url = "personal_health_behavior_survey_list_url"
	raise_exception = True


class History_of_blood_transfusion_ListView(ListView):
	model = History_of_blood_transfusion
	context_object_name = "history_of_blood_transfusions"
	template_name = "history_of_blood_transfusion_list.html"


class History_of_blood_transfusion_CreateView(SuccessMessageMixin, CreateView):
	template_name = "history_of_blood_transfusion_edit.html"
	form_class = History_of_blood_transfusion_ModelForm
	success_message = "保存成功！"


class History_of_blood_transfusion_DetailView(DetailView):
	model = History_of_blood_transfusion
	context_object_name = "history_of_blood_transfusion"
	template_name = "history_of_blood_transfusion_detail.html"

	def get_object(self):
		history_of_blood_transfusion = super(History_of_blood_transfusion_DetailView, self).get_object()
		form = History_of_blood_transfusion_ModelForm(instance=history_of_blood_transfusion)
		return form


class History_of_blood_transfusion_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "history_of_blood_transfusion_edit.html"
	form_class = History_of_blood_transfusion_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return History_of_blood_transfusion.objects.all()


class History_of_blood_transfusion_DeleteView(DeleteObjectMixin, View):
	model = History_of_blood_transfusion
	template = "history_of_blood_transfusion_delete.html"
	redirect_url = "history_of_blood_transfusion_list_url"
	raise_exception = True


class Social_environment_assessment_ListView(ListView):
	model = Social_environment_assessment
	context_object_name = "social_environment_assessments"
	template_name = "social_environment_assessment_list.html"


class Social_environment_assessment_CreateView(SuccessMessageMixin, CreateView):
	template_name = "social_environment_assessment_edit.html"
	form_class = Social_environment_assessment_ModelForm
	success_message = "保存成功！"


class Social_environment_assessment_DetailView(DetailView):
	model = Social_environment_assessment
	context_object_name = "social_environment_assessment"
	template_name = "social_environment_assessment_detail.html"

	def get_object(self):
		social_environment_assessment = super(Social_environment_assessment_DetailView, self).get_object()
		form = Social_environment_assessment_ModelForm(instance=social_environment_assessment)
		return form


class Social_environment_assessment_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "social_environment_assessment_edit.html"
	form_class = Social_environment_assessment_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Social_environment_assessment.objects.all()


class Social_environment_assessment_DeleteView(DeleteObjectMixin, View):
	model = Social_environment_assessment
	template = "social_environment_assessment_delete.html"
	redirect_url = "social_environment_assessment_list_url"
	raise_exception = True


class Medical_history_ListView(ListView):
	model = Medical_history
	context_object_name = "medical_historys"
	template_name = "medical_history_list.html"


class Medical_history_CreateView(SuccessMessageMixin, CreateView):
	template_name = "medical_history_edit.html"
	form_class = Medical_history_ModelForm
	success_message = "保存成功！"


class Medical_history_DetailView(DetailView):
	model = Medical_history
	context_object_name = "medical_history"
	template_name = "medical_history_detail.html"

	def get_object(self):
		medical_history = super(Medical_history_DetailView, self).get_object()
		form = Medical_history_ModelForm(instance=medical_history)
		return form


class Medical_history_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "medical_history_edit.html"
	form_class = Medical_history_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Medical_history.objects.all()


class Medical_history_DeleteView(DeleteObjectMixin, View):
	model = Medical_history
	template = "medical_history_delete.html"
	redirect_url = "medical_history_list_url"
	raise_exception = True


class Major_life_events_ListView(ListView):
	model = Major_life_events
	context_object_name = "major_life_eventss"
	template_name = "major_life_events_list.html"


class Major_life_events_CreateView(SuccessMessageMixin, CreateView):
	template_name = "major_life_events_edit.html"
	form_class = Major_life_events_ModelForm
	success_message = "保存成功！"


class Major_life_events_DetailView(DetailView):
	model = Major_life_events
	context_object_name = "major_life_events"
	template_name = "major_life_events_detail.html"

	def get_object(self):
		major_life_events = super(Major_life_events_DetailView, self).get_object()
		form = Major_life_events_ModelForm(instance=major_life_events)
		return form


class Major_life_events_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "major_life_events_edit.html"
	form_class = Major_life_events_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Major_life_events.objects.all()


class Major_life_events_DeleteView(DeleteObjectMixin, View):
	model = Major_life_events
	template = "major_life_events_delete.html"
	redirect_url = "major_life_events_list_url"
	raise_exception = True


class Physical_examination_vision_ListView(ListView):
	model = Physical_examination_vision
	context_object_name = "physical_examination_visions"
	template_name = "physical_examination_vision_list.html"


class Physical_examination_vision_CreateView(SuccessMessageMixin, CreateView):
	template_name = "physical_examination_vision_edit.html"
	form_class = Physical_examination_vision_ModelForm
	success_message = "保存成功！"


class Physical_examination_vision_DetailView(DetailView):
	model = Physical_examination_vision
	context_object_name = "physical_examination_vision"
	template_name = "physical_examination_vision_detail.html"

	def get_object(self):
		physical_examination_vision = super(Physical_examination_vision_DetailView, self).get_object()
		form = Physical_examination_vision_ModelForm(instance=physical_examination_vision)
		return form


class Physical_examination_vision_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "physical_examination_vision_edit.html"
	form_class = Physical_examination_vision_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Physical_examination_vision.objects.all()


class Physical_examination_vision_DeleteView(DeleteObjectMixin, View):
	model = Physical_examination_vision
	template = "physical_examination_vision_delete.html"
	redirect_url = "physical_examination_vision_list_url"
	raise_exception = True


class Family_survey_ListView(ListView):
	model = Family_survey
	context_object_name = "family_surveys"
	template_name = "family_survey_list.html"


class Family_survey_CreateView(SuccessMessageMixin, CreateView):
	template_name = "family_survey_edit.html"
	form_class = Family_survey_ModelForm
	success_message = "保存成功！"


class Family_survey_DetailView(DetailView):
	model = Family_survey
	context_object_name = "family_survey"
	template_name = "family_survey_detail.html"

	def get_object(self):
		family_survey = super(Family_survey_DetailView, self).get_object()
		form = Family_survey_ModelForm(instance=family_survey)
		return form


class Family_survey_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "family_survey_edit.html"
	form_class = Family_survey_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Family_survey.objects.all()


class Family_survey_DeleteView(DeleteObjectMixin, View):
	model = Family_survey
	template = "family_survey_delete.html"
	redirect_url = "family_survey_list_url"
	raise_exception = True


class History_of_surgery_ListView(ListView):
	model = History_of_surgery
	context_object_name = "history_of_surgerys"
	template_name = "history_of_surgery_list.html"


class History_of_surgery_CreateView(SuccessMessageMixin, CreateView):
	template_name = "history_of_surgery_edit.html"
	form_class = History_of_surgery_ModelForm
	success_message = "保存成功！"


class History_of_surgery_DetailView(DetailView):
	model = History_of_surgery
	context_object_name = "history_of_surgery"
	template_name = "history_of_surgery_detail.html"

	def get_object(self):
		history_of_surgery = super(History_of_surgery_DetailView, self).get_object()
		form = History_of_surgery_ModelForm(instance=history_of_surgery)
		return form


class History_of_surgery_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "history_of_surgery_edit.html"
	form_class = History_of_surgery_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return History_of_surgery.objects.all()


class History_of_surgery_DeleteView(DeleteObjectMixin, View):
	model = History_of_surgery
	template = "history_of_surgery_delete.html"
	redirect_url = "history_of_surgery_list_url"
	raise_exception = True


class Blood_pressure_monitoring_ListView(ListView):
	model = Blood_pressure_monitoring
	context_object_name = "blood_pressure_monitorings"
	template_name = "blood_pressure_monitoring_list.html"


class Blood_pressure_monitoring_CreateView(SuccessMessageMixin, CreateView):
	template_name = "blood_pressure_monitoring_edit.html"
	form_class = Blood_pressure_monitoring_ModelForm
	success_message = "保存成功！"


class Blood_pressure_monitoring_DetailView(DetailView):
	model = Blood_pressure_monitoring
	context_object_name = "blood_pressure_monitoring"
	template_name = "blood_pressure_monitoring_detail.html"

	def get_object(self):
		blood_pressure_monitoring = super(Blood_pressure_monitoring_DetailView, self).get_object()
		form = Blood_pressure_monitoring_ModelForm(instance=blood_pressure_monitoring)
		return form


class Blood_pressure_monitoring_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "blood_pressure_monitoring_edit.html"
	form_class = Blood_pressure_monitoring_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Blood_pressure_monitoring.objects.all()


class Blood_pressure_monitoring_DeleteView(DeleteObjectMixin, View):
	model = Blood_pressure_monitoring
	template = "blood_pressure_monitoring_delete.html"
	redirect_url = "blood_pressure_monitoring_list_url"
	raise_exception = True


class User_registry_ListView(ListView):
	model = User_registry
	context_object_name = "user_registrys"
	template_name = "user_registry_list.html"


class User_registry_CreateView(SuccessMessageMixin, CreateView):
	template_name = "user_registry_edit.html"
	form_class = User_registry_ModelForm
	success_message = "保存成功！"


class User_registry_DetailView(DetailView):
	model = User_registry
	context_object_name = "user_registry"
	template_name = "user_registry_detail.html"

	def get_object(self):
		user_registry = super(User_registry_DetailView, self).get_object()
		form = User_registry_ModelForm(instance=user_registry)
		return form


class User_registry_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "user_registry_edit.html"
	form_class = User_registry_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return User_registry.objects.all()


class User_registry_DeleteView(DeleteObjectMixin, View):
	model = User_registry
	template = "user_registry_delete.html"
	redirect_url = "user_registry_list_url"
	raise_exception = True


class Doctor_registry_ListView(ListView):
	model = Doctor_registry
	context_object_name = "doctor_registrys"
	template_name = "doctor_registry_list.html"


class Doctor_registry_CreateView(SuccessMessageMixin, CreateView):
	template_name = "doctor_registry_edit.html"
	form_class = Doctor_registry_ModelForm
	success_message = "保存成功！"


class Doctor_registry_DetailView(DetailView):
	model = Doctor_registry
	context_object_name = "doctor_registry"
	template_name = "doctor_registry_detail.html"

	def get_object(self):
		doctor_registry = super(Doctor_registry_DetailView, self).get_object()
		form = Doctor_registry_ModelForm(instance=doctor_registry)
		return form


class Doctor_registry_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "doctor_registry_edit.html"
	form_class = Doctor_registry_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Doctor_registry.objects.all()


class Doctor_registry_DeleteView(DeleteObjectMixin, View):
	model = Doctor_registry
	template = "doctor_registry_delete.html"
	redirect_url = "doctor_registry_list_url"
	raise_exception = True


class User_login_ListView(ListView):
	model = User_login
	context_object_name = "user_logins"
	template_name = "user_login_list.html"


class User_login_CreateView(SuccessMessageMixin, CreateView):
	template_name = "user_login_edit.html"
	form_class = User_login_ModelForm
	success_message = "保存成功！"


class User_login_DetailView(DetailView):
	model = User_login
	context_object_name = "user_login"
	template_name = "user_login_detail.html"

	def get_object(self):
		user_login = super(User_login_DetailView, self).get_object()
		form = User_login_ModelForm(instance=user_login)
		return form


class User_login_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "user_login_edit.html"
	form_class = User_login_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return User_login.objects.all()


class User_login_DeleteView(DeleteObjectMixin, View):
	model = User_login
	template = "user_login_delete.html"
	redirect_url = "user_login_list_url"
	raise_exception = True


class Doctor_login_ListView(ListView):
	model = Doctor_login
	context_object_name = "doctor_logins"
	template_name = "doctor_login_list.html"


class Doctor_login_CreateView(SuccessMessageMixin, CreateView):
	template_name = "doctor_login_edit.html"
	form_class = Doctor_login_ModelForm
	success_message = "保存成功！"


class Doctor_login_DetailView(DetailView):
	model = Doctor_login
	context_object_name = "doctor_login"
	template_name = "doctor_login_detail.html"

	def get_object(self):
		doctor_login = super(Doctor_login_DetailView, self).get_object()
		form = Doctor_login_ModelForm(instance=doctor_login)
		return form


class Doctor_login_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "doctor_login_edit.html"
	form_class = Doctor_login_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Doctor_login.objects.all()


class Doctor_login_DeleteView(DeleteObjectMixin, View):
	model = Doctor_login
	template = "doctor_login_delete.html"
	redirect_url = "doctor_login_list_url"
	raise_exception = True


class Vital_signs_check_ListView(ListView):
	model = Vital_signs_check
	context_object_name = "vital_signs_checks"
	template_name = "vital_signs_check_list.html"


class Vital_signs_check_CreateView(SuccessMessageMixin, CreateView):
	template_name = "vital_signs_check_edit.html"
	form_class = Vital_signs_check_ModelForm
	success_message = "保存成功！"


class Vital_signs_check_DetailView(DetailView):
	model = Vital_signs_check
	context_object_name = "vital_signs_check"
	template_name = "vital_signs_check_detail.html"

	def get_object(self):
		vital_signs_check = super(Vital_signs_check_DetailView, self).get_object()
		form = Vital_signs_check_ModelForm(instance=vital_signs_check)
		return form


class Vital_signs_check_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "vital_signs_check_edit.html"
	form_class = Vital_signs_check_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Vital_signs_check.objects.all()


class Vital_signs_check_DeleteView(DeleteObjectMixin, View):
	model = Vital_signs_check
	template = "vital_signs_check_delete.html"
	redirect_url = "vital_signs_check_list_url"
	raise_exception = True


class Physical_examination_hearing_ListView(ListView):
	model = Physical_examination_hearing
	context_object_name = "physical_examination_hearings"
	template_name = "physical_examination_hearing_list.html"


class Physical_examination_hearing_CreateView(SuccessMessageMixin, CreateView):
	template_name = "physical_examination_hearing_edit.html"
	form_class = Physical_examination_hearing_ModelForm
	success_message = "保存成功！"


class Physical_examination_hearing_DetailView(DetailView):
	model = Physical_examination_hearing
	context_object_name = "physical_examination_hearing"
	template_name = "physical_examination_hearing_detail.html"

	def get_object(self):
		physical_examination_hearing = super(Physical_examination_hearing_DetailView, self).get_object()
		form = Physical_examination_hearing_ModelForm(instance=physical_examination_hearing)
		return form


class Physical_examination_hearing_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "physical_examination_hearing_edit.html"
	form_class = Physical_examination_hearing_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Physical_examination_hearing.objects.all()


class Physical_examination_hearing_DeleteView(DeleteObjectMixin, View):
	model = Physical_examination_hearing
	template = "physical_examination_hearing_delete.html"
	redirect_url = "physical_examination_hearing_list_url"
	raise_exception = True


class Basic_personal_information_ListView(ListView):
	model = Basic_personal_information
	context_object_name = "basic_personal_informations"
	template_name = "basic_personal_information_list.html"


class Basic_personal_information_CreateView(SuccessMessageMixin, CreateView):
	template_name = "basic_personal_information_edit.html"
	form_class = Basic_personal_information_ModelForm
	success_message = "保存成功！"


class Basic_personal_information_DetailView(DetailView):
	model = Basic_personal_information
	context_object_name = "basic_personal_information"
	template_name = "basic_personal_information_detail.html"

	def get_object(self):
		basic_personal_information = super(Basic_personal_information_DetailView, self).get_object()
		form = Basic_personal_information_ModelForm(instance=basic_personal_information)
		return form


class Basic_personal_information_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "basic_personal_information_edit.html"
	form_class = Basic_personal_information_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Basic_personal_information.objects.all()


class Basic_personal_information_DeleteView(DeleteObjectMixin, View):
	model = Basic_personal_information
	template = "basic_personal_information_delete.html"
	redirect_url = "basic_personal_information_list_url"
	raise_exception = True


class History_of_infectious_diseases_ListView(ListView):
	model = History_of_infectious_diseases
	context_object_name = "history_of_infectious_diseasess"
	template_name = "history_of_infectious_diseases_list.html"


class History_of_infectious_diseases_CreateView(SuccessMessageMixin, CreateView):
	template_name = "history_of_infectious_diseases_edit.html"
	form_class = History_of_infectious_diseases_ModelForm
	success_message = "保存成功！"


class History_of_infectious_diseases_DetailView(DetailView):
	model = History_of_infectious_diseases
	context_object_name = "history_of_infectious_diseases"
	template_name = "history_of_infectious_diseases_detail.html"

	def get_object(self):
		history_of_infectious_diseases = super(History_of_infectious_diseases_DetailView, self).get_object()
		form = History_of_infectious_diseases_ModelForm(instance=history_of_infectious_diseases)
		return form


class History_of_infectious_diseases_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "history_of_infectious_diseases_edit.html"
	form_class = History_of_infectious_diseases_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return History_of_infectious_diseases.objects.all()


class History_of_infectious_diseases_DeleteView(DeleteObjectMixin, View):
	model = History_of_infectious_diseases
	template = "history_of_infectious_diseases_delete.html"
	redirect_url = "history_of_infectious_diseases_list_url"
	raise_exception = True


class Physical_examination_ListView(ListView):
	model = Physical_examination
	context_object_name = "physical_examinations"
	template_name = "physical_examination_list.html"


class Physical_examination_CreateView(SuccessMessageMixin, CreateView):
	template_name = "physical_examination_edit.html"
	form_class = Physical_examination_ModelForm
	success_message = "保存成功！"


class Physical_examination_DetailView(DetailView):
	model = Physical_examination
	context_object_name = "physical_examination"
	template_name = "physical_examination_detail.html"

	def get_object(self):
		physical_examination = super(Physical_examination_DetailView, self).get_object()
		form = Physical_examination_ModelForm(instance=physical_examination)
		return form


class Physical_examination_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "physical_examination_edit.html"
	form_class = Physical_examination_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Physical_examination.objects.all()


class Physical_examination_DeleteView(DeleteObjectMixin, View):
	model = Physical_examination
	template = "physical_examination_delete.html"
	redirect_url = "physical_examination_list_url"
	raise_exception = True


class Personal_adaptability_assessment_ListView(ListView):
	model = Personal_adaptability_assessment
	context_object_name = "personal_adaptability_assessments"
	template_name = "personal_adaptability_assessment_list.html"


class Personal_adaptability_assessment_CreateView(SuccessMessageMixin, CreateView):
	template_name = "personal_adaptability_assessment_edit.html"
	form_class = Personal_adaptability_assessment_ModelForm
	success_message = "保存成功！"


class Personal_adaptability_assessment_DetailView(DetailView):
	model = Personal_adaptability_assessment
	context_object_name = "personal_adaptability_assessment"
	template_name = "personal_adaptability_assessment_detail.html"

	def get_object(self):
		personal_adaptability_assessment = super(Personal_adaptability_assessment_DetailView, self).get_object()
		form = Personal_adaptability_assessment_ModelForm(instance=personal_adaptability_assessment)
		return form


class Personal_adaptability_assessment_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "personal_adaptability_assessment_edit.html"
	form_class = Personal_adaptability_assessment_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Personal_adaptability_assessment.objects.all()


class Personal_adaptability_assessment_DeleteView(DeleteObjectMixin, View):
	model = Personal_adaptability_assessment
	template = "personal_adaptability_assessment_delete.html"
	redirect_url = "personal_adaptability_assessment_list_url"
	raise_exception = True


class Physical_examination_abdomen_ListView(ListView):
	model = Physical_examination_abdomen
	context_object_name = "physical_examination_abdomens"
	template_name = "physical_examination_abdomen_list.html"


class Physical_examination_abdomen_CreateView(SuccessMessageMixin, CreateView):
	template_name = "physical_examination_abdomen_edit.html"
	form_class = Physical_examination_abdomen_ModelForm
	success_message = "保存成功！"


class Physical_examination_abdomen_DetailView(DetailView):
	model = Physical_examination_abdomen
	context_object_name = "physical_examination_abdomen"
	template_name = "physical_examination_abdomen_detail.html"

	def get_object(self):
		physical_examination_abdomen = super(Physical_examination_abdomen_DetailView, self).get_object()
		form = Physical_examination_abdomen_ModelForm(instance=physical_examination_abdomen)
		return form


class Physical_examination_abdomen_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "physical_examination_abdomen_edit.html"
	form_class = Physical_examination_abdomen_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Physical_examination_abdomen.objects.all()


class Physical_examination_abdomen_DeleteView(DeleteObjectMixin, View):
	model = Physical_examination_abdomen
	template = "physical_examination_abdomen_delete.html"
	redirect_url = "physical_examination_abdomen_list_url"
	raise_exception = True


class Physical_examination_athletic_ability_ListView(ListView):
	model = Physical_examination_athletic_ability
	context_object_name = "physical_examination_athletic_abilitys"
	template_name = "physical_examination_athletic_ability_list.html"


class Physical_examination_athletic_ability_CreateView(SuccessMessageMixin, CreateView):
	template_name = "physical_examination_athletic_ability_edit.html"
	form_class = Physical_examination_athletic_ability_ModelForm
	success_message = "保存成功！"


class Physical_examination_athletic_ability_DetailView(DetailView):
	model = Physical_examination_athletic_ability
	context_object_name = "physical_examination_athletic_ability"
	template_name = "physical_examination_athletic_ability_detail.html"

	def get_object(self):
		physical_examination_athletic_ability = super(Physical_examination_athletic_ability_DetailView, self).get_object()
		form = Physical_examination_athletic_ability_ModelForm(instance=physical_examination_athletic_ability)
		return form


class Physical_examination_athletic_ability_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "physical_examination_athletic_ability_edit.html"
	form_class = Physical_examination_athletic_ability_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Physical_examination_athletic_ability.objects.all()


class Physical_examination_athletic_ability_DeleteView(DeleteObjectMixin, View):
	model = Physical_examination_athletic_ability
	template = "physical_examination_athletic_ability_delete.html"
	redirect_url = "physical_examination_athletic_ability_list_url"
	raise_exception = True


class Physical_examination_oral_cavity_ListView(ListView):
	model = Physical_examination_oral_cavity
	context_object_name = "physical_examination_oral_cavitys"
	template_name = "physical_examination_oral_cavity_list.html"


class Physical_examination_oral_cavity_CreateView(SuccessMessageMixin, CreateView):
	template_name = "physical_examination_oral_cavity_edit.html"
	form_class = Physical_examination_oral_cavity_ModelForm
	success_message = "保存成功！"


class Physical_examination_oral_cavity_DetailView(DetailView):
	model = Physical_examination_oral_cavity
	context_object_name = "physical_examination_oral_cavity"
	template_name = "physical_examination_oral_cavity_detail.html"

	def get_object(self):
		physical_examination_oral_cavity = super(Physical_examination_oral_cavity_DetailView, self).get_object()
		form = Physical_examination_oral_cavity_ModelForm(instance=physical_examination_oral_cavity)
		return form


class Physical_examination_oral_cavity_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "physical_examination_oral_cavity_edit.html"
	form_class = Physical_examination_oral_cavity_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Physical_examination_oral_cavity.objects.all()


class Physical_examination_oral_cavity_DeleteView(DeleteObjectMixin, View):
	model = Physical_examination_oral_cavity
	template = "physical_examination_oral_cavity_delete.html"
	redirect_url = "physical_examination_oral_cavity_list_url"
	raise_exception = True


class Physical_examination_lungs_ListView(ListView):
	model = Physical_examination_lungs
	context_object_name = "physical_examination_lungss"
	template_name = "physical_examination_lungs_list.html"


class Physical_examination_lungs_CreateView(SuccessMessageMixin, CreateView):
	template_name = "physical_examination_lungs_edit.html"
	form_class = Physical_examination_lungs_ModelForm
	success_message = "保存成功！"


class Physical_examination_lungs_DetailView(DetailView):
	model = Physical_examination_lungs
	context_object_name = "physical_examination_lungs"
	template_name = "physical_examination_lungs_detail.html"

	def get_object(self):
		physical_examination_lungs = super(Physical_examination_lungs_DetailView, self).get_object()
		form = Physical_examination_lungs_ModelForm(instance=physical_examination_lungs)
		return form


class Physical_examination_lungs_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "physical_examination_lungs_edit.html"
	form_class = Physical_examination_lungs_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Physical_examination_lungs.objects.all()


class Physical_examination_lungs_DeleteView(DeleteObjectMixin, View):
	model = Physical_examination_lungs
	template = "physical_examination_lungs_delete.html"
	redirect_url = "physical_examination_lungs_list_url"
	raise_exception = True


class Physical_examination_limbs_ListView(ListView):
	model = Physical_examination_limbs
	context_object_name = "physical_examination_limbss"
	template_name = "physical_examination_limbs_list.html"


class Physical_examination_limbs_CreateView(SuccessMessageMixin, CreateView):
	template_name = "physical_examination_limbs_edit.html"
	form_class = Physical_examination_limbs_ModelForm
	success_message = "保存成功！"


class Physical_examination_limbs_DetailView(DetailView):
	model = Physical_examination_limbs
	context_object_name = "physical_examination_limbs"
	template_name = "physical_examination_limbs_detail.html"

	def get_object(self):
		physical_examination_limbs = super(Physical_examination_limbs_DetailView, self).get_object()
		form = Physical_examination_limbs_ModelForm(instance=physical_examination_limbs)
		return form


class Physical_examination_limbs_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "physical_examination_limbs_edit.html"
	form_class = Physical_examination_limbs_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Physical_examination_limbs.objects.all()


class Physical_examination_limbs_DeleteView(DeleteObjectMixin, View):
	model = Physical_examination_limbs
	template = "physical_examination_limbs_delete.html"
	redirect_url = "physical_examination_limbs_list_url"
	raise_exception = True


class Physical_examination_skin_ListView(ListView):
	model = Physical_examination_skin
	context_object_name = "physical_examination_skins"
	template_name = "physical_examination_skin_list.html"


class Physical_examination_skin_CreateView(SuccessMessageMixin, CreateView):
	template_name = "physical_examination_skin_edit.html"
	form_class = Physical_examination_skin_ModelForm
	success_message = "保存成功！"


class Physical_examination_skin_DetailView(DetailView):
	model = Physical_examination_skin
	context_object_name = "physical_examination_skin"
	template_name = "physical_examination_skin_detail.html"

	def get_object(self):
		physical_examination_skin = super(Physical_examination_skin_DetailView, self).get_object()
		form = Physical_examination_skin_ModelForm(instance=physical_examination_skin)
		return form


class Physical_examination_skin_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "physical_examination_skin_edit.html"
	form_class = Physical_examination_skin_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Physical_examination_skin.objects.all()


class Physical_examination_skin_DeleteView(DeleteObjectMixin, View):
	model = Physical_examination_skin
	template = "physical_examination_skin_delete.html"
	redirect_url = "physical_examination_skin_list_url"
	raise_exception = True


class Physical_examination_sclera_ListView(ListView):
	model = Physical_examination_sclera
	context_object_name = "physical_examination_scleras"
	template_name = "physical_examination_sclera_list.html"


class Physical_examination_sclera_CreateView(SuccessMessageMixin, CreateView):
	template_name = "physical_examination_sclera_edit.html"
	form_class = Physical_examination_sclera_ModelForm
	success_message = "保存成功！"


class Physical_examination_sclera_DetailView(DetailView):
	model = Physical_examination_sclera
	context_object_name = "physical_examination_sclera"
	template_name = "physical_examination_sclera_detail.html"

	def get_object(self):
		physical_examination_sclera = super(Physical_examination_sclera_DetailView, self).get_object()
		form = Physical_examination_sclera_ModelForm(instance=physical_examination_sclera)
		return form


class Physical_examination_sclera_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "physical_examination_sclera_edit.html"
	form_class = Physical_examination_sclera_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Physical_examination_sclera.objects.all()


class Physical_examination_sclera_DeleteView(DeleteObjectMixin, View):
	model = Physical_examination_sclera
	template = "physical_examination_sclera_delete.html"
	redirect_url = "physical_examination_sclera_list_url"
	raise_exception = True


class Physical_examination_lymph_nodes_ListView(ListView):
	model = Physical_examination_lymph_nodes
	context_object_name = "physical_examination_lymph_nodess"
	template_name = "physical_examination_lymph_nodes_list.html"


class Physical_examination_lymph_nodes_CreateView(SuccessMessageMixin, CreateView):
	template_name = "physical_examination_lymph_nodes_edit.html"
	form_class = Physical_examination_lymph_nodes_ModelForm
	success_message = "保存成功！"


class Physical_examination_lymph_nodes_DetailView(DetailView):
	model = Physical_examination_lymph_nodes
	context_object_name = "physical_examination_lymph_nodes"
	template_name = "physical_examination_lymph_nodes_detail.html"

	def get_object(self):
		physical_examination_lymph_nodes = super(Physical_examination_lymph_nodes_DetailView, self).get_object()
		form = Physical_examination_lymph_nodes_ModelForm(instance=physical_examination_lymph_nodes)
		return form


class Physical_examination_lymph_nodes_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "physical_examination_lymph_nodes_edit.html"
	form_class = Physical_examination_lymph_nodes_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Physical_examination_lymph_nodes.objects.all()


class Physical_examination_lymph_nodes_DeleteView(DeleteObjectMixin, View):
	model = Physical_examination_lymph_nodes
	template = "physical_examination_lymph_nodes_delete.html"
	redirect_url = "physical_examination_lymph_nodes_list_url"
	raise_exception = True


class Physical_examination_spine_ListView(ListView):
	model = Physical_examination_spine
	context_object_name = "physical_examination_spines"
	template_name = "physical_examination_spine_list.html"


class Physical_examination_spine_CreateView(SuccessMessageMixin, CreateView):
	template_name = "physical_examination_spine_edit.html"
	form_class = Physical_examination_spine_ModelForm
	success_message = "保存成功！"


class Physical_examination_spine_DetailView(DetailView):
	model = Physical_examination_spine
	context_object_name = "physical_examination_spine"
	template_name = "physical_examination_spine_detail.html"

	def get_object(self):
		physical_examination_spine = super(Physical_examination_spine_DetailView, self).get_object()
		form = Physical_examination_spine_ModelForm(instance=physical_examination_spine)
		return form


class Physical_examination_spine_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "physical_examination_spine_edit.html"
	form_class = Physical_examination_spine_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Physical_examination_spine.objects.all()


class Physical_examination_spine_DeleteView(DeleteObjectMixin, View):
	model = Physical_examination_spine
	template = "physical_examination_spine_delete.html"
	redirect_url = "physical_examination_spine_list_url"
	raise_exception = True


class Physical_examination_diabetes_ListView(ListView):
	model = Physical_examination_diabetes
	context_object_name = "physical_examination_diabetess"
	template_name = "physical_examination_diabetes_list.html"


class Physical_examination_diabetes_CreateView(SuccessMessageMixin, CreateView):
	template_name = "physical_examination_diabetes_edit.html"
	form_class = Physical_examination_diabetes_ModelForm
	success_message = "保存成功！"


class Physical_examination_diabetes_DetailView(DetailView):
	model = Physical_examination_diabetes
	context_object_name = "physical_examination_diabetes"
	template_name = "physical_examination_diabetes_detail.html"

	def get_object(self):
		physical_examination_diabetes = super(Physical_examination_diabetes_DetailView, self).get_object()
		form = Physical_examination_diabetes_ModelForm(instance=physical_examination_diabetes)
		return form


class Physical_examination_diabetes_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "physical_examination_diabetes_edit.html"
	form_class = Physical_examination_diabetes_ModelForm
	success_url = "/"
	success_message = "保存成功！"

	def get_queryset(self):
		return Physical_examination_diabetes.objects.all()


class Physical_examination_diabetes_DeleteView(DeleteObjectMixin, View):
	model = Physical_examination_diabetes
	template = "physical_examination_diabetes_delete.html"
	redirect_url = "physical_examination_diabetes_list_url"
	raise_exception = True