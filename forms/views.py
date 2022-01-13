from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.forms import modelformset_factory, inlineformset_factory
import json

from core.models import Operation_proc, Staff, Customer
from core.signals import operand_finished

from django.contrib.messages.views import SuccessMessageMixin
from forms.utils import *

from forms.models import *
from forms.forms import *

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
			todo['proc_id'] = proc.id
			todos.append(todo)
		context = super().get_context_data(**kwargs)
		context['todos'] = todos
		return context


def test1_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    context = {}
    
    # inquire_forms
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        dorsal_artery_pulsation_examination = Dorsal_artery_pulsation_examination_baseform_ModelForm(request.POST, prefix="dorsal_artery_pulsation_examination")
        history_of_infectious_diseases = History_of_infectious_diseases_baseform_ModelForm(request.POST, prefix="history_of_infectious_diseases")
        basic_personal_information = Basic_personal_information_baseform_ModelForm(request.POST, prefix="basic_personal_information")
        if dorsal_artery_pulsation_examination.is_valid() and history_of_infectious_diseases.is_valid() and basic_personal_information.is_valid():
            dorsal_artery_pulsation_examination.save()
            history_of_infectious_diseases.save()
            basic_personal_information.save()
            return redirect(reverse('index'))
    else:
        dorsal_artery_pulsation_examination = Dorsal_artery_pulsation_examination_baseform_ModelForm(prefix="dorsal_artery_pulsation_examination")
        history_of_infectious_diseases = History_of_infectious_diseases_baseform_ModelForm(prefix="history_of_infectious_diseases")
        basic_personal_information = Basic_personal_information_baseform_ModelForm(prefix="basic_personal_information")
    # context
    context['dorsal_artery_pulsation_examination'] = dorsal_artery_pulsation_examination
    context['history_of_infectious_diseases'] = history_of_infectious_diseases
    context['basic_personal_information'] = basic_personal_information
    return render(request, 'test1_create.html', context)

    


def test1_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    context = {}
    
    proc_dorsal_artery_pulsation_examination = Dorsal_artery_pulsation_examination.objects.get(pid=operation_proc)
    proc_history_of_infectious_diseases = History_of_infectious_diseases.objects.get(pid=operation_proc)
    proc_basic_personal_information = Basic_personal_information.objects.get(pid=operation_proc)
    # inquire_forms
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        dorsal_artery_pulsation_examination = Dorsal_artery_pulsation_examination_baseform_ModelForm(instance=proc_dorsal_artery_pulsation_examination, data=request.POST, prefix="dorsal_artery_pulsation_examination")
        history_of_infectious_diseases = History_of_infectious_diseases_baseform_ModelForm(instance=proc_history_of_infectious_diseases, data=request.POST, prefix="history_of_infectious_diseases")
        basic_personal_information = Basic_personal_information_baseform_ModelForm(instance=proc_basic_personal_information, data=request.POST, prefix="basic_personal_information")
        if dorsal_artery_pulsation_examination.is_valid() and history_of_infectious_diseases.is_valid() and basic_personal_information.is_valid():
            dorsal_artery_pulsation_examination.save()
            history_of_infectious_diseases.save()
            basic_personal_information.save()
            # 构造作业完成消息参数
            post_fields = request.POST.dict()
            post_fields.pop('csrfmiddlewaretoken')
            operand_finished.send(sender=test1_update, pid=kwargs['id'], ocode='rtc', field_values=post_fields)
            return redirect(reverse('index'))
    else:
        dorsal_artery_pulsation_examination = Dorsal_artery_pulsation_examination_baseform_ModelForm(instance=proc_dorsal_artery_pulsation_examination, prefix="dorsal_artery_pulsation_examination")
        history_of_infectious_diseases = History_of_infectious_diseases_baseform_ModelForm(instance=proc_history_of_infectious_diseases, prefix="history_of_infectious_diseases")
        basic_personal_information = Basic_personal_information_baseform_ModelForm(instance=proc_basic_personal_information, prefix="basic_personal_information")
    # context
    context['dorsal_artery_pulsation_examination'] = dorsal_artery_pulsation_examination
    context['history_of_infectious_diseases'] = history_of_infectious_diseases
    context['basic_personal_information'] = basic_personal_information
    context['proc_id'] = kwargs['id']
    return render(request, 'test1_update.html', context)

    
def test2_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    context = {}
    
    # inquire_forms
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        major_life_events = Major_life_events_baseform_ModelForm(request.POST, prefix="major_life_events")
        dorsal_artery_pulsation_examination = Dorsal_artery_pulsation_examination_baseform_ModelForm(request.POST, prefix="dorsal_artery_pulsation_examination")
        history_of_infectious_diseases = History_of_infectious_diseases_baseform_ModelForm(request.POST, prefix="history_of_infectious_diseases")
        basic_personal_information = Basic_personal_information_baseform_ModelForm(request.POST, prefix="basic_personal_information")
        if major_life_events.is_valid() and dorsal_artery_pulsation_examination.is_valid() and history_of_infectious_diseases.is_valid() and basic_personal_information.is_valid():
            major_life_events.save()
            dorsal_artery_pulsation_examination.save()
            history_of_infectious_diseases.save()
            basic_personal_information.save()
            return redirect(reverse('index'))
    else:
        major_life_events = Major_life_events_baseform_ModelForm(prefix="major_life_events")
        dorsal_artery_pulsation_examination = Dorsal_artery_pulsation_examination_baseform_ModelForm(prefix="dorsal_artery_pulsation_examination")
        history_of_infectious_diseases = History_of_infectious_diseases_baseform_ModelForm(prefix="history_of_infectious_diseases")
        basic_personal_information = Basic_personal_information_baseform_ModelForm(prefix="basic_personal_information")
    # context
    context['major_life_events'] = major_life_events
    context['dorsal_artery_pulsation_examination'] = dorsal_artery_pulsation_examination
    context['history_of_infectious_diseases'] = history_of_infectious_diseases
    context['basic_personal_information'] = basic_personal_information
    return render(request, 'test2_create.html', context)

    


def test2_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    context = {}
    
    proc_major_life_events = Major_life_events.objects.get(pid=operation_proc)
    proc_dorsal_artery_pulsation_examination = Dorsal_artery_pulsation_examination.objects.get(pid=operation_proc)
    proc_history_of_infectious_diseases = History_of_infectious_diseases.objects.get(pid=operation_proc)
    proc_basic_personal_information = Basic_personal_information.objects.get(pid=operation_proc)
    # inquire_forms
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        major_life_events = Major_life_events_baseform_ModelForm(instance=proc_major_life_events, data=request.POST, prefix="major_life_events")
        dorsal_artery_pulsation_examination = Dorsal_artery_pulsation_examination_baseform_ModelForm(instance=proc_dorsal_artery_pulsation_examination, data=request.POST, prefix="dorsal_artery_pulsation_examination")
        history_of_infectious_diseases = History_of_infectious_diseases_baseform_ModelForm(instance=proc_history_of_infectious_diseases, data=request.POST, prefix="history_of_infectious_diseases")
        basic_personal_information = Basic_personal_information_baseform_ModelForm(instance=proc_basic_personal_information, data=request.POST, prefix="basic_personal_information")
        if major_life_events.is_valid() and dorsal_artery_pulsation_examination.is_valid() and history_of_infectious_diseases.is_valid() and basic_personal_information.is_valid():
            major_life_events.save()
            dorsal_artery_pulsation_examination.save()
            history_of_infectious_diseases.save()
            basic_personal_information.save()
            # 构造作业完成消息参数
            post_fields = request.POST.dict()
            post_fields.pop('csrfmiddlewaretoken')
            operand_finished.send(sender=test2_update, pid=kwargs['id'], ocode='rtc', field_values=post_fields)
            return redirect(reverse('index'))
    else:
        major_life_events = Major_life_events_baseform_ModelForm(instance=proc_major_life_events, prefix="major_life_events")
        dorsal_artery_pulsation_examination = Dorsal_artery_pulsation_examination_baseform_ModelForm(instance=proc_dorsal_artery_pulsation_examination, prefix="dorsal_artery_pulsation_examination")
        history_of_infectious_diseases = History_of_infectious_diseases_baseform_ModelForm(instance=proc_history_of_infectious_diseases, prefix="history_of_infectious_diseases")
        basic_personal_information = Basic_personal_information_baseform_ModelForm(instance=proc_basic_personal_information, prefix="basic_personal_information")
    # context
    context['major_life_events'] = major_life_events
    context['dorsal_artery_pulsation_examination'] = dorsal_artery_pulsation_examination
    context['history_of_infectious_diseases'] = history_of_infectious_diseases
    context['basic_personal_information'] = basic_personal_information
    context['proc_id'] = kwargs['id']
    return render(request, 'test2_update.html', context)

    
def test3_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    context = {}
    
    # inquire_forms
    basic_personal_information = Basic_personal_information_baseform_query_1641894654_ModelForm(instance=customer, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        social_environment_assessment = Social_environment_assessment_baseform_ModelForm(request.POST, prefix="social_environment_assessment")
        if social_environment_assessment.is_valid():
            social_environment_assessment.save()
            return redirect(reverse('index'))
    else:
        social_environment_assessment = Social_environment_assessment_baseform_ModelForm(prefix="social_environment_assessment")
    # context
    context['basic_personal_information'] = basic_personal_information
    context['social_environment_assessment'] = social_environment_assessment
    return render(request, 'test3_create.html', context)

    


def test3_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    context = {}
    
    proc_social_environment_assessment = Social_environment_assessment.objects.get(pid=operation_proc)
    # inquire_forms
    basic_personal_information = Basic_personal_information_baseform_query_1641894654_ModelForm(instance=customer, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        social_environment_assessment = Social_environment_assessment_baseform_ModelForm(instance=proc_social_environment_assessment, data=request.POST, prefix="social_environment_assessment")
        if social_environment_assessment.is_valid():
            social_environment_assessment.save()
            # 构造作业完成消息参数
            post_fields = request.POST.dict()
            post_fields.pop('csrfmiddlewaretoken')
            operand_finished.send(sender=test3_update, pid=kwargs['id'], ocode='rtc', field_values=post_fields)
            return redirect(reverse('index'))
    else:
        social_environment_assessment = Social_environment_assessment_baseform_ModelForm(instance=proc_social_environment_assessment, prefix="social_environment_assessment")
    # context
    context['basic_personal_information'] = basic_personal_information
    context['social_environment_assessment'] = social_environment_assessment
    context['proc_id'] = kwargs['id']
    return render(request, 'test3_update.html', context)

    