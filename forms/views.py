from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.forms import modelformset_factory, inlineformset_factory
from core.models import Operation_proc

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


class Test_operation3_CreateView(CreateView):
    template_name = 'test_operation3_edit.html'
    success_url = '/'
    form_class = Out_of_hospital_self_report_survey_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Test_operation3_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        form0 = Basic_personal_information_ModelForm(instance=self.customer, prefix="form0")
        # mutate_formsets
        Formset1 = modelformset_factory(Out_of_hospital_self_report_survey, form=Out_of_hospital_self_report_survey_ModelForm, extra=2)
        # mutate_forms
        if self.request.method == 'POST':
            formset1 = Formset1(self.request.POST, prefix="formset1")
            form2 = Personal_comprehensive_psychological_quality_survey_ModelForm(self.request.POST, prefix="form2")
        else:
            formset1 = Formset1(prefix="formset1")
            form2 = Personal_comprehensive_psychological_quality_survey_ModelForm(prefix="form2")
        # context
        context['form0'] = form0
        context['formset1'] = formset1
        context['form2'] = form2

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid
        for form in context['formset1']:
            f = form.save(commit=False)
            f.customer = self.customer
            f.operator = self.operator
            f.save()
                
        f = context['form2'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        return super(Test_operation3_CreateView, self).form_valid(form)

        
class Test_operation_form3_CreateView(CreateView):
    template_name = 'test_operation_form3_edit.html'
    success_url = '/'
    form_class = Physical_examination_abdomen_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Test_operation_form3_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        form0 = Basic_personal_information_ModelForm(instance=self.customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Physical_examination_abdomen_ModelForm(self.request.POST, prefix="form1")
            form2 = Physical_examination_athletic_ability_ModelForm(self.request.POST, prefix="form2")
            form3 = Physical_examination_oral_cavity_ModelForm(self.request.POST, prefix="form3")
            form4 = Physical_examination_lungs_ModelForm(self.request.POST, prefix="form4")
            form5 = Physical_examination_limbs_ModelForm(self.request.POST, prefix="form5")
            form6 = Physical_examination_skin_ModelForm(self.request.POST, prefix="form6")
        else:
            form1 = Physical_examination_abdomen_ModelForm(prefix="form1")
            form2 = Physical_examination_athletic_ability_ModelForm(prefix="form2")
            form3 = Physical_examination_oral_cavity_ModelForm(prefix="form3")
            form4 = Physical_examination_lungs_ModelForm(prefix="form4")
            form5 = Physical_examination_limbs_ModelForm(prefix="form5")
            form6 = Physical_examination_skin_ModelForm(prefix="form6")
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
                
        return super(Test_operation_form3_CreateView, self).form_valid(form)

        
class Test_CreateView(CreateView):
    template_name = 'test_edit.html'
    success_url = '/'
    form_class = Out_of_hospital_self_report_survey_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Test_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        form0 = Basic_personal_information_ModelForm(instance=self.customer, prefix="form0")
        # mutate_formsets
        Formset1 = modelformset_factory(Out_of_hospital_self_report_survey, form=Out_of_hospital_self_report_survey_ModelForm, extra=2)
        # mutate_forms
        if self.request.method == 'POST':
            formset1 = Formset1(self.request.POST, prefix="formset1")
            form2 = Personal_health_assessment_ModelForm(self.request.POST, prefix="form2")
        else:
            formset1 = Formset1(prefix="formset1")
            form2 = Personal_health_assessment_ModelForm(prefix="form2")
        # context
        context['form0'] = form0
        context['formset1'] = formset1
        context['form2'] = form2

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid
        for form in context['formset1']:
            f = form.save(commit=False)
            f.customer = self.customer
            f.operator = self.operator
            f.save()
                
        f = context['form2'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        return super(Test_CreateView, self).form_valid(form)

        
class Persen_CreateView(CreateView):
    template_name = 'persen_edit.html'
    success_url = '/'
    form_class = Vital_signs_check_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Persen_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        form0 = Family_survey_ModelForm(instance=self.customer, prefix="form0")
        # mutate_formsets
        Formset4 = modelformset_factory(History_of_infectious_diseases, form=History_of_infectious_diseases_ModelForm, extra=2)
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Vital_signs_check_ModelForm(self.request.POST, prefix="form1")
            form2 = Physical_examination_hearing_ModelForm(self.request.POST, prefix="form2")
            form3 = Basic_personal_information_ModelForm(self.request.POST, prefix="form3")
            formset4 = Formset4(self.request.POST, prefix="formset4")
            form5 = Personal_adaptability_assessment_ModelForm(self.request.POST, prefix="form5")
        else:
            form1 = Vital_signs_check_ModelForm(prefix="form1")
            form2 = Physical_examination_hearing_ModelForm(prefix="form2")
            form3 = Basic_personal_information_ModelForm(prefix="form3")
            formset4 = Formset4(prefix="formset4")
            form5 = Personal_adaptability_assessment_ModelForm(prefix="form5")
        # context
        context['form0'] = form0
        context['form1'] = form1
        context['form2'] = form2
        context['form3'] = form3
        context['formset4'] = formset4
        context['form5'] = form5

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
                
        for form in context['formset4']:
            f = form.save(commit=False)
            f.customer = self.customer
            f.operator = self.operator
            f.save()
                
        f = context['form5'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        return super(Persen_CreateView, self).form_valid(form)

        