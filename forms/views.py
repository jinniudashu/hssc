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


class Metadata_follow_up_form_ListView(ListView):
	context_object_name = "metadata_follow_up_forms"
	template_name = "metadata_follow_up_form_list.html"

	def get_queryset(self):
		return Metadata_follow_up_form.objects.all()


class Metadata_follow_up_form_CreateView(SuccessMessageMixin, CreateView):
	template_name = "metadata_follow_up_form_edit.html"
	form_class = Metadata_follow_up_form_ModelForm
	success_message = "保存成功！"


class Metadata_follow_up_form_DetailView(DetailView):
	model = Metadata_follow_up_form
	context_object_name = "metadata_follow_up_form"
	template_name = "metadata_follow_up_form_detail.html"

	def get_object(self):
		metadata_follow_up_form = super(Metadata_follow_up_form_DetailView, self).get_object()
		form = Metadata_follow_up_form_ModelForm(instance=metadata_follow_up_form)
		return form


class Metadata_follow_up_form_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "metadata_follow_up_form_edit.html"
	form_class = Metadata_follow_up_form_ModelForm
	success_message = "保存成功！"

	def get_queryset(self):
		return Metadata_follow_up_form.objects.all()


class Metadata_follow_up_form_DeleteView(DeleteObjectMixin, View):
	model = Metadata_follow_up_form
	template = "metadata_follow_up_form_delete.html"
	redirect_url = "metadata_follow_up_form_list_url"
	raise_exception = True


class Classification_checklist_ListView(ListView):
	context_object_name = "classification_checklists"
	template_name = "classification_checklist_list.html"

	def get_queryset(self):
		return Classification_checklist.objects.all()


class Classification_checklist_CreateView(SuccessMessageMixin, CreateView):
	template_name = "classification_checklist_edit.html"
	form_class = Classification_checklist_ModelForm
	success_message = "保存成功！"


class Classification_checklist_DetailView(DetailView):
	model = Classification_checklist
	context_object_name = "classification_checklist"
	template_name = "classification_checklist_detail.html"

	def get_object(self):
		classification_checklist = super(Classification_checklist_DetailView, self).get_object()
		form = Classification_checklist_ModelForm(instance=classification_checklist)
		return form


class Classification_checklist_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "classification_checklist_edit.html"
	form_class = Classification_checklist_ModelForm
	success_message = "保存成功！"

	def get_queryset(self):
		return Classification_checklist.objects.all()


class Classification_checklist_DeleteView(DeleteObjectMixin, View):
	model = Classification_checklist
	template = "classification_checklist_delete.html"
	redirect_url = "classification_checklist_list_url"
	raise_exception = True


class Routine_physical_examination_ListView(ListView):
	context_object_name = "routine_physical_examinations"
	template_name = "routine_physical_examination_list.html"

	def get_queryset(self):
		return Routine_physical_examination.objects.all()


class Routine_physical_examination_CreateView(SuccessMessageMixin, CreateView):
	template_name = "routine_physical_examination_edit.html"
	form_class = Routine_physical_examination_ModelForm
	success_message = "保存成功！"


class Routine_physical_examination_DetailView(DetailView):
	model = Routine_physical_examination
	context_object_name = "routine_physical_examination"
	template_name = "routine_physical_examination_detail.html"

	def get_object(self):
		routine_physical_examination = super(Routine_physical_examination_DetailView, self).get_object()
		form = Routine_physical_examination_ModelForm(instance=routine_physical_examination)
		return form


class Routine_physical_examination_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "routine_physical_examination_edit.html"
	form_class = Routine_physical_examination_ModelForm
	success_message = "保存成功！"

	def get_queryset(self):
		return Routine_physical_examination.objects.all()


class Routine_physical_examination_DeleteView(DeleteObjectMixin, View):
	model = Routine_physical_examination
	template = "routine_physical_examination_delete.html"
	redirect_url = "routine_physical_examination_list_url"
	raise_exception = True


class Classification_survey_list_ListView(ListView):
	context_object_name = "classification_survey_lists"
	template_name = "classification_survey_list_list.html"

	def get_queryset(self):
		return Classification_survey_list.objects.all()


class Classification_survey_list_CreateView(SuccessMessageMixin, CreateView):
	template_name = "classification_survey_list_edit.html"
	form_class = Classification_survey_list_ModelForm
	success_message = "保存成功！"


class Classification_survey_list_DetailView(DetailView):
	model = Classification_survey_list
	context_object_name = "classification_survey_list"
	template_name = "classification_survey_list_detail.html"

	def get_object(self):
		classification_survey_list = super(Classification_survey_list_DetailView, self).get_object()
		form = Classification_survey_list_ModelForm(instance=classification_survey_list)
		return form


class Classification_survey_list_UpdateView(SuccessMessageMixin, UpdateView):
	template_name = "classification_survey_list_edit.html"
	form_class = Classification_survey_list_ModelForm
	success_message = "保存成功！"

	def get_queryset(self):
		return Classification_survey_list.objects.all()


class Classification_survey_list_DeleteView(DeleteObjectMixin, View):
	model = Classification_survey_list
	template = "classification_survey_list_delete.html"
	redirect_url = "classification_survey_list_list_url"
	raise_exception = True