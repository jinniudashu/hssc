from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.forms import modelformset_factory, inlineformset_factory

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
			todo['slug'] = proc.entry
			todos.append(todo)
		context = super().get_context_data(**kwargs)
		context['todos'] = todos
		return context


class Yuan_qian_zheng_zhuang_diao_cha_biao_CreateView(CreateView):
    template_name = 'yuan_qian_zheng_zhuang_diao_cha_biao_edit.html'
    success_url = '/'
    form_class = Out_of_hospital_self_report_survey_baseform_ModelForm

    def get_context_data(self, **kwargs):
        context = super(Yuan_qian_zheng_zhuang_diao_cha_biao_CreateView, self).get_context_data(**kwargs)
        customer = Customer.objects.get(user=self.request.user)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1641519651_ModelForm(instance=customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Out_of_hospital_self_report_survey_baseform_ModelForm(self.request.POST, prefix="form1")
        else:
            form1 = Out_of_hospital_self_report_survey_baseform_ModelForm(prefix="form1")
        # context
        context['form0'] = form0
        context['form1'] = form1

        context['user'] = self.request.user

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
                
        return super(Yuan_qian_zheng_zhuang_diao_cha_biao_CreateView, self).form_valid(form)

        
class Guo_min_shi_diao_cha_biao_CreateView(CreateView):
    template_name = 'guo_min_shi_diao_cha_biao_edit.html'
    success_url = '/'
    form_class = Allergies_history_baseform_ModelForm

    def get_context_data(self, **kwargs):
        context = super(Guo_min_shi_diao_cha_biao_CreateView, self).get_context_data(**kwargs)
        customer = Customer.objects.get(user=self.request.user)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1641519651_ModelForm(instance=customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Allergies_history_baseform_ModelForm(self.request.POST, prefix="form1")
        else:
            form1 = Allergies_history_baseform_ModelForm(prefix="form1")
        # context
        context['form0'] = form0
        context['form1'] = form1

        context['user'] = self.request.user

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
                
        return super(Guo_min_shi_diao_cha_biao_CreateView, self).form_valid(form)

        
class Ge_ren_ji_bing_shi_diao_cha_biao_CreateView(CreateView):
    template_name = 'ge_ren_ji_bing_shi_diao_cha_biao_edit.html'
    success_url = '/'
    form_class = Medical_history_baseform_ModelForm

    def get_context_data(self, **kwargs):
        context = super(Ge_ren_ji_bing_shi_diao_cha_biao_CreateView, self).get_context_data(**kwargs)
        customer = Customer.objects.get(user=self.request.user)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1641519651_ModelForm(instance=customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Medical_history_baseform_ModelForm(self.request.POST, prefix="form1")
        else:
            form1 = Medical_history_baseform_ModelForm(prefix="form1")
        # context
        context['form0'] = form0
        context['form1'] = form1

        context['user'] = self.request.user

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
                
        return super(Ge_ren_ji_bing_shi_diao_cha_biao_CreateView, self).form_valid(form)

        
class Ge_ren_jian_kang_xing_wei_diao_cha_biao_CreateView(CreateView):
    template_name = 'ge_ren_jian_kang_xing_wei_diao_cha_biao_edit.html'
    success_url = '/'
    form_class = Personal_health_behavior_survey_baseform_ModelForm

    def get_context_data(self, **kwargs):
        context = super(Ge_ren_jian_kang_xing_wei_diao_cha_biao_CreateView, self).get_context_data(**kwargs)
        customer = Customer.objects.get(user=self.request.user)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1641519651_ModelForm(instance=customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Personal_health_behavior_survey_baseform_ModelForm(self.request.POST, prefix="form1")
        else:
            form1 = Personal_health_behavior_survey_baseform_ModelForm(prefix="form1")
        # context
        context['form0'] = form0
        context['form1'] = form1

        context['user'] = self.request.user

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
                
        return super(Ge_ren_jian_kang_xing_wei_diao_cha_biao_CreateView, self).form_valid(form)

        
class Yuan_nei_wen_zhen_diao_cha_biao_CreateView(CreateView):
    template_name = 'yuan_nei_wen_zhen_diao_cha_biao_edit.html'
    success_url = '/'
    form_class = Out_of_hospital_self_report_survey_baseform_ModelForm

    def get_context_data(self, **kwargs):
        context = super(Yuan_nei_wen_zhen_diao_cha_biao_CreateView, self).get_context_data(**kwargs)
        customer = Customer.objects.get(user=self.request.user)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1641519651_ModelForm(instance=customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Out_of_hospital_self_report_survey_baseform_ModelForm(self.request.POST, prefix="form1")
            form2 = Men_zhen_wen_zhen_diao_cha_baseform_ModelForm(self.request.POST, prefix="form2")
        else:
            form1 = Out_of_hospital_self_report_survey_baseform_ModelForm(prefix="form1")
            form2 = Men_zhen_wen_zhen_diao_cha_baseform_ModelForm(prefix="form2")
        # context
        context['form0'] = form0
        context['form1'] = form1
        context['form2'] = form2

        context['user'] = self.request.user

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
                
        f = context['form2'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
                
        return super(Yuan_nei_wen_zhen_diao_cha_biao_CreateView, self).form_valid(form)

        
class Chang_gui_cha_ti_biao_CreateView(CreateView):
    template_name = 'chang_gui_cha_ti_biao_edit.html'
    success_url = '/'
    form_class = Vital_signs_check_baseform_ModelForm

    def get_context_data(self, **kwargs):
        context = super(Chang_gui_cha_ti_biao_CreateView, self).get_context_data(**kwargs)
        customer = Customer.objects.get(user=self.request.user)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1641519651_ModelForm(instance=customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Vital_signs_check_baseform_ModelForm(self.request.POST, prefix="form1")
            form2 = Physical_examination_baseform_ModelForm(self.request.POST, prefix="form2")
            form3 = Physical_examination_hearing_baseform_ModelForm(self.request.POST, prefix="form3")
            form4 = Physical_examination_oral_cavity_baseform_ModelForm(self.request.POST, prefix="form4")
            form5 = Physical_examination_vision_baseform_ModelForm(self.request.POST, prefix="form5")
            form6 = Lower_extremity_edema_examination_baseform_ModelForm(self.request.POST, prefix="form6")
            form7 = Physical_examination_athletic_ability_baseform_ModelForm(self.request.POST, prefix="form7")
        else:
            form1 = Vital_signs_check_baseform_ModelForm(prefix="form1")
            form2 = Physical_examination_baseform_ModelForm(prefix="form2")
            form3 = Physical_examination_hearing_baseform_ModelForm(prefix="form3")
            form4 = Physical_examination_oral_cavity_baseform_ModelForm(prefix="form4")
            form5 = Physical_examination_vision_baseform_ModelForm(prefix="form5")
            form6 = Lower_extremity_edema_examination_baseform_ModelForm(prefix="form6")
            form7 = Physical_examination_athletic_ability_baseform_ModelForm(prefix="form7")
        # context
        context['form0'] = form0
        context['form1'] = form1
        context['form2'] = form2
        context['form3'] = form3
        context['form4'] = form4
        context['form5'] = form5
        context['form6'] = form6
        context['form7'] = form7

        context['user'] = self.request.user

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
                
        f = context['form2'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
                
        f = context['form3'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
                
        f = context['form4'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
                
        f = context['form5'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
                
        f = context['form6'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
                
        f = context['form7'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
                
        return super(Chang_gui_cha_ti_biao_CreateView, self).form_valid(form)

        
class Tang_niao_bing_cha_ti_biao_CreateView(CreateView):
    template_name = 'tang_niao_bing_cha_ti_biao_edit.html'
    success_url = '/'
    form_class = Fundus_examination_baseform_ModelForm

    def get_context_data(self, **kwargs):
        context = super(Tang_niao_bing_cha_ti_biao_CreateView, self).get_context_data(**kwargs)
        customer = Customer.objects.get(user=self.request.user)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1641519651_ModelForm(instance=customer, prefix="form0")
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

        context['user'] = self.request.user

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
                
        f = context['form2'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
                
        return super(Tang_niao_bing_cha_ti_biao_CreateView, self).form_valid(form)

        
class Xue_ya_jian_ce_biao_CreateView(CreateView):
    template_name = 'xue_ya_jian_ce_biao_edit.html'
    success_url = '/'
    form_class = Blood_pressure_monitoring_baseform_ModelForm

    def get_context_data(self, **kwargs):
        context = super(Xue_ya_jian_ce_biao_CreateView, self).get_context_data(**kwargs)
        customer = Customer.objects.get(user=self.request.user)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1641519651_ModelForm(instance=customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Blood_pressure_monitoring_baseform_ModelForm(self.request.POST, prefix="form1")
        else:
            form1 = Blood_pressure_monitoring_baseform_ModelForm(prefix="form1")
        # context
        context['form0'] = form0
        context['form1'] = form1

        context['user'] = self.request.user

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
                
        return super(Xue_ya_jian_ce_biao_CreateView, self).form_valid(form)

        
class Kong_fu_xue_tang_jian_cha_biao_CreateView(CreateView):
    template_name = 'kong_fu_xue_tang_jian_cha_biao_edit.html'
    success_url = '/'
    form_class = Kong_fu_xue_tang_jian_cha_baseform_ModelForm

    def get_context_data(self, **kwargs):
        context = super(Kong_fu_xue_tang_jian_cha_biao_CreateView, self).get_context_data(**kwargs)
        customer = Customer.objects.get(user=self.request.user)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1641519651_ModelForm(instance=customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Kong_fu_xue_tang_jian_cha_baseform_ModelForm(self.request.POST, prefix="form1")
        else:
            form1 = Kong_fu_xue_tang_jian_cha_baseform_ModelForm(prefix="form1")
        # context
        context['form0'] = form0
        context['form1'] = form1

        context['user'] = self.request.user

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
                
        return super(Kong_fu_xue_tang_jian_cha_biao_CreateView, self).form_valid(form)

        
class Tang_hua_xue_hong_dan_bai_jian_cha_biao_CreateView(CreateView):
    template_name = 'tang_hua_xue_hong_dan_bai_jian_cha_biao_edit.html'
    success_url = '/'
    form_class = Tang_hua_xue_hong_dan_bai_jian_cha_baseform_ModelForm

    def get_context_data(self, **kwargs):
        context = super(Tang_hua_xue_hong_dan_bai_jian_cha_biao_CreateView, self).get_context_data(**kwargs)
        customer = Customer.objects.get(user=self.request.user)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1641519651_ModelForm(instance=customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Tang_hua_xue_hong_dan_bai_jian_cha_baseform_ModelForm(self.request.POST, prefix="form1")
        else:
            form1 = Tang_hua_xue_hong_dan_bai_jian_cha_baseform_ModelForm(prefix="form1")
        # context
        context['form0'] = form0
        context['form1'] = form1

        context['user'] = self.request.user

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
                
        return super(Tang_hua_xue_hong_dan_bai_jian_cha_biao_CreateView, self).form_valid(form)

        
class Men_zhen_zhen_duan_biao_CreateView(CreateView):
    template_name = 'men_zhen_zhen_duan_biao_edit.html'
    success_url = '/'
    form_class = Men_zhen_zhen_duan_baseform_ModelForm

    def get_context_data(self, **kwargs):
        context = super(Men_zhen_zhen_duan_biao_CreateView, self).get_context_data(**kwargs)
        customer = Customer.objects.get(user=self.request.user)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1641519651_ModelForm(instance=customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Men_zhen_zhen_duan_baseform_ModelForm(self.request.POST, prefix="form1")
        else:
            form1 = Men_zhen_zhen_duan_baseform_ModelForm(prefix="form1")
        # context
        context['form0'] = form0
        context['form1'] = form1

        context['user'] = self.request.user

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
                
        return super(Men_zhen_zhen_duan_biao_CreateView, self).form_valid(form)

        
class Yong_yao_chu_fang_biao_CreateView(CreateView):
    template_name = 'yong_yao_chu_fang_biao_edit.html'
    success_url = '/'
    form_class = Yong_yao_chu_fang_baseform_ModelForm

    def get_context_data(self, **kwargs):
        context = super(Yong_yao_chu_fang_biao_CreateView, self).get_context_data(**kwargs)
        customer = Customer.objects.get(user=self.request.user)
        
        # inquire_forms
        form0 = Basic_personal_information_baseform_query_1641519651_ModelForm(instance=customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Yong_yao_chu_fang_baseform_ModelForm(self.request.POST, prefix="form1")
        else:
            form1 = Yong_yao_chu_fang_baseform_ModelForm(prefix="form1")
        # context
        context['form0'] = form0
        context['form1'] = form1

        context['user'] = self.request.user

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])

        # form_valid
        f = context['form1'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
                
        return super(Yong_yao_chu_fang_biao_CreateView, self).form_valid(form)

        