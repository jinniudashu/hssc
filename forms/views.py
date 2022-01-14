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


def yuan_qian_zheng_zhuang_diao_cha_biao_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    context = {}
    
    # inquire_forms
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey_baseform_ModelForm(request.POST, prefix="out_of_hospital_self_report_survey")
        if out_of_hospital_self_report_survey.is_valid():
            out_of_hospital_self_report_survey.save()
            return redirect(reverse('index'))
    else:
        out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey_baseform_ModelForm(prefix="out_of_hospital_self_report_survey")
    # context
    context['basic_personal_information'] = basic_personal_information
    context['out_of_hospital_self_report_survey'] = out_of_hospital_self_report_survey
    return render(request, 'yuan_qian_zheng_zhuang_diao_cha_biao_create.html', context)

    


def yuan_qian_zheng_zhuang_diao_cha_biao_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    context = {}
    
    proc_out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey.objects.get(pid=operation_proc)
    # inquire_forms
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey_baseform_ModelForm(instance=proc_out_of_hospital_self_report_survey, data=request.POST, prefix="out_of_hospital_self_report_survey")
        if out_of_hospital_self_report_survey.is_valid():
            out_of_hospital_self_report_survey.save()
            # 构造作业完成消息参数
            post_fields = request.POST.dict()
            post_fields.pop('csrfmiddlewaretoken')
            operand_finished.send(sender=yuan_qian_zheng_zhuang_diao_cha_biao_update, pid=kwargs['id'], ocode='rtc', field_values=post_fields)
            return redirect(reverse('index'))
    else:
        out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey_baseform_ModelForm(instance=proc_out_of_hospital_self_report_survey, prefix="out_of_hospital_self_report_survey")
    # context
    context['basic_personal_information'] = basic_personal_information
    context['out_of_hospital_self_report_survey'] = out_of_hospital_self_report_survey
    context['proc_id'] = kwargs['id']
    return render(request, 'yuan_qian_zheng_zhuang_diao_cha_biao_update.html', context)

    
def men_zhen_wen_zhen_diao_cha_biao_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    context = {}
    
    # inquire_forms
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey_baseform_ModelForm(request.POST, prefix="out_of_hospital_self_report_survey")
        men_zhen_wen_zhen_diao_cha_biao = Men_zhen_wen_zhen_diao_cha_biao_baseform_ModelForm(request.POST, prefix="men_zhen_wen_zhen_diao_cha_biao")
        if out_of_hospital_self_report_survey.is_valid() and men_zhen_wen_zhen_diao_cha_biao.is_valid():
            out_of_hospital_self_report_survey.save()
            men_zhen_wen_zhen_diao_cha_biao.save()
            return redirect(reverse('index'))
    else:
        out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey_baseform_ModelForm(prefix="out_of_hospital_self_report_survey")
        men_zhen_wen_zhen_diao_cha_biao = Men_zhen_wen_zhen_diao_cha_biao_baseform_ModelForm(prefix="men_zhen_wen_zhen_diao_cha_biao")
    # context
    context['basic_personal_information'] = basic_personal_information
    context['basic_personal_information'] = basic_personal_information
    context['out_of_hospital_self_report_survey'] = out_of_hospital_self_report_survey
    context['men_zhen_wen_zhen_diao_cha_biao'] = men_zhen_wen_zhen_diao_cha_biao
    return render(request, 'men_zhen_wen_zhen_diao_cha_biao_create.html', context)

    


def men_zhen_wen_zhen_diao_cha_biao_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    context = {}
    
    proc_out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey.objects.get(pid=operation_proc)
    proc_men_zhen_wen_zhen_diao_cha_biao = Men_zhen_wen_zhen_diao_cha_biao.objects.get(pid=operation_proc)
    # inquire_forms
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey_baseform_ModelForm(instance=proc_out_of_hospital_self_report_survey, data=request.POST, prefix="out_of_hospital_self_report_survey")
        men_zhen_wen_zhen_diao_cha_biao = Men_zhen_wen_zhen_diao_cha_biao_baseform_ModelForm(instance=proc_men_zhen_wen_zhen_diao_cha_biao, data=request.POST, prefix="men_zhen_wen_zhen_diao_cha_biao")
        if out_of_hospital_self_report_survey.is_valid() and men_zhen_wen_zhen_diao_cha_biao.is_valid():
            out_of_hospital_self_report_survey.save()
            men_zhen_wen_zhen_diao_cha_biao.save()
            # 构造作业完成消息参数
            post_fields = request.POST.dict()
            post_fields.pop('csrfmiddlewaretoken')
            operand_finished.send(sender=men_zhen_wen_zhen_diao_cha_biao_update, pid=kwargs['id'], ocode='rtc', field_values=post_fields)
            return redirect(reverse('index'))
    else:
        out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey_baseform_ModelForm(instance=proc_out_of_hospital_self_report_survey, prefix="out_of_hospital_self_report_survey")
        men_zhen_wen_zhen_diao_cha_biao = Men_zhen_wen_zhen_diao_cha_biao_baseform_ModelForm(instance=proc_men_zhen_wen_zhen_diao_cha_biao, prefix="men_zhen_wen_zhen_diao_cha_biao")
    # context
    context['basic_personal_information'] = basic_personal_information
    context['basic_personal_information'] = basic_personal_information
    context['out_of_hospital_self_report_survey'] = out_of_hospital_self_report_survey
    context['men_zhen_wen_zhen_diao_cha_biao'] = men_zhen_wen_zhen_diao_cha_biao
    context['proc_id'] = kwargs['id']
    return render(request, 'men_zhen_wen_zhen_diao_cha_biao_update.html', context)

    
def ge_ren_ji_bing_shi_diao_cha_biao_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    context = {}
    
    # inquire_forms
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        medical_history = Medical_history_baseform_ModelForm(request.POST, prefix="medical_history")
        if medical_history.is_valid():
            medical_history.save()
            return redirect(reverse('index'))
    else:
        medical_history = Medical_history_baseform_ModelForm(prefix="medical_history")
    # context
    context['basic_personal_information'] = basic_personal_information
    context['medical_history'] = medical_history
    return render(request, 'ge_ren_ji_bing_shi_diao_cha_biao_create.html', context)

    


def ge_ren_ji_bing_shi_diao_cha_biao_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    context = {}
    
    proc_medical_history = Medical_history.objects.get(pid=operation_proc)
    # inquire_forms
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        medical_history = Medical_history_baseform_ModelForm(instance=proc_medical_history, data=request.POST, prefix="medical_history")
        if medical_history.is_valid():
            medical_history.save()
            # 构造作业完成消息参数
            post_fields = request.POST.dict()
            post_fields.pop('csrfmiddlewaretoken')
            operand_finished.send(sender=ge_ren_ji_bing_shi_diao_cha_biao_update, pid=kwargs['id'], ocode='rtc', field_values=post_fields)
            return redirect(reverse('index'))
    else:
        medical_history = Medical_history_baseform_ModelForm(instance=proc_medical_history, prefix="medical_history")
    # context
    context['basic_personal_information'] = basic_personal_information
    context['medical_history'] = medical_history
    context['proc_id'] = kwargs['id']
    return render(request, 'ge_ren_ji_bing_shi_diao_cha_biao_update.html', context)

    
def kong_fu_xue_tang_jian_cha_biao_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    context = {}
    
    # inquire_forms
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        kong_fu_xue_tang_jian_cha = Kong_fu_xue_tang_jian_cha_baseform_ModelForm(request.POST, prefix="kong_fu_xue_tang_jian_cha")
        if kong_fu_xue_tang_jian_cha.is_valid():
            kong_fu_xue_tang_jian_cha.save()
            return redirect(reverse('index'))
    else:
        kong_fu_xue_tang_jian_cha = Kong_fu_xue_tang_jian_cha_baseform_ModelForm(prefix="kong_fu_xue_tang_jian_cha")
    # context
    context['basic_personal_information'] = basic_personal_information
    context['kong_fu_xue_tang_jian_cha'] = kong_fu_xue_tang_jian_cha
    return render(request, 'kong_fu_xue_tang_jian_cha_biao_create.html', context)

    


def kong_fu_xue_tang_jian_cha_biao_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    context = {}
    
    proc_kong_fu_xue_tang_jian_cha = Kong_fu_xue_tang_jian_cha.objects.get(pid=operation_proc)
    # inquire_forms
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        kong_fu_xue_tang_jian_cha = Kong_fu_xue_tang_jian_cha_baseform_ModelForm(instance=proc_kong_fu_xue_tang_jian_cha, data=request.POST, prefix="kong_fu_xue_tang_jian_cha")
        if kong_fu_xue_tang_jian_cha.is_valid():
            kong_fu_xue_tang_jian_cha.save()
            # 构造作业完成消息参数
            post_fields = request.POST.dict()
            post_fields.pop('csrfmiddlewaretoken')
            operand_finished.send(sender=kong_fu_xue_tang_jian_cha_biao_update, pid=kwargs['id'], ocode='rtc', field_values=post_fields)
            return redirect(reverse('index'))
    else:
        kong_fu_xue_tang_jian_cha = Kong_fu_xue_tang_jian_cha_baseform_ModelForm(instance=proc_kong_fu_xue_tang_jian_cha, prefix="kong_fu_xue_tang_jian_cha")
    # context
    context['basic_personal_information'] = basic_personal_information
    context['kong_fu_xue_tang_jian_cha'] = kong_fu_xue_tang_jian_cha
    context['proc_id'] = kwargs['id']
    return render(request, 'kong_fu_xue_tang_jian_cha_biao_update.html', context)

    
def men_zhen_zhen_duan_biao_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    context = {}
    
    # inquire_forms
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        men_zhen_zhen_duan_biao = Men_zhen_zhen_duan_biao_baseform_ModelForm(request.POST, prefix="men_zhen_zhen_duan_biao")
        if men_zhen_zhen_duan_biao.is_valid():
            men_zhen_zhen_duan_biao.save()
            return redirect(reverse('index'))
    else:
        men_zhen_zhen_duan_biao = Men_zhen_zhen_duan_biao_baseform_ModelForm(prefix="men_zhen_zhen_duan_biao")
    # context
    context['basic_personal_information'] = basic_personal_information
    context['men_zhen_zhen_duan_biao'] = men_zhen_zhen_duan_biao
    return render(request, 'men_zhen_zhen_duan_biao_create.html', context)

    


def men_zhen_zhen_duan_biao_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    context = {}
    
    proc_men_zhen_zhen_duan_biao = Men_zhen_zhen_duan_biao.objects.get(pid=operation_proc)
    # inquire_forms
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        men_zhen_zhen_duan_biao = Men_zhen_zhen_duan_biao_baseform_ModelForm(instance=proc_men_zhen_zhen_duan_biao, data=request.POST, prefix="men_zhen_zhen_duan_biao")
        if men_zhen_zhen_duan_biao.is_valid():
            men_zhen_zhen_duan_biao.save()
            # 构造作业完成消息参数
            post_fields = request.POST.dict()
            post_fields.pop('csrfmiddlewaretoken')
            operand_finished.send(sender=men_zhen_zhen_duan_biao_update, pid=kwargs['id'], ocode='rtc', field_values=post_fields)
            return redirect(reverse('index'))
    else:
        men_zhen_zhen_duan_biao = Men_zhen_zhen_duan_biao_baseform_ModelForm(instance=proc_men_zhen_zhen_duan_biao, prefix="men_zhen_zhen_duan_biao")
    # context
    context['basic_personal_information'] = basic_personal_information
    context['men_zhen_zhen_duan_biao'] = men_zhen_zhen_duan_biao
    context['proc_id'] = kwargs['id']
    return render(request, 'men_zhen_zhen_duan_biao_update.html', context)

    
def tang_hua_xue_hong_dan_bai_jian_cha_biao_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    context = {}
    
    # inquire_forms
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        tang_hua_xue_hong_dan_bai_jian_cha_biao = Tang_hua_xue_hong_dan_bai_jian_cha_biao_baseform_ModelForm(request.POST, prefix="tang_hua_xue_hong_dan_bai_jian_cha_biao")
        if tang_hua_xue_hong_dan_bai_jian_cha_biao.is_valid():
            tang_hua_xue_hong_dan_bai_jian_cha_biao.save()
            return redirect(reverse('index'))
    else:
        tang_hua_xue_hong_dan_bai_jian_cha_biao = Tang_hua_xue_hong_dan_bai_jian_cha_biao_baseform_ModelForm(prefix="tang_hua_xue_hong_dan_bai_jian_cha_biao")
    # context
    context['basic_personal_information'] = basic_personal_information
    context['tang_hua_xue_hong_dan_bai_jian_cha_biao'] = tang_hua_xue_hong_dan_bai_jian_cha_biao
    return render(request, 'tang_hua_xue_hong_dan_bai_jian_cha_biao_create.html', context)

    


def tang_hua_xue_hong_dan_bai_jian_cha_biao_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    context = {}
    
    proc_tang_hua_xue_hong_dan_bai_jian_cha_biao = Tang_hua_xue_hong_dan_bai_jian_cha_biao.objects.get(pid=operation_proc)
    # inquire_forms
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        tang_hua_xue_hong_dan_bai_jian_cha_biao = Tang_hua_xue_hong_dan_bai_jian_cha_biao_baseform_ModelForm(instance=proc_tang_hua_xue_hong_dan_bai_jian_cha_biao, data=request.POST, prefix="tang_hua_xue_hong_dan_bai_jian_cha_biao")
        if tang_hua_xue_hong_dan_bai_jian_cha_biao.is_valid():
            tang_hua_xue_hong_dan_bai_jian_cha_biao.save()
            # 构造作业完成消息参数
            post_fields = request.POST.dict()
            post_fields.pop('csrfmiddlewaretoken')
            operand_finished.send(sender=tang_hua_xue_hong_dan_bai_jian_cha_biao_update, pid=kwargs['id'], ocode='rtc', field_values=post_fields)
            return redirect(reverse('index'))
    else:
        tang_hua_xue_hong_dan_bai_jian_cha_biao = Tang_hua_xue_hong_dan_bai_jian_cha_biao_baseform_ModelForm(instance=proc_tang_hua_xue_hong_dan_bai_jian_cha_biao, prefix="tang_hua_xue_hong_dan_bai_jian_cha_biao")
    # context
    context['basic_personal_information'] = basic_personal_information
    context['tang_hua_xue_hong_dan_bai_jian_cha_biao'] = tang_hua_xue_hong_dan_bai_jian_cha_biao
    context['proc_id'] = kwargs['id']
    return render(request, 'tang_hua_xue_hong_dan_bai_jian_cha_biao_update.html', context)

    