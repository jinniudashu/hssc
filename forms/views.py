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


class Ge_ren_ji_ben_xin_xi_diao_cha_1638359668_CreateView(CreateView):
    template_name = 'ge_ren_ji_ben_xin_xi_diao_cha_1638359668_edit.html'
    success_url = '/'
    form_class = Ge_ren_ji_ben_xin_xi_1638359483_baseform_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Ge_ren_ji_ben_xin_xi_diao_cha_1638359668_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form0 = Ge_ren_ji_ben_xin_xi_1638359483_baseform_ModelForm(self.request.POST, prefix="form0")
        else:
            form0 = Ge_ren_ji_ben_xin_xi_1638359483_baseform_ModelForm(prefix="form0")
        # context
        context['form0'] = form0

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid
        f = context['form0'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        return super(Ge_ren_ji_ben_xin_xi_diao_cha_1638359668_CreateView, self).form_valid(form)

        
class Ge_ren_ji_bing_shi_1638359691_CreateView(CreateView):
    template_name = 'ge_ren_ji_bing_shi_1638359691_edit.html'
    success_url = '/'
    form_class = Ji_bing_shi_1638359530_baseform_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Ge_ren_ji_bing_shi_1638359691_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        form0 = Ge_ren_ji_ben_xin_xi_1638359483_baseform_query_1638359584_ModelForm(instance=self.customer, prefix="form0")
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form1 = Ji_bing_shi_1638359530_baseform_ModelForm(self.request.POST, prefix="form1")
        else:
            form1 = Ji_bing_shi_1638359530_baseform_ModelForm(prefix="form1")
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
                
        return super(Ge_ren_ji_bing_shi_1638359691_CreateView, self).form_valid(form)

        
class Ge_ren_jian_kang_diao_cha_biao_1638361044_CreateView(CreateView):
    template_name = 'ge_ren_jian_kang_diao_cha_biao_1638361044_edit.html'
    success_url = '/'
    form_class = Ge_ren_ji_ben_xin_xi_1638359483_baseform_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Ge_ren_jian_kang_diao_cha_biao_1638361044_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form0 = Ge_ren_ji_ben_xin_xi_1638359483_baseform_ModelForm(self.request.POST, prefix="form0")
            form1 = Ji_bing_shi_1638359530_baseform_ModelForm(self.request.POST, prefix="form1")
        else:
            form0 = Ge_ren_ji_ben_xin_xi_1638359483_baseform_ModelForm(prefix="form0")
            form1 = Ji_bing_shi_1638359530_baseform_ModelForm(prefix="form1")
        # context
        context['form0'] = form0
        context['form1'] = form1

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
                
        return super(Ge_ren_jian_kang_diao_cha_biao_1638361044_CreateView, self).form_valid(form)

        
class Sfs_1638362066_CreateView(CreateView):
    template_name = 'sfs_1638362066_edit.html'
    success_url = '/'
    form_class = Ge_ren_ji_ben_xin_xi_1638359483_baseform_ModelForm

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super(Sfs_1638362066_CreateView, self).get_context_data(**kwargs)
        
        # inquire_forms
        # mutate_formsets
        # mutate_forms
        if self.request.method == 'POST':
            form0 = Ge_ren_ji_ben_xin_xi_1638359483_baseform_ModelForm(self.request.POST, prefix="form0")
        else:
            form0 = Ge_ren_ji_ben_xin_xi_1638359483_baseform_ModelForm(prefix="form0")
        # context
        context['form0'] = form0

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid
        f = context['form0'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                
        return super(Sfs_1638362066_CreateView, self).form_valid(form)

        