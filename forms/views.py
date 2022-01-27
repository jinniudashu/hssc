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
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {}
    
    # inquire_forms
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        form_out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey_baseform_ModelForm(request.POST, prefix="out_of_hospital_self_report_survey")
        if form_out_of_hospital_self_report_survey.is_valid():
            form_out_of_hospital_self_report_survey.save()
            return redirect(reverse('index'))
    else:
        form_out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey_baseform_ModelForm(prefix="out_of_hospital_self_report_survey")
    # context
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_out_of_hospital_self_report_survey'] = form_out_of_hospital_self_report_survey
    return render(request, 'yuan_qian_zheng_zhuang_diao_cha_biao_create.html', context)


def yuan_qian_zheng_zhuang_diao_cha_biao_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {}
    
    out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey.objects.get(pid=operation_proc)
    # inquire_forms
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        form_out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey_baseform_ModelForm(instance=out_of_hospital_self_report_survey, data=request.POST, prefix="out_of_hospital_self_report_survey")
        if form_out_of_hospital_self_report_survey.is_valid():
            form_out_of_hospital_self_report_survey.save()
            # 构造作业完成消息参数
            operand_finished.send(sender=yuan_qian_zheng_zhuang_diao_cha_biao_update, pid=kwargs['id'], ocode='rtc', field_values=request.POST)
            return redirect(reverse('index'))
    else:
        form_out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey_baseform_ModelForm(instance=out_of_hospital_self_report_survey, prefix="out_of_hospital_self_report_survey")
    # context
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_out_of_hospital_self_report_survey'] = form_out_of_hospital_self_report_survey
    context['proc_id'] = kwargs['id']
    return render(request, 'yuan_qian_zheng_zhuang_diao_cha_biao_update.html', context)

    
def ge_ren_ji_bing_shi_diao_cha_biao_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {}
    
    # inquire_forms
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        form_medical_history = Medical_history_baseform_ModelForm(request.POST, prefix="medical_history")
        if form_medical_history.is_valid():
            form_medical_history.save()
            return redirect(reverse('index'))
    else:
        form_medical_history = Medical_history_baseform_ModelForm(prefix="medical_history")
    # context
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_medical_history'] = form_medical_history
    return render(request, 'ge_ren_ji_bing_shi_diao_cha_biao_create.html', context)


def ge_ren_ji_bing_shi_diao_cha_biao_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {}
    
    medical_history = Medical_history.objects.get(pid=operation_proc)
    # inquire_forms
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        form_medical_history = Medical_history_baseform_ModelForm(instance=medical_history, data=request.POST, prefix="medical_history")
        if form_medical_history.is_valid():
            form_medical_history.save()
            # 构造作业完成消息参数
            operand_finished.send(sender=yuan_qian_zheng_zhuang_diao_cha_biao_update, pid=kwargs['id'], ocode='rtc', field_values=request.POST)
            return redirect(reverse('index'))
    else:
        form_medical_history = Medical_history_baseform_ModelForm(instance=medical_history, prefix="medical_history")
    # context
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_medical_history'] = form_medical_history
    context['proc_id'] = kwargs['id']
    return render(request, 'ge_ren_ji_bing_shi_diao_cha_biao_update.html', context)

    
def kong_fu_xue_tang_jian_cha_biao_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {}
    
    # inquire_forms
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        form_kong_fu_xue_tang_jian_cha = Kong_fu_xue_tang_jian_cha_baseform_ModelForm(request.POST, prefix="kong_fu_xue_tang_jian_cha")
        if form_kong_fu_xue_tang_jian_cha.is_valid():
            form_kong_fu_xue_tang_jian_cha.save()
            return redirect(reverse('index'))
    else:
        form_kong_fu_xue_tang_jian_cha = Kong_fu_xue_tang_jian_cha_baseform_ModelForm(prefix="kong_fu_xue_tang_jian_cha")
    # context
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_kong_fu_xue_tang_jian_cha'] = form_kong_fu_xue_tang_jian_cha
    return render(request, 'kong_fu_xue_tang_jian_cha_biao_create.html', context)


def kong_fu_xue_tang_jian_cha_biao_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {}
    
    kong_fu_xue_tang_jian_cha = Kong_fu_xue_tang_jian_cha.objects.get(pid=operation_proc)
    # inquire_forms
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        form_kong_fu_xue_tang_jian_cha = Kong_fu_xue_tang_jian_cha_baseform_ModelForm(instance=kong_fu_xue_tang_jian_cha, data=request.POST, prefix="kong_fu_xue_tang_jian_cha")
        if form_kong_fu_xue_tang_jian_cha.is_valid():
            form_kong_fu_xue_tang_jian_cha.save()
            # 构造作业完成消息参数
            operand_finished.send(sender=yuan_qian_zheng_zhuang_diao_cha_biao_update, pid=kwargs['id'], ocode='rtc', field_values=request.POST)
            return redirect(reverse('index'))
    else:
        form_kong_fu_xue_tang_jian_cha = Kong_fu_xue_tang_jian_cha_baseform_ModelForm(instance=kong_fu_xue_tang_jian_cha, prefix="kong_fu_xue_tang_jian_cha")
    # context
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_kong_fu_xue_tang_jian_cha'] = form_kong_fu_xue_tang_jian_cha
    context['proc_id'] = kwargs['id']
    return render(request, 'kong_fu_xue_tang_jian_cha_biao_update.html', context)

    
def men_zhen_zhen_duan_biao_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {}
    
    # inquire_forms
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        form_men_zhen_zhen_duan_biao = Men_zhen_zhen_duan_biao_baseform_ModelForm(request.POST, prefix="men_zhen_zhen_duan_biao")
        if form_men_zhen_zhen_duan_biao.is_valid():
            form_men_zhen_zhen_duan_biao.save()
            return redirect(reverse('index'))
    else:
        form_men_zhen_zhen_duan_biao = Men_zhen_zhen_duan_biao_baseform_ModelForm(prefix="men_zhen_zhen_duan_biao")
    # context
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_men_zhen_zhen_duan_biao'] = form_men_zhen_zhen_duan_biao
    return render(request, 'men_zhen_zhen_duan_biao_create.html', context)


def men_zhen_zhen_duan_biao_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {}
    
    men_zhen_zhen_duan_biao = Men_zhen_zhen_duan_biao.objects.get(pid=operation_proc)
    # inquire_forms
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        form_men_zhen_zhen_duan_biao = Men_zhen_zhen_duan_biao_baseform_ModelForm(instance=men_zhen_zhen_duan_biao, data=request.POST, prefix="men_zhen_zhen_duan_biao")
        if form_men_zhen_zhen_duan_biao.is_valid():
            form_men_zhen_zhen_duan_biao.save()
            # 构造作业完成消息参数
            operand_finished.send(sender=yuan_qian_zheng_zhuang_diao_cha_biao_update, pid=kwargs['id'], ocode='rtc', field_values=request.POST)
            return redirect(reverse('index'))
    else:
        form_men_zhen_zhen_duan_biao = Men_zhen_zhen_duan_biao_baseform_ModelForm(instance=men_zhen_zhen_duan_biao, prefix="men_zhen_zhen_duan_biao")
    # context
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_men_zhen_zhen_duan_biao'] = form_men_zhen_zhen_duan_biao
    context['proc_id'] = kwargs['id']
    return render(request, 'men_zhen_zhen_duan_biao_update.html', context)

    
def tang_hua_xue_hong_dan_bai_jian_cha_biao_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {}
    
    # inquire_forms
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        form_tang_hua_xue_hong_dan_bai_jian_cha_biao = Tang_hua_xue_hong_dan_bai_jian_cha_biao_baseform_ModelForm(request.POST, prefix="tang_hua_xue_hong_dan_bai_jian_cha_biao")
        if form_tang_hua_xue_hong_dan_bai_jian_cha_biao.is_valid():
            form_tang_hua_xue_hong_dan_bai_jian_cha_biao.save()
            return redirect(reverse('index'))
    else:
        form_tang_hua_xue_hong_dan_bai_jian_cha_biao = Tang_hua_xue_hong_dan_bai_jian_cha_biao_baseform_ModelForm(prefix="tang_hua_xue_hong_dan_bai_jian_cha_biao")
    # context
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_tang_hua_xue_hong_dan_bai_jian_cha_biao'] = form_tang_hua_xue_hong_dan_bai_jian_cha_biao
    return render(request, 'tang_hua_xue_hong_dan_bai_jian_cha_biao_create.html', context)


def tang_hua_xue_hong_dan_bai_jian_cha_biao_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {}
    
    tang_hua_xue_hong_dan_bai_jian_cha_biao = Tang_hua_xue_hong_dan_bai_jian_cha_biao.objects.get(pid=operation_proc)
    # inquire_forms
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        form_tang_hua_xue_hong_dan_bai_jian_cha_biao = Tang_hua_xue_hong_dan_bai_jian_cha_biao_baseform_ModelForm(instance=tang_hua_xue_hong_dan_bai_jian_cha_biao, data=request.POST, prefix="tang_hua_xue_hong_dan_bai_jian_cha_biao")
        if form_tang_hua_xue_hong_dan_bai_jian_cha_biao.is_valid():
            form_tang_hua_xue_hong_dan_bai_jian_cha_biao.save()
            # 构造作业完成消息参数
            operand_finished.send(sender=yuan_qian_zheng_zhuang_diao_cha_biao_update, pid=kwargs['id'], ocode='rtc', field_values=request.POST)
            return redirect(reverse('index'))
    else:
        form_tang_hua_xue_hong_dan_bai_jian_cha_biao = Tang_hua_xue_hong_dan_bai_jian_cha_biao_baseform_ModelForm(instance=tang_hua_xue_hong_dan_bai_jian_cha_biao, prefix="tang_hua_xue_hong_dan_bai_jian_cha_biao")
    # context
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_tang_hua_xue_hong_dan_bai_jian_cha_biao'] = form_tang_hua_xue_hong_dan_bai_jian_cha_biao
    context['proc_id'] = kwargs['id']
    return render(request, 'tang_hua_xue_hong_dan_bai_jian_cha_biao_update.html', context)

    
def chang_gui_cha_ti_biao_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {}
    
    # inquire_forms
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        form_vital_signs_check = Vital_signs_check_baseform_ModelForm(request.POST, prefix="vital_signs_check")
        form_physical_examination = Physical_examination_baseform_ModelForm(request.POST, prefix="physical_examination")
        form_physical_examination_hearing = Physical_examination_hearing_baseform_ModelForm(request.POST, prefix="physical_examination_hearing")
        form_physical_examination_oral_cavity = Physical_examination_oral_cavity_baseform_ModelForm(request.POST, prefix="physical_examination_oral_cavity")
        form_physical_examination_vision = Physical_examination_vision_baseform_ModelForm(request.POST, prefix="physical_examination_vision")
        form_physical_examination_athletic_ability = Physical_examination_athletic_ability_baseform_ModelForm(request.POST, prefix="physical_examination_athletic_ability")
        if form_vital_signs_check.is_valid() and form_physical_examination.is_valid() and form_physical_examination_hearing.is_valid() and form_physical_examination_oral_cavity.is_valid() and form_physical_examination_vision.is_valid() and form_physical_examination_athletic_ability.is_valid():
            form_vital_signs_check.save()
            form_physical_examination.save()
            form_physical_examination_hearing.save()
            form_physical_examination_oral_cavity.save()
            form_physical_examination_vision.save()
            form_physical_examination_athletic_ability.save()
            return redirect(reverse('index'))
    else:
        form_vital_signs_check = Vital_signs_check_baseform_ModelForm(prefix="vital_signs_check")
        form_physical_examination = Physical_examination_baseform_ModelForm(prefix="physical_examination")
        form_physical_examination_hearing = Physical_examination_hearing_baseform_ModelForm(prefix="physical_examination_hearing")
        form_physical_examination_oral_cavity = Physical_examination_oral_cavity_baseform_ModelForm(prefix="physical_examination_oral_cavity")
        form_physical_examination_vision = Physical_examination_vision_baseform_ModelForm(prefix="physical_examination_vision")
        form_physical_examination_athletic_ability = Physical_examination_athletic_ability_baseform_ModelForm(prefix="physical_examination_athletic_ability")
    # context
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_vital_signs_check'] = form_vital_signs_check
    context['form_physical_examination'] = form_physical_examination
    context['form_physical_examination_hearing'] = form_physical_examination_hearing
    context['form_physical_examination_oral_cavity'] = form_physical_examination_oral_cavity
    context['form_physical_examination_vision'] = form_physical_examination_vision
    context['form_physical_examination_athletic_ability'] = form_physical_examination_athletic_ability
    return render(request, 'chang_gui_cha_ti_biao_create.html', context)


def chang_gui_cha_ti_biao_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {}
    
    vital_signs_check = Vital_signs_check.objects.get(pid=operation_proc)
    physical_examination = Physical_examination.objects.get(pid=operation_proc)
    physical_examination_hearing = Physical_examination_hearing.objects.get(pid=operation_proc)
    physical_examination_oral_cavity = Physical_examination_oral_cavity.objects.get(pid=operation_proc)
    physical_examination_vision = Physical_examination_vision.objects.get(pid=operation_proc)
    physical_examination_athletic_ability = Physical_examination_athletic_ability.objects.get(pid=operation_proc)
    # inquire_forms
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        form_vital_signs_check = Vital_signs_check_baseform_ModelForm(instance=vital_signs_check, data=request.POST, prefix="vital_signs_check")
        form_physical_examination = Physical_examination_baseform_ModelForm(instance=physical_examination, data=request.POST, prefix="physical_examination")
        form_physical_examination_hearing = Physical_examination_hearing_baseform_ModelForm(instance=physical_examination_hearing, data=request.POST, prefix="physical_examination_hearing")
        form_physical_examination_oral_cavity = Physical_examination_oral_cavity_baseform_ModelForm(instance=physical_examination_oral_cavity, data=request.POST, prefix="physical_examination_oral_cavity")
        form_physical_examination_vision = Physical_examination_vision_baseform_ModelForm(instance=physical_examination_vision, data=request.POST, prefix="physical_examination_vision")
        form_physical_examination_athletic_ability = Physical_examination_athletic_ability_baseform_ModelForm(instance=physical_examination_athletic_ability, data=request.POST, prefix="physical_examination_athletic_ability")
        if form_vital_signs_check.is_valid() and form_physical_examination.is_valid() and form_physical_examination_hearing.is_valid() and form_physical_examination_oral_cavity.is_valid() and form_physical_examination_vision.is_valid() and form_physical_examination_athletic_ability.is_valid():
            form_vital_signs_check.save()
            form_physical_examination.save()
            form_physical_examination_hearing.save()
            form_physical_examination_oral_cavity.save()
            form_physical_examination_vision.save()
            form_physical_examination_athletic_ability.save()
            # 构造作业完成消息参数
            operand_finished.send(sender=yuan_qian_zheng_zhuang_diao_cha_biao_update, pid=kwargs['id'], ocode='rtc', field_values=request.POST)
            return redirect(reverse('index'))
    else:
        form_vital_signs_check = Vital_signs_check_baseform_ModelForm(instance=vital_signs_check, prefix="vital_signs_check")
        form_physical_examination = Physical_examination_baseform_ModelForm(instance=physical_examination, prefix="physical_examination")
        form_physical_examination_hearing = Physical_examination_hearing_baseform_ModelForm(instance=physical_examination_hearing, prefix="physical_examination_hearing")
        form_physical_examination_oral_cavity = Physical_examination_oral_cavity_baseform_ModelForm(instance=physical_examination_oral_cavity, prefix="physical_examination_oral_cavity")
        form_physical_examination_vision = Physical_examination_vision_baseform_ModelForm(instance=physical_examination_vision, prefix="physical_examination_vision")
        form_physical_examination_athletic_ability = Physical_examination_athletic_ability_baseform_ModelForm(instance=physical_examination_athletic_ability, prefix="physical_examination_athletic_ability")
    # context
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_vital_signs_check'] = form_vital_signs_check
    context['form_physical_examination'] = form_physical_examination
    context['form_physical_examination_hearing'] = form_physical_examination_hearing
    context['form_physical_examination_oral_cavity'] = form_physical_examination_oral_cavity
    context['form_physical_examination_vision'] = form_physical_examination_vision
    context['form_physical_examination_athletic_ability'] = form_physical_examination_athletic_ability
    context['proc_id'] = kwargs['id']
    return render(request, 'chang_gui_cha_ti_biao_update.html', context)

    
def tang_niao_bing_cha_ti_biao_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {}
    
    # inquire_forms
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        form_fundus_examination = Fundus_examination_baseform_ModelForm(request.POST, prefix="fundus_examination")
        form_dorsal_artery_pulsation_examination = Dorsal_artery_pulsation_examination_baseform_ModelForm(request.POST, prefix="dorsal_artery_pulsation_examination")
        if form_fundus_examination.is_valid() and form_dorsal_artery_pulsation_examination.is_valid():
            form_fundus_examination.save()
            form_dorsal_artery_pulsation_examination.save()
            return redirect(reverse('index'))
    else:
        form_fundus_examination = Fundus_examination_baseform_ModelForm(prefix="fundus_examination")
        form_dorsal_artery_pulsation_examination = Dorsal_artery_pulsation_examination_baseform_ModelForm(prefix="dorsal_artery_pulsation_examination")
    # context
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_fundus_examination'] = form_fundus_examination
    context['form_dorsal_artery_pulsation_examination'] = form_dorsal_artery_pulsation_examination
    return render(request, 'tang_niao_bing_cha_ti_biao_create.html', context)


def tang_niao_bing_cha_ti_biao_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {}
    
    fundus_examination = Fundus_examination.objects.get(pid=operation_proc)
    dorsal_artery_pulsation_examination = Dorsal_artery_pulsation_examination.objects.get(pid=operation_proc)
    # inquire_forms
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        form_fundus_examination = Fundus_examination_baseform_ModelForm(instance=fundus_examination, data=request.POST, prefix="fundus_examination")
        form_dorsal_artery_pulsation_examination = Dorsal_artery_pulsation_examination_baseform_ModelForm(instance=dorsal_artery_pulsation_examination, data=request.POST, prefix="dorsal_artery_pulsation_examination")
        if form_fundus_examination.is_valid() and form_dorsal_artery_pulsation_examination.is_valid():
            form_fundus_examination.save()
            form_dorsal_artery_pulsation_examination.save()
            # 构造作业完成消息参数
            operand_finished.send(sender=yuan_qian_zheng_zhuang_diao_cha_biao_update, pid=kwargs['id'], ocode='rtc', field_values=request.POST)
            return redirect(reverse('index'))
    else:
        form_fundus_examination = Fundus_examination_baseform_ModelForm(instance=fundus_examination, prefix="fundus_examination")
        form_dorsal_artery_pulsation_examination = Dorsal_artery_pulsation_examination_baseform_ModelForm(instance=dorsal_artery_pulsation_examination, prefix="dorsal_artery_pulsation_examination")
    # context
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_fundus_examination'] = form_fundus_examination
    context['form_dorsal_artery_pulsation_examination'] = form_dorsal_artery_pulsation_examination
    context['proc_id'] = kwargs['id']
    return render(request, 'tang_niao_bing_cha_ti_biao_update.html', context)

    
def ge_ren_guo_min_shi_diao_cha_biao_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {}
    
    # inquire_forms
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        form_allergies_history = Allergies_history_baseform_ModelForm(request.POST, prefix="allergies_history")
        if form_allergies_history.is_valid():
            form_allergies_history.save()
            return redirect(reverse('index'))
    else:
        form_allergies_history = Allergies_history_baseform_ModelForm(prefix="allergies_history")
    # context
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_allergies_history'] = form_allergies_history
    return render(request, 'ge_ren_guo_min_shi_diao_cha_biao_create.html', context)


def ge_ren_guo_min_shi_diao_cha_biao_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {}
    
    allergies_history = Allergies_history.objects.get(pid=operation_proc)
    # inquire_forms
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        form_allergies_history = Allergies_history_baseform_ModelForm(instance=allergies_history, data=request.POST, prefix="allergies_history")
        if form_allergies_history.is_valid():
            form_allergies_history.save()
            # 构造作业完成消息参数
            operand_finished.send(sender=yuan_qian_zheng_zhuang_diao_cha_biao_update, pid=kwargs['id'], ocode='rtc', field_values=request.POST)
            return redirect(reverse('index'))
    else:
        form_allergies_history = Allergies_history_baseform_ModelForm(instance=allergies_history, prefix="allergies_history")
    # context
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_allergies_history'] = form_allergies_history
    context['proc_id'] = kwargs['id']
    return render(request, 'ge_ren_guo_min_shi_diao_cha_biao_update.html', context)

    
def men_zhen_wen_zhen_diao_cha_biao_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {}
    
    # inquire_forms
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    form_out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey_baseform_query_1642212281_ModelForm(instance=out_of_hospital_self_report_survey, prefix="out_of_hospital_self_report_survey")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        form_out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey_baseform_ModelForm(request.POST, prefix="out_of_hospital_self_report_survey")
        form_men_zhen_wen_zhen_diao_cha_biao = Men_zhen_wen_zhen_diao_cha_biao_baseform_ModelForm(request.POST, prefix="men_zhen_wen_zhen_diao_cha_biao")
        if form_out_of_hospital_self_report_survey.is_valid() and form_men_zhen_wen_zhen_diao_cha_biao.is_valid():
            form_out_of_hospital_self_report_survey.save()
            form_men_zhen_wen_zhen_diao_cha_biao.save()
            return redirect(reverse('index'))
    else:
        form_out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey_baseform_ModelForm(prefix="out_of_hospital_self_report_survey")
        form_men_zhen_wen_zhen_diao_cha_biao = Men_zhen_wen_zhen_diao_cha_biao_baseform_ModelForm(prefix="men_zhen_wen_zhen_diao_cha_biao")
    # context
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_out_of_hospital_self_report_survey'] = form_out_of_hospital_self_report_survey
    context['form_out_of_hospital_self_report_survey'] = form_out_of_hospital_self_report_survey
    context['form_men_zhen_wen_zhen_diao_cha_biao'] = form_men_zhen_wen_zhen_diao_cha_biao
    return render(request, 'men_zhen_wen_zhen_diao_cha_biao_create.html', context)


def men_zhen_wen_zhen_diao_cha_biao_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {}
    
    out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey.objects.get(pid=operation_proc)
    men_zhen_wen_zhen_diao_cha_biao = Men_zhen_wen_zhen_diao_cha_biao.objects.get(pid=operation_proc)
    # inquire_forms
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    form_out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey_baseform_query_1642212281_ModelForm(instance=out_of_hospital_self_report_survey, prefix="out_of_hospital_self_report_survey")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        form_out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey_baseform_ModelForm(instance=out_of_hospital_self_report_survey, data=request.POST, prefix="out_of_hospital_self_report_survey")
        form_men_zhen_wen_zhen_diao_cha_biao = Men_zhen_wen_zhen_diao_cha_biao_baseform_ModelForm(instance=men_zhen_wen_zhen_diao_cha_biao, data=request.POST, prefix="men_zhen_wen_zhen_diao_cha_biao")
        if form_out_of_hospital_self_report_survey.is_valid() and form_men_zhen_wen_zhen_diao_cha_biao.is_valid():
            form_out_of_hospital_self_report_survey.save()
            form_men_zhen_wen_zhen_diao_cha_biao.save()
            # 构造作业完成消息参数
            operand_finished.send(sender=yuan_qian_zheng_zhuang_diao_cha_biao_update, pid=kwargs['id'], ocode='rtc', field_values=request.POST)
            return redirect(reverse('index'))
    else:
        form_out_of_hospital_self_report_survey = Out_of_hospital_self_report_survey_baseform_ModelForm(instance=out_of_hospital_self_report_survey, prefix="out_of_hospital_self_report_survey")
        form_men_zhen_wen_zhen_diao_cha_biao = Men_zhen_wen_zhen_diao_cha_biao_baseform_ModelForm(instance=men_zhen_wen_zhen_diao_cha_biao, prefix="men_zhen_wen_zhen_diao_cha_biao")
    # context
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_out_of_hospital_self_report_survey'] = form_out_of_hospital_self_report_survey
    context['form_out_of_hospital_self_report_survey'] = form_out_of_hospital_self_report_survey
    context['form_men_zhen_wen_zhen_diao_cha_biao'] = form_men_zhen_wen_zhen_diao_cha_biao
    context['proc_id'] = kwargs['id']
    return render(request, 'men_zhen_wen_zhen_diao_cha_biao_update.html', context)

    
def men_zhen_chu_fang_biao_create(request):
    customer = Customer.objects.get(user=request.user)
    operator = Staff.objects.get(user=request.user)
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {}
    
    # inquire_forms
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        form_yong_yao_chu_fang = Yong_yao_chu_fang_baseform_ModelForm(request.POST, prefix="yong_yao_chu_fang")
        if form_yong_yao_chu_fang.is_valid():
            form_yong_yao_chu_fang.save()
            return redirect(reverse('index'))
    else:
        form_yong_yao_chu_fang = Yong_yao_chu_fang_baseform_ModelForm(prefix="yong_yao_chu_fang")
    # context
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_yong_yao_chu_fang'] = form_yong_yao_chu_fang
    return render(request, 'men_zhen_chu_fang_biao_create.html', context)


def men_zhen_chu_fang_biao_update(request, *args, **kwargs):
    operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
    customer = operation_proc.customer
    operator = operation_proc.operator
    basic_personal_information = Basic_personal_information.objects.get(customer=customer)
    context = {}
    
    yong_yao_chu_fang = Yong_yao_chu_fang.objects.get(pid=operation_proc)
    # inquire_forms
    form_basic_personal_information = Basic_personal_information_baseform_query_1642159528_ModelForm(instance=basic_personal_information, prefix="basic_personal_information")
    # mutate_formsets
    # mutate_forms
    if request.method == 'POST':
        form_yong_yao_chu_fang = Yong_yao_chu_fang_baseform_ModelForm(instance=yong_yao_chu_fang, data=request.POST, prefix="yong_yao_chu_fang")
        if form_yong_yao_chu_fang.is_valid():
            form_yong_yao_chu_fang.save()
            # 构造作业完成消息参数
            operand_finished.send(sender=yuan_qian_zheng_zhuang_diao_cha_biao_update, pid=kwargs['id'], ocode='rtc', field_values=request.POST)
            return redirect(reverse('index'))
    else:
        form_yong_yao_chu_fang = Yong_yao_chu_fang_baseform_ModelForm(instance=yong_yao_chu_fang, prefix="yong_yao_chu_fang")
    # context
    context['form_basic_personal_information'] = form_basic_personal_information
    context['form_yong_yao_chu_fang'] = form_yong_yao_chu_fang
    context['proc_id'] = kwargs['id']
    return render(request, 'men_zhen_chu_fang_biao_update.html', context)

    