from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.forms import modelformset_factory, inlineformset_factory
import json

from core.models import Operation_proc, Staff, Customer
from core.signals import operand_started, operand_finished
from forms.utils import *
from forms.models import *
from forms.forms import *

class Index_view(ListView):
    model = Operation_proc
    template_name = 'index.html'

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object(queryset=Operation_proc.objects.exclude(state=4))

    def get_context_data(self, **kwargs):
        # 如果用户当前未登录，request.user将被设置为AnonymousUser。用user.is_authenticated()判断用户登录状态：
        operator=Staff.objects.get(user=self.request.user)
        group = Group.objects.filter(user=self.request.user)
        # 获取当前用户所属角色组的所有作业进程
        procs = Operation_proc.objects.exclude(state=4).filter(Q(group__in=group) | Q(operator=operator)).distinct()

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


class Chang_gui_cha_ti_biao_CreateView(CreateView):
    model = A3110
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Chang_gui_cha_ti_biao_CreateView, self).get_context_data(**kwargs)
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A3110_ModelForm(self.request.POST, prefix="attribute_form0")
            attribute_form1 = A3109_ModelForm(self.request.POST, prefix="attribute_form1")
            attribute_form2 = A3108_ModelForm(self.request.POST, prefix="attribute_form2")
            attribute_form3 = A6502_ModelForm(self.request.POST, prefix="attribute_form3")
            attribute_form4 = A3001_ModelForm(self.request.POST, prefix="attribute_form4")
        else:
            attribute_form0 = A3110_ModelForm(prefix="attribute_form0")
            attribute_form1 = A3109_ModelForm(prefix="attribute_form1")
            attribute_form2 = A3108_ModelForm(prefix="attribute_form2")
            attribute_form3 = A6502_ModelForm(prefix="attribute_form3")
            attribute_form4 = A3001_ModelForm(prefix="attribute_form4")
        # context
        context['base_form'] = base_form
        context['attribute_form0'] = attribute_form0
        context['attribute_form1'] = attribute_form1
        context['attribute_form2'] = attribute_form2
        context['attribute_form3'] = attribute_form3
        context['attribute_form4'] = attribute_form4
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['attribute_form0'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['attribute_form1'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['attribute_form2'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['attribute_form3'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['attribute_form4'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Chang_gui_cha_ti_biao_CreateView, self).form_valid(form)

class Tang_niao_bing_cha_ti_biao_CreateView(CreateView):
    model = Tang_niao_bing_cha_ti_biao
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Tang_niao_bing_cha_ti_biao_CreateView, self).get_context_data(**kwargs)
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = Tang_niao_bing_cha_ti_biao_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            attribute_form0 = Tang_niao_bing_cha_ti_biao_ModelForm(prefix="attribute_form0")
        # context
        context['base_form'] = base_form
        context['attribute_form0'] = attribute_form0
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['attribute_form0'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Tang_niao_bing_cha_ti_biao_CreateView, self).form_valid(form)

class Men_zhen_chu_fang_biao_CreateView(CreateView):
    model = A5001
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Men_zhen_chu_fang_biao_CreateView, self).get_context_data(**kwargs)
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A5001_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            attribute_form0 = A5001_ModelForm(prefix="attribute_form0")
        # context
        context['base_form'] = base_form
        context['attribute_form0'] = attribute_form0
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['attribute_form0'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Men_zhen_chu_fang_biao_CreateView, self).form_valid(form)

class User_registry_CreateView(CreateView):
    model = Z6201
    context = {}

    def get_context_data(self, **kwargs):
        context = super(User_registry_CreateView, self).get_context_data(**kwargs)
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = Z6201_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            attribute_form0 = Z6201_ModelForm(prefix="attribute_form0")
        # context
        context['base_form'] = base_form
        context['attribute_form0'] = attribute_form0
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['attribute_form0'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(User_registry_CreateView, self).form_valid(form)

class User_login_CreateView(CreateView):
    model = Z6230
    context = {}

    def get_context_data(self, **kwargs):
        context = super(User_login_CreateView, self).get_context_data(**kwargs)
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = Z6230_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            attribute_form0 = Z6230_ModelForm(prefix="attribute_form0")
        # context
        context['base_form'] = base_form
        context['attribute_form0'] = attribute_form0
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['attribute_form0'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(User_login_CreateView, self).form_valid(form)

class Doctor_login_CreateView(CreateView):
    model = Z6230
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Doctor_login_CreateView, self).get_context_data(**kwargs)
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = Z6230_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            attribute_form0 = Z6230_ModelForm(prefix="attribute_form0")
        # context
        context['base_form'] = base_form
        context['attribute_form0'] = attribute_form0
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['attribute_form0'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Doctor_login_CreateView, self).form_valid(form)

class A6501_CreateView(CreateView):
    model = A6501
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A6501_CreateView, self).get_context_data(**kwargs)
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A6501_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            attribute_form0 = A6501_ModelForm(prefix="attribute_form0")
        # context
        context['base_form'] = base_form
        context['attribute_form0'] = attribute_form0
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['attribute_form0'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A6501_CreateView, self).form_valid(form)

class Men_zhen_fu_zhu_jian_cha_CreateView(CreateView):
    model = A3001
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Men_zhen_fu_zhu_jian_cha_CreateView, self).get_context_data(**kwargs)
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A3001_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            attribute_form0 = A3001_ModelForm(prefix="attribute_form0")
        # context
        context['base_form'] = base_form
        context['attribute_form0'] = attribute_form0
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['attribute_form0'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Men_zhen_fu_zhu_jian_cha_CreateView, self).form_valid(form)

class Tang_niao_bing_zhuan_yong_wen_zhen_CreateView(CreateView):
    model = A6219
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Tang_niao_bing_zhuan_yong_wen_zhen_CreateView, self).get_context_data(**kwargs)
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A6219_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            attribute_form0 = A6219_ModelForm(prefix="attribute_form0")
        # context
        context['base_form'] = base_form
        context['attribute_form0'] = attribute_form0
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['attribute_form0'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Tang_niao_bing_zhuan_yong_wen_zhen_CreateView, self).form_valid(form)

class Yao_shi_fu_wu_CreateView(CreateView):
    model = A5002
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Yao_shi_fu_wu_CreateView, self).get_context_data(**kwargs)
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A5002_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            attribute_form0 = A5002_ModelForm(prefix="attribute_form0")
        # context
        context['base_form'] = base_form
        context['attribute_form0'] = attribute_form0
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['attribute_form0'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Yao_shi_fu_wu_CreateView, self).form_valid(form)

class Tang_niao_bing_zi_wo_jian_ce_CreateView(CreateView):
    model = T4505
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Tang_niao_bing_zi_wo_jian_ce_CreateView, self).get_context_data(**kwargs)
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = T4505_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            attribute_form0 = T4505_ModelForm(prefix="attribute_form0")
        # context
        context['base_form'] = base_form
        context['attribute_form0'] = attribute_form0
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['attribute_form0'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Tang_niao_bing_zi_wo_jian_ce_CreateView, self).form_valid(form)

class Yuan_nei_fu_zhu_wen_zhen_CreateView(CreateView):
    model = A6217
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Yuan_nei_fu_zhu_wen_zhen_CreateView, self).get_context_data(**kwargs)
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A6217_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            attribute_form0 = A6217_ModelForm(prefix="attribute_form0")
        # context
        context['base_form'] = base_form
        context['attribute_form0'] = attribute_form0
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['attribute_form0'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Yuan_nei_fu_zhu_wen_zhen_CreateView, self).form_valid(form)

class A6201_CreateView(CreateView):
    model = A6201
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A6201_CreateView, self).get_context_data(**kwargs)
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A6201_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            attribute_form0 = A6201_ModelForm(prefix="attribute_form0")
        # context
        context['base_form'] = base_form
        context['attribute_form0'] = attribute_form0
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['attribute_form0'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A6201_CreateView, self).form_valid(form)

class Men_zhen_yi_sheng_wen_zhen_CreateView(CreateView):
    model = A6218
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Men_zhen_yi_sheng_wen_zhen_CreateView, self).get_context_data(**kwargs)
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A6218_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            attribute_form0 = A6218_ModelForm(prefix="attribute_form0")
        # context
        context['base_form'] = base_form
        context['attribute_form0'] = attribute_form0
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['attribute_form0'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Men_zhen_yi_sheng_wen_zhen_CreateView, self).form_valid(form)

class T8901_CreateView(CreateView):
    model = Tang_niao_bing_zhen_duan_biao
    context = {}

    def get_context_data(self, **kwargs):
        context = super(T8901_CreateView, self).get_context_data(**kwargs)
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = Tang_niao_bing_zhen_duan_biao_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            attribute_form0 = Tang_niao_bing_zhen_duan_biao_ModelForm(prefix="attribute_form0")
        # context
        context['base_form'] = base_form
        context['attribute_form0'] = attribute_form0
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['attribute_form0'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(T8901_CreateView, self).form_valid(form)

class T6301_CreateView(CreateView):
    model = T6301
    context = {}

    def get_context_data(self, **kwargs):
        context = super(T6301_CreateView, self).get_context_data(**kwargs)
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = T6301_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            attribute_form0 = T6301_ModelForm(prefix="attribute_form0")
        # context
        context['base_form'] = base_form
        context['attribute_form0'] = attribute_form0
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['attribute_form0'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(T6301_CreateView, self).form_valid(form)

class A6202_CreateView(CreateView):
    model = A6202
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A6202_CreateView, self).get_context_data(**kwargs)
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A6202_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            attribute_form0 = A6202_ModelForm(prefix="attribute_form0")
        # context
        context['base_form'] = base_form
        context['attribute_form0'] = attribute_form0
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['attribute_form0'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A6202_CreateView, self).form_valid(form)

class A6220_CreateView(CreateView):
    model = A6220
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A6220_CreateView, self).get_context_data(**kwargs)
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A6220_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            attribute_form0 = A6220_ModelForm(prefix="attribute_form0")
        # context
        context['base_form'] = base_form
        context['attribute_form0'] = attribute_form0
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['attribute_form0'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A6220_CreateView, self).form_valid(form)

class A6299_CreateView(CreateView):
    model = A6203
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A6299_CreateView, self).get_context_data(**kwargs)
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A6203_ModelForm(self.request.POST, prefix="attribute_form0")
            attribute_form1 = A6210_ModelForm(self.request.POST, prefix="attribute_form1")
            attribute_form2 = A6207_ModelForm(self.request.POST, prefix="attribute_form2")
            attribute_form3 = A6209_ModelForm(self.request.POST, prefix="attribute_form3")
            attribute_form4 = A6205_ModelForm(self.request.POST, prefix="attribute_form4")
            attribute_form5 = A6204_ModelForm(self.request.POST, prefix="attribute_form5")
            attribute_form6 = A6206_ModelForm(self.request.POST, prefix="attribute_form6")
            attribute_form7 = A6208_ModelForm(self.request.POST, prefix="attribute_form7")
            attribute_form8 = A6213_ModelForm(self.request.POST, prefix="attribute_form8")
            attribute_form9 = A6215_ModelForm(self.request.POST, prefix="attribute_form9")
            attribute_form10 = A6214_ModelForm(self.request.POST, prefix="attribute_form10")
            attribute_form11 = A6212_ModelForm(self.request.POST, prefix="attribute_form11")
            attribute_form12 = A6216_ModelForm(self.request.POST, prefix="attribute_form12")
        else:
            attribute_form0 = A6203_ModelForm(prefix="attribute_form0")
            attribute_form1 = A6210_ModelForm(prefix="attribute_form1")
            attribute_form2 = A6207_ModelForm(prefix="attribute_form2")
            attribute_form3 = A6209_ModelForm(prefix="attribute_form3")
            attribute_form4 = A6205_ModelForm(prefix="attribute_form4")
            attribute_form5 = A6204_ModelForm(prefix="attribute_form5")
            attribute_form6 = A6206_ModelForm(prefix="attribute_form6")
            attribute_form7 = A6208_ModelForm(prefix="attribute_form7")
            attribute_form8 = A6213_ModelForm(prefix="attribute_form8")
            attribute_form9 = A6215_ModelForm(prefix="attribute_form9")
            attribute_form10 = A6214_ModelForm(prefix="attribute_form10")
            attribute_form11 = A6212_ModelForm(prefix="attribute_form11")
            attribute_form12 = A6216_ModelForm(prefix="attribute_form12")
        # context
        context['base_form'] = base_form
        context['attribute_form0'] = attribute_form0
        context['attribute_form1'] = attribute_form1
        context['attribute_form2'] = attribute_form2
        context['attribute_form3'] = attribute_form3
        context['attribute_form4'] = attribute_form4
        context['attribute_form5'] = attribute_form5
        context['attribute_form6'] = attribute_form6
        context['attribute_form7'] = attribute_form7
        context['attribute_form8'] = attribute_form8
        context['attribute_form9'] = attribute_form9
        context['attribute_form10'] = attribute_form10
        context['attribute_form11'] = attribute_form11
        context['attribute_form12'] = attribute_form12
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['attribute_form0'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['attribute_form1'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['attribute_form2'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['attribute_form3'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['attribute_form4'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['attribute_form5'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['attribute_form6'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['attribute_form7'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['attribute_form8'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['attribute_form9'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['attribute_form10'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['attribute_form11'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['attribute_form12'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A6299_CreateView, self).form_valid(form)

class A3502_CreateView(CreateView):
    model = A3502
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A3502_CreateView, self).get_context_data(**kwargs)
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A3502_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            attribute_form0 = A3502_ModelForm(prefix="attribute_form0")
        # context
        context['base_form'] = base_form
        context['attribute_form0'] = attribute_form0
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['attribute_form0'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A3502_CreateView, self).form_valid(form)
