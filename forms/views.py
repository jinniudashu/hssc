from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin

from .utils import DetailObjectMixin, CreateObjectMixin, UpdateObjectMixin, DeleteObjectMixin

from .models import *
from .forms import *

# class TestDetailView(DetailView):
# 	a = 'a'
# 	def get_object(self):
# 		slug = self.kwargs.get('slug')
# 		return get_object_or_404(Test, slug=slug)

def index_view(request):
	return render(request, 'index.html')


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


class Family_history_ListView(ListView):
	context_object_name = "family_historys"
	template_name = "family_history_list.html"

	def get_queryset(self):
		return Family_history.objects.all()


class Family_history_CreateView(SuccessMessageMixin, CreateView):
	template_name = "family_history_edit.html"
	form_class = Family_history_ModelForm
	success_message = "保存成功！"


class Family_history_DetailView(DetailView):
	model = Family_history
	context_object_name = "family_history"
	template_name = "family_history_detail.html"

	def get_object(self):
		family_history = super(Family_history_DetailView, self).get_object()
		form = Family_history_ModelForm(instance=family_history)
		return form


class Family_history_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "family_history_edit.html"
	form_class = Family_history_ModelForm
	success_message = "保存成功！"

	def get_queryset(self):
		return Family_history.objects.all()


class Family_history_DeleteView(DeleteObjectMixin, View):
	model = Family_history
	template = "family_history_delete.html"
	redirect_url = "family_history_list_url"
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