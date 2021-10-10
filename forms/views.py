from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, resolve_url
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
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

def index_view(request):
	# user = []
	procs = Operation_proc.objects.exclude(state=4)
	todos = []
	for proc in procs:
		todo = {}
		todo['operation'] = proc.operation.label
		todo['url'] = f'{proc.operation.name}_update_url'
		todo['slug'] = proc.entry
		todos.append(todo)

	context = {"todos": todos}
	return render(request, 'index.html', context)


class History_of_trauma_ListView(ListView):
	context_object_name = "history_of_traumas"
	template_name = "history_of_trauma_list.html"

	def get_queryset(self):
		return History_of_trauma.objects.all()


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
	success_message = "保存成功！"

	def get_queryset(self):
		return History_of_trauma.objects.all()


class History_of_trauma_DeleteView(DeleteObjectMixin, View):
	model = History_of_trauma
	template = "history_of_trauma_delete.html"
	redirect_url = "history_of_trauma_list_url"
	raise_exception = True


class Out_of_hospital_self_report_survey_ListView(ListView):
	context_object_name = "out_of_hospital_self_report_surveys"
	template_name = "out_of_hospital_self_report_survey_list.html"

	def get_queryset(self):
		return Out_of_hospital_self_report_survey.objects.all()


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
	success_message = "保存成功！"

	def get_queryset(self):
		return Out_of_hospital_self_report_survey.objects.all()
	

class Out_of_hospital_self_report_survey_DeleteView(DeleteObjectMixin, View):
	model = Out_of_hospital_self_report_survey
	template = "out_of_hospital_self_report_survey_delete.html"
	redirect_url = "out_of_hospital_self_report_survey_list_url"
	raise_exception = True


class Personal_comprehensive_psychological_quality_survey_ListView(ListView):
	context_object_name = "personal_comprehensive_psychological_quality_surveys"
	template_name = "personal_comprehensive_psychological_quality_survey_list.html"

	def get_queryset(self):
		return Personal_comprehensive_psychological_quality_survey.objects.all()


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
	success_message = "保存成功！"

	def get_queryset(self):
		return Personal_comprehensive_psychological_quality_survey.objects.all()


class Personal_comprehensive_psychological_quality_survey_DeleteView(DeleteObjectMixin, View):
	model = Personal_comprehensive_psychological_quality_survey
	template = "personal_comprehensive_psychological_quality_survey_delete.html"
	redirect_url = "personal_comprehensive_psychological_quality_survey_list_url"
	raise_exception = True


class Personal_health_assessment_ListView(ListView):
	context_object_name = "personal_health_assessments"
	template_name = "personal_health_assessment_list.html"

	def get_queryset(self):
		return Personal_health_assessment.objects.all()


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
	success_message = "保存成功！"

	def get_queryset(self):
		return Personal_health_assessment.objects.all()


class Personal_health_assessment_DeleteView(DeleteObjectMixin, View):
	model = Personal_health_assessment
	template = "personal_health_assessment_delete.html"
	redirect_url = "personal_health_assessment_list_url"
	raise_exception = True


class Allergies_history_ListView(ListView):
	context_object_name = "allergies_historys"
	template_name = "allergies_history_list.html"

	def get_queryset(self):
		return Allergies_history.objects.all()


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
	success_message = "保存成功！"

	def get_queryset(self):
		return Allergies_history.objects.all()


class Allergies_history_DeleteView(DeleteObjectMixin, View):
	model = Allergies_history
	template = "allergies_history_delete.html"
	redirect_url = "allergies_history_list_url"
	raise_exception = True


class Personal_health_behavior_survey_ListView(ListView):
	context_object_name = "personal_health_behavior_surveys"
	template_name = "personal_health_behavior_survey_list.html"

	def get_queryset(self):
		return Personal_health_behavior_survey.objects.all()


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
	success_message = "保存成功！"

	def get_queryset(self):
		return Personal_health_behavior_survey.objects.all()


class Personal_health_behavior_survey_DeleteView(DeleteObjectMixin, View):
	model = Personal_health_behavior_survey
	template = "personal_health_behavior_survey_delete.html"
	redirect_url = "personal_health_behavior_survey_list_url"
	raise_exception = True


class History_of_blood_transfusion_ListView(ListView):
	context_object_name = "history_of_blood_transfusions"
	template_name = "history_of_blood_transfusion_list.html"

	def get_queryset(self):
		return History_of_blood_transfusion.objects.all()


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
	success_message = "保存成功！"

	def get_queryset(self):
		return History_of_blood_transfusion.objects.all()


class History_of_blood_transfusion_DeleteView(DeleteObjectMixin, View):
	model = History_of_blood_transfusion
	template = "history_of_blood_transfusion_delete.html"
	redirect_url = "history_of_blood_transfusion_list_url"
	raise_exception = True


class Social_environment_assessment_ListView(ListView):
	context_object_name = "social_environment_assessments"
	template_name = "social_environment_assessment_list.html"

	def get_queryset(self):
		return Social_environment_assessment.objects.all()


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
	success_message = "保存成功！"

	def get_queryset(self):
		return Social_environment_assessment.objects.all()


class Social_environment_assessment_DeleteView(DeleteObjectMixin, View):
	model = Social_environment_assessment
	template = "social_environment_assessment_delete.html"
	redirect_url = "social_environment_assessment_list_url"
	raise_exception = True


class Medical_history_ListView(ListView):
	context_object_name = "medical_historys"
	template_name = "medical_history_list.html"

	def get_queryset(self):
		return Medical_history.objects.all()


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
	success_message = "保存成功！"

	def get_queryset(self):
		return Medical_history.objects.all()


class Medical_history_DeleteView(DeleteObjectMixin, View):
	model = Medical_history
	template = "medical_history_delete.html"
	redirect_url = "medical_history_list_url"
	raise_exception = True


class Major_life_events_ListView(ListView):
	context_object_name = "major_life_eventss"
	template_name = "major_life_events_list.html"

	def get_queryset(self):
		return Major_life_events.objects.all()


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
	success_message = "保存成功！"

	def get_queryset(self):
		return Major_life_events.objects.all()


class Major_life_events_DeleteView(DeleteObjectMixin, View):
	model = Major_life_events
	template = "major_life_events_delete.html"
	redirect_url = "major_life_events_list_url"
	raise_exception = True


class Family_survey_ListView(ListView):
	context_object_name = "family_surveys"
	template_name = "family_survey_list.html"

	def get_queryset(self):
		return Family_survey.objects.all()


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
	success_message = "保存成功！"

	def get_queryset(self):
		return Family_survey.objects.all()


class Family_survey_DeleteView(DeleteObjectMixin, View):
	model = Family_survey
	template = "family_survey_delete.html"
	redirect_url = "family_survey_list_url"
	raise_exception = True


class History_of_surgery_ListView(ListView):
	context_object_name = "history_of_surgerys"
	template_name = "history_of_surgery_list.html"

	def get_queryset(self):
		return History_of_surgery.objects.all()


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
	success_message = "保存成功！"

	def get_queryset(self):
		return History_of_surgery.objects.all()


class History_of_surgery_DeleteView(DeleteObjectMixin, View):
	model = History_of_surgery
	template = "history_of_surgery_delete.html"
	redirect_url = "history_of_surgery_list_url"
	raise_exception = True


class User_registry_ListView(ListView):
	context_object_name = "user_registrys"
	template_name = "user_registry_list.html"

	def get_queryset(self):
		return User_registry.objects.all()


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
	success_message = "保存成功！"

	def get_queryset(self):
		return User_registry.objects.all()


class User_registry_DeleteView(DeleteObjectMixin, View):
	model = User_registry
	template = "user_registry_delete.html"
	redirect_url = "user_registry_list_url"
	raise_exception = True


class Doctor_registry_ListView(ListView):
	context_object_name = "doctor_registrys"
	template_name = "doctor_registry_list.html"

	def get_queryset(self):
		return Doctor_registry.objects.all()


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
	success_message = "保存成功！"

	def get_queryset(self):
		return Doctor_registry.objects.all()


class Doctor_registry_DeleteView(DeleteObjectMixin, View):
	model = Doctor_registry
	template = "doctor_registry_delete.html"
	redirect_url = "doctor_registry_list_url"
	raise_exception = True


class User_login_ListView(ListView):
	context_object_name = "user_logins"
	template_name = "user_login_list.html"

	def get_queryset(self):
		return User_login.objects.all()


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
	success_message = "保存成功！"

	def get_queryset(self):
		return User_login.objects.all()


class User_login_DeleteView(DeleteObjectMixin, View):
	model = User_login
	template = "user_login_delete.html"
	redirect_url = "user_login_list_url"
	raise_exception = True


class Doctor_login_ListView(ListView):
	context_object_name = "doctor_logins"
	template_name = "doctor_login_list.html"

	def get_queryset(self):
		return Doctor_login.objects.all()


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
	success_message = "保存成功！"

	def get_queryset(self):
		return Doctor_login.objects.all()


class Doctor_login_DeleteView(DeleteObjectMixin, View):
	model = Doctor_login
	template = "doctor_login_delete.html"
	redirect_url = "doctor_login_list_url"
	raise_exception = True


class Basic_personal_information_ListView(ListView):
	context_object_name = "basic_personal_informations"
	template_name = "basic_personal_information_list.html"

	def get_queryset(self):
		return Basic_personal_information.objects.all()


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
	success_message = "保存成功！"

	def get_queryset(self):
		return Basic_personal_information.objects.all()


class Basic_personal_information_DeleteView(DeleteObjectMixin, View):
	model = Basic_personal_information
	template = "basic_personal_information_delete.html"
	redirect_url = "basic_personal_information_list_url"
	raise_exception = True


class History_of_infectious_diseases_ListView(ListView):
	context_object_name = "history_of_infectious_diseasess"
	template_name = "history_of_infectious_diseases_list.html"

	def get_queryset(self):
		return History_of_infectious_diseases.objects.all()


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
	success_message = "保存成功！"

	def get_queryset(self):
		return History_of_infectious_diseases.objects.all()


class History_of_infectious_diseases_DeleteView(DeleteObjectMixin, View):
	model = History_of_infectious_diseases
	template = "history_of_infectious_diseases_delete.html"
	redirect_url = "history_of_infectious_diseases_list_url"
	raise_exception = True


class Personal_adaptability_assessment_ListView(ListView):
	context_object_name = "personal_adaptability_assessments"
	template_name = "personal_adaptability_assessment_list.html"

	def get_queryset(self):
		return Personal_adaptability_assessment.objects.all()


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
	success_message = "保存成功！"

	def get_queryset(self):
		return Personal_adaptability_assessment.objects.all()


class Personal_adaptability_assessment_DeleteView(DeleteObjectMixin, View):
	model = Personal_adaptability_assessment
	template = "personal_adaptability_assessment_delete.html"
	redirect_url = "personal_adaptability_assessment_list_url"
	raise_exception = True