from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.forms import modelformset_factory, inlineformset_factory
from core.models import Operation_proc, Staff, Customer

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
			todo['slug'] = proc.entry
			todos.append(todo)
		context = super().get_context_data(**kwargs)
		context['todos'] = todos
		return context


class Guo_min_shi_diao_cha_biao_CreateView(CreateView):
    template_name = 'guo_min_shi_diao_cha_biao_edit.html'
    success_url = '/'
    form_class = Allergies_history_baseform_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Guo_min_shi_diao_cha_biao_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1639620882_ModelForm(instance=self.customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Allergies_history_baseform_ModelForm(self.request.POST, prefix="form1")
        else:
            form1 = Allergies_history_baseform_ModelForm(prefix="form1")
        # context
        context['form0'] = form0
        context['form1'] = form1

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        return super(Guo_min_shi_diao_cha_biao_CreateView, self).form_valid(form)

        
class Ge_ren_ji_bing_shi_diao_cha_biao_CreateView(CreateView):
    template_name = 'ge_ren_ji_bing_shi_diao_cha_biao_edit.html'
    success_url = '/'
    form_class = Medical_history_baseform_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Ge_ren_ji_bing_shi_diao_cha_biao_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1639620882_ModelForm(instance=self.customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Medical_history_baseform_ModelForm(self.request.POST, prefix="form1")
        else:
            form1 = Medical_history_baseform_ModelForm(prefix="form1")
        # context
        context['form0'] = form0
        context['form1'] = form1

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        return super(Ge_ren_ji_bing_shi_diao_cha_biao_CreateView, self).form_valid(form)

        
class Yuan_qian_wen_zhen_biao_CreateView(CreateView):
    template_name = 'yuan_qian_wen_zhen_biao_edit.html'
    success_url = '/'
    form_class = Out_of_hospital_self_report_survey_baseform_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Yuan_qian_wen_zhen_biao_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1639643054_ModelForm(instance=self.customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Out_of_hospital_self_report_survey_baseform_ModelForm(self.request.POST, prefix="form1")
        else:
            form1 = Out_of_hospital_self_report_survey_baseform_ModelForm(prefix="form1")
        # context
        context['form0'] = form0
        context['form1'] = form1

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        return super(Yuan_qian_wen_zhen_biao_CreateView, self).form_valid(form)

        
class Bing_li_shou_ye_CreateView(CreateView):
    template_name = 'bing_li_shou_ye_edit.html'
    success_url = '/'
    form_class = Allergies_history_baseform_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Bing_li_shou_ye_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1639643054_ModelForm(instance=self.customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Allergies_history_baseform_ModelForm(self.request.POST, prefix="form1")
            form2 = Family_history_of_illness_baseform_ModelForm(self.request.POST, prefix="form2")
            form3 = Medical_history_baseform_ModelForm(self.request.POST, prefix="form3")
            form4 = History_of_infectious_diseases_baseform_ModelForm(self.request.POST, prefix="form4")
        else:
            form1 = Allergies_history_baseform_ModelForm(prefix="form1")
            form2 = Family_history_of_illness_baseform_ModelForm(prefix="form2")
            form3 = Medical_history_baseform_ModelForm(prefix="form3")
            form4 = History_of_infectious_diseases_baseform_ModelForm(prefix="form4")
        # context
        context['form0'] = form0
        context['form1'] = form1
        context['form2'] = form2
        context['form3'] = form3
        context['form4'] = form4

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form2'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form3'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form4'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        return super(Bing_li_shou_ye_CreateView, self).form_valid(form)

        
class Men_zhen_wen_zhen_biao_CreateView(CreateView):
    template_name = 'men_zhen_wen_zhen_biao_edit.html'
    success_url = '/'
    form_class = Allergies_history_baseform_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Men_zhen_wen_zhen_biao_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1639643054_ModelForm(instance=self.customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Allergies_history_baseform_ModelForm(self.request.POST, prefix="form1")
            form2 = Out_of_hospital_self_report_survey_baseform_ModelForm(self.request.POST, prefix="form2")
            form3 = Family_history_of_illness_baseform_ModelForm(self.request.POST, prefix="form3")
            form4 = Medical_history_baseform_ModelForm(self.request.POST, prefix="form4")
            form5 = History_of_infectious_diseases_baseform_ModelForm(self.request.POST, prefix="form5")
            form6 = Blood_pressure_monitoring_baseform_ModelForm(self.request.POST, prefix="form6")
            form7 = Men_zhen_wen_zhen_diao_cha_baseform_ModelForm(self.request.POST, prefix="form7")
        else:
            form1 = Allergies_history_baseform_ModelForm(prefix="form1")
            form2 = Out_of_hospital_self_report_survey_baseform_ModelForm(prefix="form2")
            form3 = Family_history_of_illness_baseform_ModelForm(prefix="form3")
            form4 = Medical_history_baseform_ModelForm(prefix="form4")
            form5 = History_of_infectious_diseases_baseform_ModelForm(prefix="form5")
            form6 = Blood_pressure_monitoring_baseform_ModelForm(prefix="form6")
            form7 = Men_zhen_wen_zhen_diao_cha_baseform_ModelForm(prefix="form7")
        # context
        context['form0'] = form0
        context['form1'] = form1
        context['form2'] = form2
        context['form3'] = form3
        context['form4'] = form4
        context['form5'] = form5
        context['form6'] = form6
        context['form7'] = form7

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form2'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form3'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form4'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form5'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form6'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form7'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        return super(Men_zhen_wen_zhen_biao_CreateView, self).form_valid(form)

        
class Ju_min_jian_kang_dang_an_CreateView(CreateView):
    template_name = 'ju_min_jian_kang_dang_an_edit.html'
    success_url = '/'
    form_class = Allergies_history_baseform_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Ju_min_jian_kang_dang_an_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form0 = Allergies_history_baseform_ModelForm(self.request.POST, prefix="form0")
            form1 = Personal_comprehensive_psychological_quality_survey_baseform_ModelForm(self.request.POST, prefix="form1")
            form2 = Personal_adaptability_assessment_baseform_ModelForm(self.request.POST, prefix="form2")
            form3 = Personal_health_behavior_survey_baseform_ModelForm(self.request.POST, prefix="form3")
            form4 = Personal_health_assessment_baseform_ModelForm(self.request.POST, prefix="form4")
            form5 = Social_environment_assessment_baseform_ModelForm(self.request.POST, prefix="form5")
            form6 = Family_history_of_illness_baseform_ModelForm(self.request.POST, prefix="form6")
            form7 = History_of_blood_transfusion_baseform_ModelForm(self.request.POST, prefix="form7")
            form8 = History_of_trauma_baseform_ModelForm(self.request.POST, prefix="form8")
            form9 = Medical_history_baseform_ModelForm(self.request.POST, prefix="form9")
            form10 = History_of_infectious_diseases_baseform_ModelForm(self.request.POST, prefix="form10")
            form11 = History_of_surgery_baseform_ModelForm(self.request.POST, prefix="form11")
            form12 = Major_life_events_baseform_ModelForm(self.request.POST, prefix="form12")
            form13 = Basic_personal_information_baseform_ModelForm(self.request.POST, prefix="form13")
        else:
            form0 = Allergies_history_baseform_ModelForm(prefix="form0")
            form1 = Personal_comprehensive_psychological_quality_survey_baseform_ModelForm(prefix="form1")
            form2 = Personal_adaptability_assessment_baseform_ModelForm(prefix="form2")
            form3 = Personal_health_behavior_survey_baseform_ModelForm(prefix="form3")
            form4 = Personal_health_assessment_baseform_ModelForm(prefix="form4")
            form5 = Social_environment_assessment_baseform_ModelForm(prefix="form5")
            form6 = Family_history_of_illness_baseform_ModelForm(prefix="form6")
            form7 = History_of_blood_transfusion_baseform_ModelForm(prefix="form7")
            form8 = History_of_trauma_baseform_ModelForm(prefix="form8")
            form9 = Medical_history_baseform_ModelForm(prefix="form9")
            form10 = History_of_infectious_diseases_baseform_ModelForm(prefix="form10")
            form11 = History_of_surgery_baseform_ModelForm(prefix="form11")
            form12 = Major_life_events_baseform_ModelForm(prefix="form12")
            form13 = Basic_personal_information_baseform_ModelForm(prefix="form13")
        # context
        context['form0'] = form0
        context['form1'] = form1
        context['form2'] = form2
        context['form3'] = form3
        context['form4'] = form4
        context['form5'] = form5
        context['form6'] = form6
        context['form7'] = form7
        context['form8'] = form8
        context['form9'] = form9
        context['form10'] = form10
        context['form11'] = form11
        context['form12'] = form12
        context['form13'] = form13

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid
        f = context['form0'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form1'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form2'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form3'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form4'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form5'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form6'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form7'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form8'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form9'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form10'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form11'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form12'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form13'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        return super(Ju_min_jian_kang_dang_an_CreateView, self).form_valid(form)

        
class Ti_jian_cha_ti_biao_CreateView(CreateView):
    template_name = 'ti_jian_cha_ti_biao_edit.html'
    success_url = '/'
    form_class = Vital_signs_check_baseform_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Ti_jian_cha_ti_biao_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1639620882_ModelForm(instance=self.customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Vital_signs_check_baseform_ModelForm(self.request.POST, prefix="form1")
            form2 = Physical_examination_baseform_ModelForm(self.request.POST, prefix="form2")
            form3 = Physical_examination_hearing_baseform_ModelForm(self.request.POST, prefix="form3")
            form4 = Physical_examination_oral_cavity_baseform_ModelForm(self.request.POST, prefix="form4")
            form5 = Physical_examination_vision_baseform_ModelForm(self.request.POST, prefix="form5")
            form6 = Physical_examination_athletic_ability_baseform_ModelForm(self.request.POST, prefix="form6")
        else:
            form1 = Vital_signs_check_baseform_ModelForm(prefix="form1")
            form2 = Physical_examination_baseform_ModelForm(prefix="form2")
            form3 = Physical_examination_hearing_baseform_ModelForm(prefix="form3")
            form4 = Physical_examination_oral_cavity_baseform_ModelForm(prefix="form4")
            form5 = Physical_examination_vision_baseform_ModelForm(prefix="form5")
            form6 = Physical_examination_athletic_ability_baseform_ModelForm(prefix="form6")
        # context
        context['form0'] = form0
        context['form1'] = form1
        context['form2'] = form2
        context['form3'] = form3
        context['form4'] = form4
        context['form5'] = form5
        context['form6'] = form6

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form2'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form3'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form4'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form5'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form6'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        return super(Ti_jian_cha_ti_biao_CreateView, self).form_valid(form)

        
class Xue_ya_jian_ce_biao_CreateView(CreateView):
    template_name = 'xue_ya_jian_ce_biao_edit.html'
    success_url = '/'
    form_class = Blood_pressure_monitoring_baseform_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Xue_ya_jian_ce_biao_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1639620882_ModelForm(instance=self.customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Blood_pressure_monitoring_baseform_ModelForm(self.request.POST, prefix="form1")
        else:
            form1 = Blood_pressure_monitoring_baseform_ModelForm(prefix="form1")
        # context
        context['form0'] = form0
        context['form1'] = form1

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        return super(Xue_ya_jian_ce_biao_CreateView, self).form_valid(form)

        
class Tang_hua_xue_hong_dan_bai_jian_cha_biao_CreateView(CreateView):
    template_name = 'tang_hua_xue_hong_dan_bai_jian_cha_biao_edit.html'
    success_url = '/'
    form_class = Tang_hua_xue_hong_dan_bai_jian_cha_biao_baseform_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Tang_hua_xue_hong_dan_bai_jian_cha_biao_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1639620882_ModelForm(instance=self.customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Tang_hua_xue_hong_dan_bai_jian_cha_biao_baseform_ModelForm(self.request.POST, prefix="form1")
        else:
            form1 = Tang_hua_xue_hong_dan_bai_jian_cha_biao_baseform_ModelForm(prefix="form1")
        # context
        context['form0'] = form0
        context['form1'] = form1

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        return super(Tang_hua_xue_hong_dan_bai_jian_cha_biao_CreateView, self).form_valid(form)

        
class Kong_fu_xue_tang_jian_cha_biao_CreateView(CreateView):
    template_name = 'kong_fu_xue_tang_jian_cha_biao_edit.html'
    success_url = '/'
    form_class = Kong_fu_xue_tang_jian_cha_baseform_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Kong_fu_xue_tang_jian_cha_biao_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1639620882_ModelForm(instance=self.customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Kong_fu_xue_tang_jian_cha_baseform_ModelForm(self.request.POST, prefix="form1")
        else:
            form1 = Kong_fu_xue_tang_jian_cha_baseform_ModelForm(prefix="form1")
        # context
        context['form0'] = form0
        context['form1'] = form1

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        return super(Kong_fu_xue_tang_jian_cha_biao_CreateView, self).form_valid(form)

        
class Tang_niao_bing_cha_ti_biao_CreateView(CreateView):
    template_name = 'tang_niao_bing_cha_ti_biao_edit.html'
    success_url = '/'
    form_class = Fundus_examination_baseform_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Tang_niao_bing_cha_ti_biao_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1639620882_ModelForm(instance=self.customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Fundus_examination_baseform_ModelForm(self.request.POST, prefix="form1")
            form2 = Dorsal_artery_pulsation_examination_baseform_ModelForm(self.request.POST, prefix="form2")
        else:
            form1 = Fundus_examination_baseform_ModelForm(prefix="form1")
            form2 = Dorsal_artery_pulsation_examination_baseform_ModelForm(prefix="form2")
        # context
        context['form0'] = form0
        context['form1'] = form1
        context['form2'] = form2

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form2'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        return super(Tang_niao_bing_cha_ti_biao_CreateView, self).form_valid(form)

        
class Can_hou_2_xiao_shi_xue_tang_jian_cha_biao_CreateView(CreateView):
    template_name = 'can_hou_2_xiao_shi_xue_tang_jian_cha_biao_edit.html'
    success_url = '/'
    form_class = Can_hou_2_xiao_shi_xue_tang_baseform_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Can_hou_2_xiao_shi_xue_tang_jian_cha_biao_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1639620882_ModelForm(instance=self.customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Can_hou_2_xiao_shi_xue_tang_baseform_ModelForm(self.request.POST, prefix="form1")
        else:
            form1 = Can_hou_2_xiao_shi_xue_tang_baseform_ModelForm(prefix="form1")
        # context
        context['form0'] = form0
        context['form1'] = form1

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        return super(Can_hou_2_xiao_shi_xue_tang_jian_cha_biao_CreateView, self).form_valid(form)

        
class Zhen_duan_biao_CreateView(CreateView):
    template_name = 'zhen_duan_biao_edit.html'
    success_url = '/'
    form_class = Zhen_duan_biao_baseform_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Zhen_duan_biao_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1639620882_ModelForm(instance=self.customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Zhen_duan_biao_baseform_ModelForm(self.request.POST, prefix="form1")
        else:
            form1 = Zhen_duan_biao_baseform_ModelForm(prefix="form1")
        # context
        context['form0'] = form0
        context['form1'] = form1

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        return super(Zhen_duan_biao_CreateView, self).form_valid(form)

        
class Yong_yao_chu_fang_biao_CreateView(CreateView):
    template_name = 'yong_yao_chu_fang_biao_edit.html'
    success_url = '/'
    form_class = Yong_yao_chu_fang_baseform_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Yong_yao_chu_fang_biao_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1639620882_ModelForm(instance=self.customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Yong_yao_chu_fang_baseform_ModelForm(self.request.POST, prefix="form1")
        else:
            form1 = Yong_yao_chu_fang_baseform_ModelForm(prefix="form1")
        # context
        context['form0'] = form0
        context['form1'] = form1

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        return super(Yong_yao_chu_fang_biao_CreateView, self).form_valid(form)

        