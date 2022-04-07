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
    success_url = 'forms/'
    template_name = 'chang_gui_cha_ti_biao_create.html'
    form_class = A3110_ModelForm # the first form ModelForm class
    model = A3110
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Chang_gui_cha_ti_biao_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")

            attribute_form0 = A3110_ModelForm(self.request.POST, prefix="attribute_form0")
            attribute_form1 = A3109_ModelForm(self.request.POST, prefix="attribute_form1")
            attribute_form2 = A3108_ModelForm(self.request.POST, prefix="attribute_form2")
            attribute_form3 = A6502_ModelForm(self.request.POST, prefix="attribute_form3")
            attribute_form4 = A3001_ModelForm(self.request.POST, prefix="attribute_form4")
        else:
            base_form = A6203_ModelForm(prefix="base_form")

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



class Chang_gui_cha_ti_biao_UpdateView(UpdateView):
    success_url = 'forms/'
    template_name = 'chang_gui_cha_ti_biao_update.html'
    form_class = A3110_ModelForm # the first form ModelForm class
    model = A3110

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    # # 构造作业开始消息参数
    # operand_started.send(sender=self, operation_proc=operation_proc, ocode='rtr', operator=self.request.user)

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Chang_gui_cha_ti_biao_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A3110_ModelForm(self.request.POST, prefix="attribute_form0")
            attribute_form1 = A3109_ModelForm(self.request.POST, prefix="attribute_form1")
            attribute_form2 = A3108_ModelForm(self.request.POST, prefix="attribute_form2")
            attribute_form3 = A6502_ModelForm(self.request.POST, prefix="attribute_form3")
            attribute_form4 = A3001_ModelForm(self.request.POST, prefix="attribute_form4")
            # 构造作业完成消息参数
            operand_finished.send(sender=self, pid=kwargs['id'], ocode='rtc', field_values=self.request.POST)
            return redirect(reverse('index'))
        else:
            attribute_form0 = A3110_ModelForm(instance=A3110.objects.get(pid=kwargs['id']), prefix="attribute_form0")
            attribute_form1 = A3109_ModelForm(instance=A3109.objects.get(pid=kwargs['id']), prefix="attribute_form1")
            attribute_form2 = A3108_ModelForm(instance=A3108.objects.get(pid=kwargs['id']), prefix="attribute_form2")
            attribute_form3 = A6502_ModelForm(instance=A6502.objects.get(pid=kwargs['id']), prefix="attribute_form3")
            attribute_form4 = A3001_ModelForm(instance=A3001.objects.get(pid=kwargs['id']), prefix="attribute_form4")
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
    success_url = 'forms/'
    template_name = 'tang_niao_bing_cha_ti_biao_create.html'
    form_class = Tang_niao_bing_cha_ti_biao_ModelForm # the first form ModelForm class
    model = Tang_niao_bing_cha_ti_biao
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Tang_niao_bing_cha_ti_biao_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")

            attribute_form0 = Tang_niao_bing_cha_ti_biao_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            base_form = A6203_ModelForm(prefix="base_form")

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



class Tang_niao_bing_cha_ti_biao_UpdateView(UpdateView):
    success_url = 'forms/'
    template_name = 'tang_niao_bing_cha_ti_biao_update.html'
    form_class = Tang_niao_bing_cha_ti_biao_ModelForm # the first form ModelForm class
    model = Tang_niao_bing_cha_ti_biao

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    # # 构造作业开始消息参数
    # operand_started.send(sender=self, operation_proc=operation_proc, ocode='rtr', operator=self.request.user)

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Tang_niao_bing_cha_ti_biao_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = Tang_niao_bing_cha_ti_biao_ModelForm(self.request.POST, prefix="attribute_form0")
            # 构造作业完成消息参数
            operand_finished.send(sender=self, pid=kwargs['id'], ocode='rtc', field_values=self.request.POST)
            return redirect(reverse('index'))
        else:
            attribute_form0 = Tang_niao_bing_cha_ti_biao_ModelForm(instance=Tang_niao_bing_cha_ti_biao.objects.get(pid=kwargs['id']), prefix="attribute_form0")
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
    success_url = 'forms/'
    template_name = 'men_zhen_chu_fang_biao_create.html'
    form_class = A5001_ModelForm # the first form ModelForm class
    model = A5001
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Men_zhen_chu_fang_biao_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")

            attribute_form0 = A5001_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            base_form = A6203_ModelForm(prefix="base_form")

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



class Men_zhen_chu_fang_biao_UpdateView(UpdateView):
    success_url = 'forms/'
    template_name = 'men_zhen_chu_fang_biao_update.html'
    form_class = A5001_ModelForm # the first form ModelForm class
    model = A5001

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    # # 构造作业开始消息参数
    # operand_started.send(sender=self, operation_proc=operation_proc, ocode='rtr', operator=self.request.user)

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Men_zhen_chu_fang_biao_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A5001_ModelForm(self.request.POST, prefix="attribute_form0")
            # 构造作业完成消息参数
            operand_finished.send(sender=self, pid=kwargs['id'], ocode='rtc', field_values=self.request.POST)
            return redirect(reverse('index'))
        else:
            attribute_form0 = A5001_ModelForm(instance=A5001.objects.get(pid=kwargs['id']), prefix="attribute_form0")
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
    success_url = 'forms/'
    template_name = 'user_registry_create.html'
    form_class = Z6201_ModelForm # the first form ModelForm class
    model = Z6201
    context = {}

    def get_context_data(self, **kwargs):
        context = super(User_registry_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")

            attribute_form0 = Z6201_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            base_form = A6203_ModelForm(prefix="base_form")

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



class User_registry_UpdateView(UpdateView):
    success_url = 'forms/'
    template_name = 'user_registry_update.html'
    form_class = Z6201_ModelForm # the first form ModelForm class
    model = Z6201

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    # # 构造作业开始消息参数
    # operand_started.send(sender=self, operation_proc=operation_proc, ocode='rtr', operator=self.request.user)

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(User_registry_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = Z6201_ModelForm(self.request.POST, prefix="attribute_form0")
            # 构造作业完成消息参数
            operand_finished.send(sender=self, pid=kwargs['id'], ocode='rtc', field_values=self.request.POST)
            return redirect(reverse('index'))
        else:
            attribute_form0 = Z6201_ModelForm(instance=Z6201.objects.get(pid=kwargs['id']), prefix="attribute_form0")
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
    success_url = 'forms/'
    template_name = 'user_login_create.html'
    form_class = Z6230_ModelForm # the first form ModelForm class
    model = Z6230
    context = {}

    def get_context_data(self, **kwargs):
        context = super(User_login_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")

            attribute_form0 = Z6230_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            base_form = A6203_ModelForm(prefix="base_form")

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



class User_login_UpdateView(UpdateView):
    success_url = 'forms/'
    template_name = 'user_login_update.html'
    form_class = Z6230_ModelForm # the first form ModelForm class
    model = Z6230

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    # # 构造作业开始消息参数
    # operand_started.send(sender=self, operation_proc=operation_proc, ocode='rtr', operator=self.request.user)

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(User_login_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = Z6230_ModelForm(self.request.POST, prefix="attribute_form0")
            # 构造作业完成消息参数
            operand_finished.send(sender=self, pid=kwargs['id'], ocode='rtc', field_values=self.request.POST)
            return redirect(reverse('index'))
        else:
            attribute_form0 = Z6230_ModelForm(instance=Z6230.objects.get(pid=kwargs['id']), prefix="attribute_form0")
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
    success_url = 'forms/'
    template_name = 'doctor_login_create.html'
    form_class = Z6230_ModelForm # the first form ModelForm class
    model = Z6230
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Doctor_login_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")

            attribute_form0 = Z6230_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            base_form = A6203_ModelForm(prefix="base_form")

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



class Doctor_login_UpdateView(UpdateView):
    success_url = 'forms/'
    template_name = 'doctor_login_update.html'
    form_class = Z6230_ModelForm # the first form ModelForm class
    model = Z6230

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    # # 构造作业开始消息参数
    # operand_started.send(sender=self, operation_proc=operation_proc, ocode='rtr', operator=self.request.user)

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Doctor_login_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = Z6230_ModelForm(self.request.POST, prefix="attribute_form0")
            # 构造作业完成消息参数
            operand_finished.send(sender=self, pid=kwargs['id'], ocode='rtc', field_values=self.request.POST)
            return redirect(reverse('index'))
        else:
            attribute_form0 = Z6230_ModelForm(instance=Z6230.objects.get(pid=kwargs['id']), prefix="attribute_form0")
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
    success_url = 'forms/'
    template_name = 'A6501_create.html'
    form_class = A6501_ModelForm # the first form ModelForm class
    model = A6501
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A6501_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")

            attribute_form0 = A6501_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            base_form = A6203_ModelForm(prefix="base_form")

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



class A6501_UpdateView(UpdateView):
    success_url = 'forms/'
    template_name = 'A6501_update.html'
    form_class = A6501_ModelForm # the first form ModelForm class
    model = A6501

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    # # 构造作业开始消息参数
    # operand_started.send(sender=self, operation_proc=operation_proc, ocode='rtr', operator=self.request.user)

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(A6501_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A6501_ModelForm(self.request.POST, prefix="attribute_form0")
            # 构造作业完成消息参数
            operand_finished.send(sender=self, pid=kwargs['id'], ocode='rtc', field_values=self.request.POST)
            return redirect(reverse('index'))
        else:
            attribute_form0 = A6501_ModelForm(instance=A6501.objects.get(pid=kwargs['id']), prefix="attribute_form0")
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
    success_url = 'forms/'
    template_name = 'men_zhen_fu_zhu_jian_cha_create.html'
    form_class = A3001_ModelForm # the first form ModelForm class
    model = A3001
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Men_zhen_fu_zhu_jian_cha_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")

            attribute_form0 = A3001_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            base_form = A6203_ModelForm(prefix="base_form")

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



class Men_zhen_fu_zhu_jian_cha_UpdateView(UpdateView):
    success_url = 'forms/'
    template_name = 'men_zhen_fu_zhu_jian_cha_update.html'
    form_class = A3001_ModelForm # the first form ModelForm class
    model = A3001

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    # # 构造作业开始消息参数
    # operand_started.send(sender=self, operation_proc=operation_proc, ocode='rtr', operator=self.request.user)

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Men_zhen_fu_zhu_jian_cha_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A3001_ModelForm(self.request.POST, prefix="attribute_form0")
            # 构造作业完成消息参数
            operand_finished.send(sender=self, pid=kwargs['id'], ocode='rtc', field_values=self.request.POST)
            return redirect(reverse('index'))
        else:
            attribute_form0 = A3001_ModelForm(instance=A3001.objects.get(pid=kwargs['id']), prefix="attribute_form0")
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
    success_url = 'forms/'
    template_name = 'tang_niao_bing_zhuan_yong_wen_zhen_create.html'
    form_class = A6219_ModelForm # the first form ModelForm class
    model = A6219
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Tang_niao_bing_zhuan_yong_wen_zhen_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")

            attribute_form0 = A6219_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            base_form = A6203_ModelForm(prefix="base_form")

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



class Tang_niao_bing_zhuan_yong_wen_zhen_UpdateView(UpdateView):
    success_url = 'forms/'
    template_name = 'tang_niao_bing_zhuan_yong_wen_zhen_update.html'
    form_class = A6219_ModelForm # the first form ModelForm class
    model = A6219

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    # # 构造作业开始消息参数
    # operand_started.send(sender=self, operation_proc=operation_proc, ocode='rtr', operator=self.request.user)

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Tang_niao_bing_zhuan_yong_wen_zhen_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A6219_ModelForm(self.request.POST, prefix="attribute_form0")
            # 构造作业完成消息参数
            operand_finished.send(sender=self, pid=kwargs['id'], ocode='rtc', field_values=self.request.POST)
            return redirect(reverse('index'))
        else:
            attribute_form0 = A6219_ModelForm(instance=A6219.objects.get(pid=kwargs['id']), prefix="attribute_form0")
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
    success_url = 'forms/'
    template_name = 'yao_shi_fu_wu_create.html'
    form_class = A5002_ModelForm # the first form ModelForm class
    model = A5002
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Yao_shi_fu_wu_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")

            attribute_form0 = A5002_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            base_form = A6203_ModelForm(prefix="base_form")

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



class Yao_shi_fu_wu_UpdateView(UpdateView):
    success_url = 'forms/'
    template_name = 'yao_shi_fu_wu_update.html'
    form_class = A5002_ModelForm # the first form ModelForm class
    model = A5002

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    # # 构造作业开始消息参数
    # operand_started.send(sender=self, operation_proc=operation_proc, ocode='rtr', operator=self.request.user)

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Yao_shi_fu_wu_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A5002_ModelForm(self.request.POST, prefix="attribute_form0")
            # 构造作业完成消息参数
            operand_finished.send(sender=self, pid=kwargs['id'], ocode='rtc', field_values=self.request.POST)
            return redirect(reverse('index'))
        else:
            attribute_form0 = A5002_ModelForm(instance=A5002.objects.get(pid=kwargs['id']), prefix="attribute_form0")
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
    success_url = 'forms/'
    template_name = 'tang_niao_bing_zi_wo_jian_ce_create.html'
    form_class = T4505_ModelForm # the first form ModelForm class
    model = T4505
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Tang_niao_bing_zi_wo_jian_ce_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")

            attribute_form0 = T4505_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            base_form = A6203_ModelForm(prefix="base_form")

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



class Tang_niao_bing_zi_wo_jian_ce_UpdateView(UpdateView):
    success_url = 'forms/'
    template_name = 'tang_niao_bing_zi_wo_jian_ce_update.html'
    form_class = T4505_ModelForm # the first form ModelForm class
    model = T4505

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    # # 构造作业开始消息参数
    # operand_started.send(sender=self, operation_proc=operation_proc, ocode='rtr', operator=self.request.user)

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Tang_niao_bing_zi_wo_jian_ce_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = T4505_ModelForm(self.request.POST, prefix="attribute_form0")
            # 构造作业完成消息参数
            operand_finished.send(sender=self, pid=kwargs['id'], ocode='rtc', field_values=self.request.POST)
            return redirect(reverse('index'))
        else:
            attribute_form0 = T4505_ModelForm(instance=T4505.objects.get(pid=kwargs['id']), prefix="attribute_form0")
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
    success_url = 'forms/'
    template_name = 'yuan_nei_fu_zhu_wen_zhen_create.html'
    form_class = A6217_ModelForm # the first form ModelForm class
    model = A6217
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Yuan_nei_fu_zhu_wen_zhen_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")

            attribute_form0 = A6217_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            base_form = A6203_ModelForm(prefix="base_form")

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



class Yuan_nei_fu_zhu_wen_zhen_UpdateView(UpdateView):
    success_url = 'forms/'
    template_name = 'yuan_nei_fu_zhu_wen_zhen_update.html'
    form_class = A6217_ModelForm # the first form ModelForm class
    model = A6217

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    # # 构造作业开始消息参数
    # operand_started.send(sender=self, operation_proc=operation_proc, ocode='rtr', operator=self.request.user)

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Yuan_nei_fu_zhu_wen_zhen_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A6217_ModelForm(self.request.POST, prefix="attribute_form0")
            # 构造作业完成消息参数
            operand_finished.send(sender=self, pid=kwargs['id'], ocode='rtc', field_values=self.request.POST)
            return redirect(reverse('index'))
        else:
            attribute_form0 = A6217_ModelForm(instance=A6217.objects.get(pid=kwargs['id']), prefix="attribute_form0")
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
    success_url = 'forms/'
    template_name = 'A6201_create.html'
    form_class = A6201_ModelForm # the first form ModelForm class
    model = A6201
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A6201_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")

            attribute_form0 = A6201_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            base_form = A6203_ModelForm(prefix="base_form")

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



class A6201_UpdateView(UpdateView):
    success_url = 'forms/'
    template_name = 'A6201_update.html'
    form_class = A6201_ModelForm # the first form ModelForm class
    model = A6201

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    # # 构造作业开始消息参数
    # operand_started.send(sender=self, operation_proc=operation_proc, ocode='rtr', operator=self.request.user)

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(A6201_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A6201_ModelForm(self.request.POST, prefix="attribute_form0")
            # 构造作业完成消息参数
            operand_finished.send(sender=self, pid=kwargs['id'], ocode='rtc', field_values=self.request.POST)
            return redirect(reverse('index'))
        else:
            attribute_form0 = A6201_ModelForm(instance=A6201.objects.get(pid=kwargs['id']), prefix="attribute_form0")
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
    success_url = 'forms/'
    template_name = 'men_zhen_yi_sheng_wen_zhen_create.html'
    form_class = A6218_ModelForm # the first form ModelForm class
    model = A6218
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Men_zhen_yi_sheng_wen_zhen_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")

            attribute_form0 = A6218_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            base_form = A6203_ModelForm(prefix="base_form")

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



class Men_zhen_yi_sheng_wen_zhen_UpdateView(UpdateView):
    success_url = 'forms/'
    template_name = 'men_zhen_yi_sheng_wen_zhen_update.html'
    form_class = A6218_ModelForm # the first form ModelForm class
    model = A6218

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    # # 构造作业开始消息参数
    # operand_started.send(sender=self, operation_proc=operation_proc, ocode='rtr', operator=self.request.user)

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Men_zhen_yi_sheng_wen_zhen_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A6218_ModelForm(self.request.POST, prefix="attribute_form0")
            # 构造作业完成消息参数
            operand_finished.send(sender=self, pid=kwargs['id'], ocode='rtc', field_values=self.request.POST)
            return redirect(reverse('index'))
        else:
            attribute_form0 = A6218_ModelForm(instance=A6218.objects.get(pid=kwargs['id']), prefix="attribute_form0")
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
    success_url = 'forms/'
    template_name = 'T8901_create.html'
    form_class = Tang_niao_bing_zhen_duan_biao_ModelForm # the first form ModelForm class
    model = Tang_niao_bing_zhen_duan_biao
    context = {}

    def get_context_data(self, **kwargs):
        context = super(T8901_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")

            attribute_form0 = Tang_niao_bing_zhen_duan_biao_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            base_form = A6203_ModelForm(prefix="base_form")

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



class T8901_UpdateView(UpdateView):
    success_url = 'forms/'
    template_name = 'T8901_update.html'
    form_class = Tang_niao_bing_zhen_duan_biao_ModelForm # the first form ModelForm class
    model = Tang_niao_bing_zhen_duan_biao

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    # # 构造作业开始消息参数
    # operand_started.send(sender=self, operation_proc=operation_proc, ocode='rtr', operator=self.request.user)

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(T8901_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = Tang_niao_bing_zhen_duan_biao_ModelForm(self.request.POST, prefix="attribute_form0")
            # 构造作业完成消息参数
            operand_finished.send(sender=self, pid=kwargs['id'], ocode='rtc', field_values=self.request.POST)
            return redirect(reverse('index'))
        else:
            attribute_form0 = Tang_niao_bing_zhen_duan_biao_ModelForm(instance=Tang_niao_bing_zhen_duan_biao.objects.get(pid=kwargs['id']), prefix="attribute_form0")
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
    success_url = 'forms/'
    template_name = 'T6301_create.html'
    form_class = T6301_ModelForm # the first form ModelForm class
    model = T6301
    context = {}

    def get_context_data(self, **kwargs):
        context = super(T6301_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")

            attribute_form0 = T6301_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            base_form = A6203_ModelForm(prefix="base_form")

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



class T6301_UpdateView(UpdateView):
    success_url = 'forms/'
    template_name = 'T6301_update.html'
    form_class = T6301_ModelForm # the first form ModelForm class
    model = T6301

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    # # 构造作业开始消息参数
    # operand_started.send(sender=self, operation_proc=operation_proc, ocode='rtr', operator=self.request.user)

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(T6301_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = T6301_ModelForm(self.request.POST, prefix="attribute_form0")
            # 构造作业完成消息参数
            operand_finished.send(sender=self, pid=kwargs['id'], ocode='rtc', field_values=self.request.POST)
            return redirect(reverse('index'))
        else:
            attribute_form0 = T6301_ModelForm(instance=T6301.objects.get(pid=kwargs['id']), prefix="attribute_form0")
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
    success_url = 'forms/'
    template_name = 'A6202_create.html'
    form_class = A6202_ModelForm # the first form ModelForm class
    model = A6202
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A6202_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")

            attribute_form0 = A6202_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            base_form = A6203_ModelForm(prefix="base_form")

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



class A6202_UpdateView(UpdateView):
    success_url = 'forms/'
    template_name = 'A6202_update.html'
    form_class = A6202_ModelForm # the first form ModelForm class
    model = A6202

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    # # 构造作业开始消息参数
    # operand_started.send(sender=self, operation_proc=operation_proc, ocode='rtr', operator=self.request.user)

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(A6202_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A6202_ModelForm(self.request.POST, prefix="attribute_form0")
            # 构造作业完成消息参数
            operand_finished.send(sender=self, pid=kwargs['id'], ocode='rtc', field_values=self.request.POST)
            return redirect(reverse('index'))
        else:
            attribute_form0 = A6202_ModelForm(instance=A6202.objects.get(pid=kwargs['id']), prefix="attribute_form0")
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
    success_url = 'forms/'
    template_name = 'A6220_create.html'
    form_class = A6220_ModelForm # the first form ModelForm class
    model = A6220
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A6220_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")

            attribute_form0 = A6220_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            base_form = A6203_ModelForm(prefix="base_form")

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



class A6220_UpdateView(UpdateView):
    success_url = 'forms/'
    template_name = 'A6220_update.html'
    form_class = A6220_ModelForm # the first form ModelForm class
    model = A6220

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    # # 构造作业开始消息参数
    # operand_started.send(sender=self, operation_proc=operation_proc, ocode='rtr', operator=self.request.user)

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(A6220_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A6220_ModelForm(self.request.POST, prefix="attribute_form0")
            # 构造作业完成消息参数
            operand_finished.send(sender=self, pid=kwargs['id'], ocode='rtc', field_values=self.request.POST)
            return redirect(reverse('index'))
        else:
            attribute_form0 = A6220_ModelForm(instance=A6220.objects.get(pid=kwargs['id']), prefix="attribute_form0")
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
    success_url = 'forms/'
    template_name = 'A6299_create.html'
    form_class = A6203_ModelForm # the first form ModelForm class
    model = A6203
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A6299_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")

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
            base_form = A6203_ModelForm(prefix="base_form")

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



class A6299_UpdateView(UpdateView):
    success_url = 'forms/'
    template_name = 'A6299_update.html'
    form_class = A6203_ModelForm # the first form ModelForm class
    model = A6203

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    # # 构造作业开始消息参数
    # operand_started.send(sender=self, operation_proc=operation_proc, ocode='rtr', operator=self.request.user)

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(A6299_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
        customer = operation_proc.customer
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
            # 构造作业完成消息参数
            operand_finished.send(sender=self, pid=kwargs['id'], ocode='rtc', field_values=self.request.POST)
            return redirect(reverse('index'))
        else:
            attribute_form0 = A6203_ModelForm(instance=A6203.objects.get(pid=kwargs['id']), prefix="attribute_form0")
            attribute_form1 = A6210_ModelForm(instance=A6210.objects.get(pid=kwargs['id']), prefix="attribute_form1")
            attribute_form2 = A6207_ModelForm(instance=A6207.objects.get(pid=kwargs['id']), prefix="attribute_form2")
            attribute_form3 = A6209_ModelForm(instance=A6209.objects.get(pid=kwargs['id']), prefix="attribute_form3")
            attribute_form4 = A6205_ModelForm(instance=A6205.objects.get(pid=kwargs['id']), prefix="attribute_form4")
            attribute_form5 = A6204_ModelForm(instance=A6204.objects.get(pid=kwargs['id']), prefix="attribute_form5")
            attribute_form6 = A6206_ModelForm(instance=A6206.objects.get(pid=kwargs['id']), prefix="attribute_form6")
            attribute_form7 = A6208_ModelForm(instance=A6208.objects.get(pid=kwargs['id']), prefix="attribute_form7")
            attribute_form8 = A6213_ModelForm(instance=A6213.objects.get(pid=kwargs['id']), prefix="attribute_form8")
            attribute_form9 = A6215_ModelForm(instance=A6215.objects.get(pid=kwargs['id']), prefix="attribute_form9")
            attribute_form10 = A6214_ModelForm(instance=A6214.objects.get(pid=kwargs['id']), prefix="attribute_form10")
            attribute_form11 = A6212_ModelForm(instance=A6212.objects.get(pid=kwargs['id']), prefix="attribute_form11")
            attribute_form12 = A6216_ModelForm(instance=A6216.objects.get(pid=kwargs['id']), prefix="attribute_form12")
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
    success_url = 'forms/'
    template_name = 'A3502_create.html'
    form_class = A3502_ModelForm # the first form ModelForm class
    model = A3502
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A3502_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")

            attribute_form0 = A3502_ModelForm(self.request.POST, prefix="attribute_form0")
        else:
            base_form = A6203_ModelForm(prefix="base_form")

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



class A3502_UpdateView(UpdateView):
    success_url = 'forms/'
    template_name = 'A3502_update.html'
    form_class = A3502_ModelForm # the first form ModelForm class
    model = A3502

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    # # 构造作业开始消息参数
    # operand_started.send(sender=self, operation_proc=operation_proc, ocode='rtr', operator=self.request.user)

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(A3502_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(Operation_proc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            attribute_form0 = A3502_ModelForm(self.request.POST, prefix="attribute_form0")
            # 构造作业完成消息参数
            operand_finished.send(sender=self, pid=kwargs['id'], ocode='rtc', field_values=self.request.POST)
            return redirect(reverse('index'))
        else:
            attribute_form0 = A3502_ModelForm(instance=A3502.objects.get(pid=kwargs['id']), prefix="attribute_form0")
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
