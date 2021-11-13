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


class Test_operation_CreateView(CreateView):
    template_name = 'test_operation_edit.html'
    success_url = '/'
    form_class = Personal_health_assessment_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Test_operation_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        Formset0 = modelformset_factory(History_of_trauma, form=History_of_trauma_ModelForm, extra=2)
        # formset0 = Formset0(queryset=self.customer.history_of_trauma.all(), prefix="formset0")
        formset0 = Formset0(prefix="formset0")
        Formset1 = modelformset_factory(Out_of_hospital_self_report_survey, form=Out_of_hospital_self_report_survey_ModelForm, extra=2)
        # formset1 = Formset1(queryset=self.customer.out_of_hospital_self_report_survey.all(), prefix="formset1")
        formset1 = Formset1(prefix="formset1")
        form2 = Personal_comprehensive_psychological_quality_survey_ModelForm(instance=self.customer, prefix="form2")
        # mutate_formsets
        Formset4 = modelformset_factory(Allergies_history, form=Allergies_history_ModelForm, extra=2)
        Formset5 = modelformset_factory(History_of_blood_transfusion, form=History_of_blood_transfusion_ModelForm, extra=2)
        # mutate_forms
        if self.request.method == 'POST':
            form3 = Personal_health_assessment_ModelForm(self.request.POST, prefix="form3")
            formset4 = Formset4(self.request.POST, prefix="formset4")
            formset5 = Formset5(self.request.POST, prefix="formset5")
        else:
            form3 = Personal_health_assessment_ModelForm(prefix="form3")
            formset4 = Formset4(prefix="formset4")
            formset5 = Formset5(prefix="formset5")
        # context
        context['formset0'] = formset0
        context['formset1'] = formset1
        context['form2'] = form2
        context['form3'] = form3
        context['formset4'] = formset4
        context['formset5'] = formset5

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid
        f = context['form3'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        for form in context['formset4']:
            f = form.save(commit=False)
            f.customer = self.customer
            f.operator = self.operator
            f.save()
                
        for form in context['formset5']:
            f = form.save(commit=False)
            f.customer = self.customer
            f.operator = self.operator
            f.save()
                
        return super(Test_operation_CreateView, self).form_valid(form)

        
class Test2_opera_CreateView(CreateView):
    template_name = 'test2_opera_edit.html'
    success_url = '/'
    form_class = Personal_comprehensive_psychological_quality_survey_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Test2_opera_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        Formset0 = modelformset_factory(Out_of_hospital_self_report_survey, form=Out_of_hospital_self_report_survey_ModelForm, extra=2)
        # formset0 = Formset0(queryset=self.customer.out_of_hospital_self_report_survey.all(), prefix="formset0")
        formset0 = Formset0(prefix="formset0")
        form1 = Personal_health_assessment_ModelForm(instance=self.customer, prefix="form1")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form2 = Personal_comprehensive_psychological_quality_survey_ModelForm(self.request.POST, prefix="form2")
            form3 = Personal_health_behavior_survey_ModelForm(self.request.POST, prefix="form3")
        else:
            form2 = Personal_comprehensive_psychological_quality_survey_ModelForm(prefix="form2")
            form3 = Personal_health_behavior_survey_ModelForm(prefix="form3")
        # context
        context['formset0'] = formset0
        context['form1'] = form1
        context['form2'] = form2
        context['form3'] = form3

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid
        f = context['form2'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        f = context['form3'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        return super(Test2_opera_CreateView, self).form_valid(form)

        