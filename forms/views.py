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

    
def chang_gui_cha_ti_biao_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    context = {}
    
    # inquire_forms
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        vital_signs_check = Vital_signs_check_baseform_ModelForm(request.POST, prefix="vital_signs_check")
        physical_examination = Physical_examination_baseform_ModelForm(request.POST, prefix="physical_examination")
        physical_examination_hearing = Physical_examination_hearing_baseform_ModelForm(request.POST, prefix="physical_examination_hearing")
        physical_examination_oral_cavity = Physical_examination_oral_cavity_baseform_ModelForm(request.POST, prefix="physical_examination_oral_cavity")
        physical_examination_vision = Physical_examination_vision_baseform_ModelForm(request.POST, prefix="physical_examination_vision")
        physical_examination_athletic_ability = Physical_examination_athletic_ability_baseform_ModelForm(request.POST, prefix="physical_examination_athletic_ability")
        if vital_signs_check.is_valid() and physical_examination.is_valid() and physical_examination_hearing.is_valid() and physical_examination_oral_cavity.is_valid() and physical_examination_vision.is_valid() and physical_examination_athletic_ability.is_valid():
            vital_signs_check.save()
            physical_examination.save()
            physical_examination_hearing.save()
            physical_examination_oral_cavity.save()
            physical_examination_vision.save()
            physical_examination_athletic_ability.save()
            return redirect(reverse('index'))
    else:
        vital_signs_check = Vital_signs_check_baseform_ModelForm(prefix="vital_signs_check")
        physical_examination = Physical_examination_baseform_ModelForm(prefix="physical_examination")
        physical_examination_hearing = Physical_examination_hearing_baseform_ModelForm(prefix="physical_examination_hearing")
        physical_examination_oral_cavity = Physical_examination_oral_cavity_baseform_ModelForm(prefix="physical_examination_oral_cavity")
        physical_examination_vision = Physical_examination_vision_baseform_ModelForm(prefix="physical_examination_vision")
        physical_examination_athletic_ability = Physical_examination_athletic_ability_baseform_ModelForm(prefix="physical_examination_athletic_ability")
    # context
    context['basic_personal_information'] = basic_personal_information
    context['vital_signs_check'] = vital_signs_check
    context['physical_examination'] = physical_examination
    context['physical_examination_hearing'] = physical_examination_hearing
    context['physical_examination_oral_cavity'] = physical_examination_oral_cavity
    context['physical_examination_vision'] = physical_examination_vision
    context['physical_examination_athletic_ability'] = physical_examination_athletic_ability
    return render(request, 'chang_gui_cha_ti_biao_create.html', context)

    


def chang_gui_cha_ti_biao_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    context = {}
    
    proc_vital_signs_check = Vital_signs_check.objects.get(pid=operation_proc)
    proc_physical_examination = Physical_examination.objects.get(pid=operation_proc)
    proc_physical_examination_hearing = Physical_examination_hearing.objects.get(pid=operation_proc)
    proc_physical_examination_oral_cavity = Physical_examination_oral_cavity.objects.get(pid=operation_proc)
    proc_physical_examination_vision = Physical_examination_vision.objects.get(pid=operation_proc)
    proc_physical_examination_athletic_ability = Physical_examination_athletic_ability.objects.get(pid=operation_proc)
    # inquire_forms
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        vital_signs_check = Vital_signs_check_baseform_ModelForm(instance=proc_vital_signs_check, data=request.POST, prefix="vital_signs_check")
        physical_examination = Physical_examination_baseform_ModelForm(instance=proc_physical_examination, data=request.POST, prefix="physical_examination")
        physical_examination_hearing = Physical_examination_hearing_baseform_ModelForm(instance=proc_physical_examination_hearing, data=request.POST, prefix="physical_examination_hearing")
        physical_examination_oral_cavity = Physical_examination_oral_cavity_baseform_ModelForm(instance=proc_physical_examination_oral_cavity, data=request.POST, prefix="physical_examination_oral_cavity")
        physical_examination_vision = Physical_examination_vision_baseform_ModelForm(instance=proc_physical_examination_vision, data=request.POST, prefix="physical_examination_vision")
        physical_examination_athletic_ability = Physical_examination_athletic_ability_baseform_ModelForm(instance=proc_physical_examination_athletic_ability, data=request.POST, prefix="physical_examination_athletic_ability")
        if vital_signs_check.is_valid() and physical_examination.is_valid() and physical_examination_hearing.is_valid() and physical_examination_oral_cavity.is_valid() and physical_examination_vision.is_valid() and physical_examination_athletic_ability.is_valid():
            vital_signs_check.save()
            physical_examination.save()
            physical_examination_hearing.save()
            physical_examination_oral_cavity.save()
            physical_examination_vision.save()
            physical_examination_athletic_ability.save()
            # 构造作业完成消息参数
            post_fields = request.POST.dict()
            post_fields.pop('csrfmiddlewaretoken')
            operand_finished.send(sender=chang_gui_cha_ti_biao_update, pid=kwargs['id'], ocode='rtc', field_values=post_fields)
            return redirect(reverse('index'))
    else:
        vital_signs_check = Vital_signs_check_baseform_ModelForm(instance=proc_vital_signs_check, prefix="vital_signs_check")
        physical_examination = Physical_examination_baseform_ModelForm(instance=proc_physical_examination, prefix="physical_examination")
        physical_examination_hearing = Physical_examination_hearing_baseform_ModelForm(instance=proc_physical_examination_hearing, prefix="physical_examination_hearing")
        physical_examination_oral_cavity = Physical_examination_oral_cavity_baseform_ModelForm(instance=proc_physical_examination_oral_cavity, prefix="physical_examination_oral_cavity")
        physical_examination_vision = Physical_examination_vision_baseform_ModelForm(instance=proc_physical_examination_vision, prefix="physical_examination_vision")
        physical_examination_athletic_ability = Physical_examination_athletic_ability_baseform_ModelForm(instance=proc_physical_examination_athletic_ability, prefix="physical_examination_athletic_ability")
    # context
    context['basic_personal_information'] = basic_personal_information
    context['vital_signs_check'] = vital_signs_check
    context['physical_examination'] = physical_examination
    context['physical_examination_hearing'] = physical_examination_hearing
    context['physical_examination_oral_cavity'] = physical_examination_oral_cavity
    context['physical_examination_vision'] = physical_examination_vision
    context['physical_examination_athletic_ability'] = physical_examination_athletic_ability
    context['proc_id'] = kwargs['id']
    return render(request, 'chang_gui_cha_ti_biao_update.html', context)

    
def tang_niao_bing_cha_ti_biao_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    context = {}
    
    # inquire_forms
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        fundus_examination = Fundus_examination_baseform_ModelForm(request.POST, prefix="fundus_examination")
        dorsal_artery_pulsation_examination = Dorsal_artery_pulsation_examination_baseform_ModelForm(request.POST, prefix="dorsal_artery_pulsation_examination")
        if fundus_examination.is_valid() and dorsal_artery_pulsation_examination.is_valid():
            fundus_examination.save()
            dorsal_artery_pulsation_examination.save()
            return redirect(reverse('index'))
    else:
        fundus_examination = Fundus_examination_baseform_ModelForm(prefix="fundus_examination")
        dorsal_artery_pulsation_examination = Dorsal_artery_pulsation_examination_baseform_ModelForm(prefix="dorsal_artery_pulsation_examination")
    # context
    context['basic_personal_information'] = basic_personal_information
    context['fundus_examination'] = fundus_examination
    context['dorsal_artery_pulsation_examination'] = dorsal_artery_pulsation_examination
    return render(request, 'tang_niao_bing_cha_ti_biao_create.html', context)

    


def tang_niao_bing_cha_ti_biao_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    context = {}
    
    proc_fundus_examination = Fundus_examination.objects.get(pid=operation_proc)
    proc_dorsal_artery_pulsation_examination = Dorsal_artery_pulsation_examination.objects.get(pid=operation_proc)
    # inquire_forms
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        fundus_examination = Fundus_examination_baseform_ModelForm(instance=proc_fundus_examination, data=request.POST, prefix="fundus_examination")
        dorsal_artery_pulsation_examination = Dorsal_artery_pulsation_examination_baseform_ModelForm(instance=proc_dorsal_artery_pulsation_examination, data=request.POST, prefix="dorsal_artery_pulsation_examination")
        if fundus_examination.is_valid() and dorsal_artery_pulsation_examination.is_valid():
            fundus_examination.save()
            dorsal_artery_pulsation_examination.save()
            # 构造作业完成消息参数
            post_fields = request.POST.dict()
            post_fields.pop('csrfmiddlewaretoken')
            operand_finished.send(sender=tang_niao_bing_cha_ti_biao_update, pid=kwargs['id'], ocode='rtc', field_values=post_fields)
            return redirect(reverse('index'))
    else:
        fundus_examination = Fundus_examination_baseform_ModelForm(instance=proc_fundus_examination, prefix="fundus_examination")
        dorsal_artery_pulsation_examination = Dorsal_artery_pulsation_examination_baseform_ModelForm(instance=proc_dorsal_artery_pulsation_examination, prefix="dorsal_artery_pulsation_examination")
    # context
    context['basic_personal_information'] = basic_personal_information
    context['fundus_examination'] = fundus_examination
    context['dorsal_artery_pulsation_examination'] = dorsal_artery_pulsation_examination
    context['proc_id'] = kwargs['id']
    return render(request, 'tang_niao_bing_cha_ti_biao_update.html', context)

    
def ge_ren_guo_min_shi_diao_cha_biao_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    context = {}
    
    # inquire_forms
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        allergies_history = Allergies_history_baseform_ModelForm(request.POST, prefix="allergies_history")
        if allergies_history.is_valid():
            allergies_history.save()
            return redirect(reverse('index'))
    else:
        allergies_history = Allergies_history_baseform_ModelForm(prefix="allergies_history")
    # context
    context['basic_personal_information'] = basic_personal_information
    context['allergies_history'] = allergies_history
    return render(request, 'ge_ren_guo_min_shi_diao_cha_biao_create.html', context)

    


def ge_ren_guo_min_shi_diao_cha_biao_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    context = {}
    
    proc_allergies_history = Allergies_history.objects.get(pid=operation_proc)
    # inquire_forms
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        allergies_history = Allergies_history_baseform_ModelForm(instance=proc_allergies_history, data=request.POST, prefix="allergies_history")
        if allergies_history.is_valid():
            allergies_history.save()
            # 构造作业完成消息参数
            post_fields = request.POST.dict()
            post_fields.pop('csrfmiddlewaretoken')
            operand_finished.send(sender=ge_ren_guo_min_shi_diao_cha_biao_update, pid=kwargs['id'], ocode='rtc', field_values=post_fields)
            return redirect(reverse('index'))
    else:
        allergies_history = Allergies_history_baseform_ModelForm(instance=proc_allergies_history, prefix="allergies_history")
    # context
    context['basic_personal_information'] = basic_personal_information
    context['allergies_history'] = allergies_history
    context['proc_id'] = kwargs['id']
    return render(request, 'ge_ren_guo_min_shi_diao_cha_biao_update.html', context)

    
def men_zhen_wen_zhen_diao_cha_biao_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    context = {}
    
    # inquire_forms
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey_baseform_query_1642212281_ModelForm(instance=customer, prefix="out_of_hospital_self_report_survey")
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
    context['basic_personal_information'] = basic_personal_information
    context['out_of_hospital_self_report_survey'] = out_of_hospital_self_report_survey
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
    basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=customer, prefix="basic_personal_information")
    out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey_baseform_query_1642212281_ModelForm(instance=customer, prefix="out_of_hospital_self_report_survey")
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
    context['basic_personal_information'] = basic_personal_information
    context['out_of_hospital_self_report_survey'] = out_of_hospital_self_report_survey
    context['out_of_hospital_self_report_survey'] = out_of_hospital_self_report_survey
    context['men_zhen_wen_zhen_diao_cha_biao'] = men_zhen_wen_zhen_diao_cha_biao
    context['proc_id'] = kwargs['id']
    return render(request, 'men_zhen_wen_zhen_diao_cha_biao_update.html', context)

    