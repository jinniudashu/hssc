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


class Test_operation_CreateView(CreateView):
    template_name = 'test_operation_edit.html'
    success_url = '/'
    form_class = Personal_health_behavior_survey_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Test_operation_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        form0 = Basic_personal_information_ModelForm(instance=self.customer, prefix="form0")
        Formset1 = modelformset_factory(History_of_infectious_diseases, form=History_of_infectious_diseases_ModelForm, extra=2)
        # formset1 = Formset1(queryset=self.customer.history_of_infectious_diseases.all(), prefix="formset1")
        formset1 = Formset1(prefix="formset1")
        # mutate_formsets
        Formset3 = modelformset_factory(History_of_blood_transfusion, form=History_of_blood_transfusion_ModelForm, extra=2)
        # mutate_forms
        if self.request.method == 'POST':
            form2 = Personal_health_behavior_survey_ModelForm(self.request.POST, prefix="form2")
            formset3 = Formset3(self.request.POST, prefix="formset3")
        else:
            form2 = Personal_health_behavior_survey_ModelForm(prefix="form2")
            formset3 = Formset3(prefix="formset3")
        # context
        context['form0'] = form0
        context['formset1'] = formset1
        context['form2'] = form2
        context['formset3'] = formset3

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid
        f = context['form2'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        for form in context['formset3']:
            f = form.save(commit=False)
            f.customer = self.customer
            f.operator = self.operator
            f.save()
                
        return super(Test_operation_CreateView, self).form_valid(form)

        