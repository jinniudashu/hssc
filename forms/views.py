from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.forms import modelformset_factory, inlineformset_factory
import json

from core.models import OperationProc, Staff, Customer
from core.utils import SendSignalsMixin
from forms.utils import *
from forms.models import *
from forms.forms import *


class Index_view(ListView):
    model = OperationProc
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        # 如果用户当前未登录，request.user将被设置为AnonymousUser。用user.is_authenticated()判断用户登录状态：
        operator=User.objects.get(username=self.request.user).customer
        role = operator.staff.role.all()
        # 获取当前用户所属角色的所有作业进程
        procs = OperationProc.objects.exclude(state=4).filter(Q(role__in=role) | Q(operator=operator)).distinct()

        todos = []
        for proc in procs:
            todo = {}
            todo['operation'] = proc.service.label
            todo['url'] = f'{proc.service.name}_update_url'
            todo['proc_id'] = proc.id
            todos.append(todo)
        context = super().get_context_data(**kwargs)
        context['todos'] = todos
        return context


class Men_zhen_chu_fang_biao_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'men_zhen_chu_fang_biao_create.html'
    form_class = A5001_ModelForm  # the first form ModelForm class
    model = A5001
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Men_zhen_chu_fang_biao_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            a5001_form = A5001_ModelForm(self.request.POST, prefix="a5001_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            a5001_form = A5001_ModelForm(prefix="a5001_form")
        # context
        context['base_form'] = base_form
        context['a5001_form'] = a5001_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a5001_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Men_zhen_chu_fang_biao_CreateView, self).form_valid(form)



class Men_zhen_chu_fang_biao_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'men_zhen_chu_fang_biao_update.html'
    form_class = A5001_ModelForm # the first form ModelForm class
    model = A5001

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Men_zhen_chu_fang_biao_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            a5001_form = A5001_ModelForm(self.request.POST, prefix="a5001_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            a5001_form = A5001_ModelForm(instance=A5001.objects.get(pid=kwargs['id']), prefix="a5001_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['a5001_form'] = a5001_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a5001_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Men_zhen_chu_fang_biao_CreateView, self).form_valid(form)

class Z6201_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'Z6201_create.html'
    form_class = Z6201_ModelForm  # the first form ModelForm class
    model = Z6201
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Z6201_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            z6201_form = Z6201_ModelForm(self.request.POST, prefix="z6201_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            z6201_form = Z6201_ModelForm(prefix="z6201_form")
        # context
        context['base_form'] = base_form
        context['z6201_form'] = z6201_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['z6201_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Z6201_CreateView, self).form_valid(form)



class Z6201_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'Z6201_update.html'
    form_class = Z6201_ModelForm # the first form ModelForm class
    model = Z6201

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Z6201_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            z6201_form = Z6201_ModelForm(self.request.POST, prefix="z6201_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            z6201_form = Z6201_ModelForm(instance=Z6201.objects.get(pid=kwargs['id']), prefix="z6201_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['z6201_form'] = z6201_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['z6201_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Z6201_CreateView, self).form_valid(form)

class User_login_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'user_login_create.html'
    form_class = Z6230_ModelForm  # the first form ModelForm class
    model = Z6230
    context = {}

    def get_context_data(self, **kwargs):
        context = super(User_login_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            z6230_form = Z6230_ModelForm(self.request.POST, prefix="z6230_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            z6230_form = Z6230_ModelForm(prefix="z6230_form")
        # context
        context['base_form'] = base_form
        context['z6230_form'] = z6230_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['z6230_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(User_login_CreateView, self).form_valid(form)



class User_login_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'user_login_update.html'
    form_class = Z6230_ModelForm # the first form ModelForm class
    model = Z6230

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(User_login_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            z6230_form = Z6230_ModelForm(self.request.POST, prefix="z6230_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            z6230_form = Z6230_ModelForm(instance=Z6230.objects.get(pid=kwargs['id']), prefix="z6230_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['z6230_form'] = z6230_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['z6230_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(User_login_CreateView, self).form_valid(form)

class Doctor_login_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'doctor_login_create.html'
    form_class = Z6230_ModelForm  # the first form ModelForm class
    model = Z6230
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Doctor_login_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            z6230_form = Z6230_ModelForm(self.request.POST, prefix="z6230_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            z6230_form = Z6230_ModelForm(prefix="z6230_form")
        # context
        context['base_form'] = base_form
        context['z6230_form'] = z6230_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['z6230_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Doctor_login_CreateView, self).form_valid(form)



class Doctor_login_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'doctor_login_update.html'
    form_class = Z6230_ModelForm # the first form ModelForm class
    model = Z6230

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Doctor_login_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            z6230_form = Z6230_ModelForm(self.request.POST, prefix="z6230_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            z6230_form = Z6230_ModelForm(instance=Z6230.objects.get(pid=kwargs['id']), prefix="z6230_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['z6230_form'] = z6230_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['z6230_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Doctor_login_CreateView, self).form_valid(form)

class A6501_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'A6501_create.html'
    form_class = A6501_ModelForm  # the first form ModelForm class
    model = A6501
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A6501_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            a6501_form = A6501_ModelForm(self.request.POST, prefix="a6501_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            a6501_form = A6501_ModelForm(prefix="a6501_form")
        # context
        context['base_form'] = base_form
        context['a6501_form'] = a6501_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a6501_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A6501_CreateView, self).form_valid(form)



class A6501_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'A6501_update.html'
    form_class = A6501_ModelForm # the first form ModelForm class
    model = A6501

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(A6501_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            a6501_form = A6501_ModelForm(self.request.POST, prefix="a6501_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            a6501_form = A6501_ModelForm(instance=A6501.objects.get(pid=kwargs['id']), prefix="a6501_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['a6501_form'] = a6501_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a6501_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A6501_CreateView, self).form_valid(form)

class A6502_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'A6502_create.html'
    form_class = A6502_ModelForm  # the first form ModelForm class
    model = A6502
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A6502_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            a6502_form = A6502_ModelForm(self.request.POST, prefix="a6502_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            a6502_form = A6502_ModelForm(prefix="a6502_form")
        # context
        context['base_form'] = base_form
        context['a6502_form'] = a6502_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a6502_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A6502_CreateView, self).form_valid(form)



class A6502_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'A6502_update.html'
    form_class = A6502_ModelForm # the first form ModelForm class
    model = A6502

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(A6502_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            a6502_form = A6502_ModelForm(self.request.POST, prefix="a6502_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            a6502_form = A6502_ModelForm(instance=A6502.objects.get(pid=kwargs['id']), prefix="a6502_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['a6502_form'] = a6502_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a6502_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A6502_CreateView, self).form_valid(form)

class A3101_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'A3101_create.html'
    form_class = A3001_ModelForm  # the first form ModelForm class
    model = A3001
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A3101_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            a3001_form = A3001_ModelForm(self.request.POST, prefix="a3001_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            a3001_form = A3001_ModelForm(prefix="a3001_form")
        # context
        context['base_form'] = base_form
        context['a3001_form'] = a3001_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a3001_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A3101_CreateView, self).form_valid(form)



class A3101_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'A3101_update.html'
    form_class = A3001_ModelForm # the first form ModelForm class
    model = A3001

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(A3101_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            a3001_form = A3001_ModelForm(self.request.POST, prefix="a3001_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            a3001_form = A3001_ModelForm(instance=A3001.objects.get(pid=kwargs['id']), prefix="a3001_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['a3001_form'] = a3001_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a3001_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A3101_CreateView, self).form_valid(form)

class Tang_niao_bing_zhuan_yong_wen_zhen_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'tang_niao_bing_zhuan_yong_wen_zhen_create.html'
    form_class = A6219_ModelForm  # the first form ModelForm class
    model = A6219
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Tang_niao_bing_zhuan_yong_wen_zhen_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            a6219_form = A6219_ModelForm(self.request.POST, prefix="a6219_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            a6219_form = A6219_ModelForm(prefix="a6219_form")
        # context
        context['base_form'] = base_form
        context['a6219_form'] = a6219_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a6219_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Tang_niao_bing_zhuan_yong_wen_zhen_CreateView, self).form_valid(form)



class Tang_niao_bing_zhuan_yong_wen_zhen_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'tang_niao_bing_zhuan_yong_wen_zhen_update.html'
    form_class = A6219_ModelForm # the first form ModelForm class
    model = A6219

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Tang_niao_bing_zhuan_yong_wen_zhen_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            a6219_form = A6219_ModelForm(self.request.POST, prefix="a6219_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            a6219_form = A6219_ModelForm(instance=A6219.objects.get(pid=kwargs['id']), prefix="a6219_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['a6219_form'] = a6219_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a6219_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Tang_niao_bing_zhuan_yong_wen_zhen_CreateView, self).form_valid(form)

class Yao_shi_fu_wu_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'yao_shi_fu_wu_create.html'
    form_class = A5002_ModelForm  # the first form ModelForm class
    model = A5002
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Yao_shi_fu_wu_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            a5002_form = A5002_ModelForm(self.request.POST, prefix="a5002_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            a5002_form = A5002_ModelForm(prefix="a5002_form")
        # context
        context['base_form'] = base_form
        context['a5002_form'] = a5002_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a5002_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Yao_shi_fu_wu_CreateView, self).form_valid(form)



class Yao_shi_fu_wu_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'yao_shi_fu_wu_update.html'
    form_class = A5002_ModelForm # the first form ModelForm class
    model = A5002

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Yao_shi_fu_wu_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            a5002_form = A5002_ModelForm(self.request.POST, prefix="a5002_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            a5002_form = A5002_ModelForm(instance=A5002.objects.get(pid=kwargs['id']), prefix="a5002_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['a5002_form'] = a5002_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a5002_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Yao_shi_fu_wu_CreateView, self).form_valid(form)

class Tang_niao_bing_zi_wo_jian_ce_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'tang_niao_bing_zi_wo_jian_ce_create.html'
    form_class = T4505_ModelForm  # the first form ModelForm class
    model = T4505
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Tang_niao_bing_zi_wo_jian_ce_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            t4505_form = T4505_ModelForm(self.request.POST, prefix="t4505_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            t4505_form = T4505_ModelForm(prefix="t4505_form")
        # context
        context['base_form'] = base_form
        context['t4505_form'] = t4505_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['t4505_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Tang_niao_bing_zi_wo_jian_ce_CreateView, self).form_valid(form)



class Tang_niao_bing_zi_wo_jian_ce_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'tang_niao_bing_zi_wo_jian_ce_update.html'
    form_class = T4505_ModelForm # the first form ModelForm class
    model = T4505

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Tang_niao_bing_zi_wo_jian_ce_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            t4505_form = T4505_ModelForm(self.request.POST, prefix="t4505_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            t4505_form = T4505_ModelForm(instance=T4505.objects.get(pid=kwargs['id']), prefix="t4505_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['t4505_form'] = t4505_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['t4505_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Tang_niao_bing_zi_wo_jian_ce_CreateView, self).form_valid(form)

class A6217_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'A6217_create.html'
    form_class = A6217_ModelForm  # the first form ModelForm class
    model = A6217
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A6217_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            a6217_form = A6217_ModelForm(self.request.POST, prefix="a6217_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            a6217_form = A6217_ModelForm(prefix="a6217_form")
        # context
        context['base_form'] = base_form
        context['a6217_form'] = a6217_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a6217_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A6217_CreateView, self).form_valid(form)



class A6217_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'A6217_update.html'
    form_class = A6217_ModelForm # the first form ModelForm class
    model = A6217

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(A6217_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            a6217_form = A6217_ModelForm(self.request.POST, prefix="a6217_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            a6217_form = A6217_ModelForm(instance=A6217.objects.get(pid=kwargs['id']), prefix="a6217_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['a6217_form'] = a6217_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a6217_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A6217_CreateView, self).form_valid(form)

class A6201_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'A6201_create.html'
    form_class = A6201_ModelForm  # the first form ModelForm class
    model = A6201
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A6201_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            a6201_form = A6201_ModelForm(self.request.POST, prefix="a6201_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            a6201_form = A6201_ModelForm(prefix="a6201_form")
        # context
        context['base_form'] = base_form
        context['a6201_form'] = a6201_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a6201_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A6201_CreateView, self).form_valid(form)



class A6201_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'A6201_update.html'
    form_class = A6201_ModelForm # the first form ModelForm class
    model = A6201

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(A6201_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            a6201_form = A6201_ModelForm(self.request.POST, prefix="a6201_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            a6201_form = A6201_ModelForm(instance=A6201.objects.get(pid=kwargs['id']), prefix="a6201_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['a6201_form'] = a6201_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a6201_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A6201_CreateView, self).form_valid(form)

class A6218_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'A6218_create.html'
    form_class = A6218_ModelForm  # the first form ModelForm class
    model = A6218
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A6218_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            a6218_form = A6218_ModelForm(self.request.POST, prefix="a6218_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            a6218_form = A6218_ModelForm(prefix="a6218_form")
        # context
        context['base_form'] = base_form
        context['a6218_form'] = a6218_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a6218_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A6218_CreateView, self).form_valid(form)



class A6218_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'A6218_update.html'
    form_class = A6218_ModelForm # the first form ModelForm class
    model = A6218

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(A6218_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            a6218_form = A6218_ModelForm(self.request.POST, prefix="a6218_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            a6218_form = A6218_ModelForm(instance=A6218.objects.get(pid=kwargs['id']), prefix="a6218_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['a6218_form'] = a6218_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a6218_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A6218_CreateView, self).form_valid(form)

class T8901_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'T8901_create.html'
    form_class = T9001_ModelForm  # the first form ModelForm class
    model = T9001
    context = {}

    def get_context_data(self, **kwargs):
        context = super(T8901_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            t9001_form = T9001_ModelForm(self.request.POST, prefix="t9001_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            t9001_form = T9001_ModelForm(prefix="t9001_form")
        # context
        context['base_form'] = base_form
        context['t9001_form'] = t9001_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['t9001_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(T8901_CreateView, self).form_valid(form)



class T8901_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'T8901_update.html'
    form_class = T9001_ModelForm # the first form ModelForm class
    model = T9001

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(T8901_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            t9001_form = T9001_ModelForm(self.request.POST, prefix="t9001_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            t9001_form = T9001_ModelForm(instance=T9001.objects.get(pid=kwargs['id']), prefix="t9001_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['t9001_form'] = t9001_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['t9001_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(T8901_CreateView, self).form_valid(form)

class T6301_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'T6301_create.html'
    form_class = T6301_ModelForm  # the first form ModelForm class
    model = T6301
    context = {}

    def get_context_data(self, **kwargs):
        context = super(T6301_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            t6301_form = T6301_ModelForm(self.request.POST, prefix="t6301_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            t6301_form = T6301_ModelForm(prefix="t6301_form")
        # context
        context['base_form'] = base_form
        context['t6301_form'] = t6301_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['t6301_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(T6301_CreateView, self).form_valid(form)



class T6301_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'T6301_update.html'
    form_class = T6301_ModelForm # the first form ModelForm class
    model = T6301

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(T6301_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            t6301_form = T6301_ModelForm(self.request.POST, prefix="t6301_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            t6301_form = T6301_ModelForm(instance=T6301.objects.get(pid=kwargs['id']), prefix="t6301_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['t6301_form'] = t6301_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['t6301_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(T6301_CreateView, self).form_valid(form)

class A6202_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'A6202_create.html'
    form_class = A6202_ModelForm  # the first form ModelForm class
    model = A6202
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A6202_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            a6202_form = A6202_ModelForm(self.request.POST, prefix="a6202_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            a6202_form = A6202_ModelForm(prefix="a6202_form")
        # context
        context['base_form'] = base_form
        context['a6202_form'] = a6202_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a6202_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A6202_CreateView, self).form_valid(form)



class A6202_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'A6202_update.html'
    form_class = A6202_ModelForm # the first form ModelForm class
    model = A6202

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(A6202_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            a6202_form = A6202_ModelForm(self.request.POST, prefix="a6202_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            a6202_form = A6202_ModelForm(instance=A6202.objects.get(pid=kwargs['id']), prefix="a6202_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['a6202_form'] = a6202_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a6202_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A6202_CreateView, self).form_valid(form)

class A6220_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'A6220_create.html'
    form_class = A6220_ModelForm  # the first form ModelForm class
    model = A6220
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A6220_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            a6220_form = A6220_ModelForm(self.request.POST, prefix="a6220_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            a6220_form = A6220_ModelForm(prefix="a6220_form")
        # context
        context['base_form'] = base_form
        context['a6220_form'] = a6220_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a6220_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A6220_CreateView, self).form_valid(form)



class A6220_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'A6220_update.html'
    form_class = A6220_ModelForm # the first form ModelForm class
    model = A6220

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(A6220_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            a6220_form = A6220_ModelForm(self.request.POST, prefix="a6220_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            a6220_form = A6220_ModelForm(instance=A6220.objects.get(pid=kwargs['id']), prefix="a6220_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['a6220_form'] = a6220_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a6220_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A6220_CreateView, self).form_valid(form)

class A6299_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'A6299_create.html'
    form_class = A6209_ModelForm  # the first form ModelForm class
    model = A6209
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A6299_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            a6209_form = A6209_ModelForm(self.request.POST, prefix="a6209_form")
            a6204_form = A6204_ModelForm(self.request.POST, prefix="a6204_form")
            a6216_form = A6216_ModelForm(self.request.POST, prefix="a6216_form")
            a6206_form = A6206_ModelForm(self.request.POST, prefix="a6206_form")
            a6205_form = A6205_ModelForm(self.request.POST, prefix="a6205_form")
            a6208_form = A6208_ModelForm(self.request.POST, prefix="a6208_form")
            a6214_form = A6214_ModelForm(self.request.POST, prefix="a6214_form")
            a6210_form = A6210_ModelForm(self.request.POST, prefix="a6210_form")
            a6212_form = A6212_ModelForm(self.request.POST, prefix="a6212_form")
            a6203_form = A6203_ModelForm(self.request.POST, prefix="a6203_form")
            a6213_form = A6213_ModelForm(self.request.POST, prefix="a6213_form")
            a6207_form = A6207_ModelForm(self.request.POST, prefix="a6207_form")
            a6215_form = A6215_ModelForm(self.request.POST, prefix="a6215_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            a6209_form = A6209_ModelForm(prefix="a6209_form")
            a6204_form = A6204_ModelForm(prefix="a6204_form")
            a6216_form = A6216_ModelForm(prefix="a6216_form")
            a6206_form = A6206_ModelForm(prefix="a6206_form")
            a6205_form = A6205_ModelForm(prefix="a6205_form")
            a6208_form = A6208_ModelForm(prefix="a6208_form")
            a6214_form = A6214_ModelForm(prefix="a6214_form")
            a6210_form = A6210_ModelForm(prefix="a6210_form")
            a6212_form = A6212_ModelForm(prefix="a6212_form")
            a6203_form = A6203_ModelForm(prefix="a6203_form")
            a6213_form = A6213_ModelForm(prefix="a6213_form")
            a6207_form = A6207_ModelForm(prefix="a6207_form")
            a6215_form = A6215_ModelForm(prefix="a6215_form")
        # context
        context['base_form'] = base_form
        context['a6209_form'] = a6209_form
        context['a6204_form'] = a6204_form
        context['a6216_form'] = a6216_form
        context['a6206_form'] = a6206_form
        context['a6205_form'] = a6205_form
        context['a6208_form'] = a6208_form
        context['a6214_form'] = a6214_form
        context['a6210_form'] = a6210_form
        context['a6212_form'] = a6212_form
        context['a6203_form'] = a6203_form
        context['a6213_form'] = a6213_form
        context['a6207_form'] = a6207_form
        context['a6215_form'] = a6215_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a6209_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6204_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6216_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6206_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6205_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6208_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6214_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6210_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6212_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6203_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6213_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6207_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6215_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A6299_CreateView, self).form_valid(form)



class A6299_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'A6299_update.html'
    form_class = A6209_ModelForm # the first form ModelForm class
    model = A6209

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(A6299_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            a6209_form = A6209_ModelForm(self.request.POST, prefix="a6209_form")
            a6204_form = A6204_ModelForm(self.request.POST, prefix="a6204_form")
            a6216_form = A6216_ModelForm(self.request.POST, prefix="a6216_form")
            a6206_form = A6206_ModelForm(self.request.POST, prefix="a6206_form")
            a6205_form = A6205_ModelForm(self.request.POST, prefix="a6205_form")
            a6208_form = A6208_ModelForm(self.request.POST, prefix="a6208_form")
            a6214_form = A6214_ModelForm(self.request.POST, prefix="a6214_form")
            a6210_form = A6210_ModelForm(self.request.POST, prefix="a6210_form")
            a6212_form = A6212_ModelForm(self.request.POST, prefix="a6212_form")
            a6203_form = A6203_ModelForm(self.request.POST, prefix="a6203_form")
            a6213_form = A6213_ModelForm(self.request.POST, prefix="a6213_form")
            a6207_form = A6207_ModelForm(self.request.POST, prefix="a6207_form")
            a6215_form = A6215_ModelForm(self.request.POST, prefix="a6215_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            a6209_form = A6209_ModelForm(instance=A6209.objects.get(pid=kwargs['id']), prefix="a6209_form")
            a6204_form = A6204_ModelForm(instance=A6204.objects.get(pid=kwargs['id']), prefix="a6204_form")
            a6216_form = A6216_ModelForm(instance=A6216.objects.get(pid=kwargs['id']), prefix="a6216_form")
            a6206_form = A6206_ModelForm(instance=A6206.objects.get(pid=kwargs['id']), prefix="a6206_form")
            a6205_form = A6205_ModelForm(instance=A6205.objects.get(pid=kwargs['id']), prefix="a6205_form")
            a6208_form = A6208_ModelForm(instance=A6208.objects.get(pid=kwargs['id']), prefix="a6208_form")
            a6214_form = A6214_ModelForm(instance=A6214.objects.get(pid=kwargs['id']), prefix="a6214_form")
            a6210_form = A6210_ModelForm(instance=A6210.objects.get(pid=kwargs['id']), prefix="a6210_form")
            a6212_form = A6212_ModelForm(instance=A6212.objects.get(pid=kwargs['id']), prefix="a6212_form")
            a6203_form = A6203_ModelForm(instance=A6203.objects.get(pid=kwargs['id']), prefix="a6203_form")
            a6213_form = A6213_ModelForm(instance=A6213.objects.get(pid=kwargs['id']), prefix="a6213_form")
            a6207_form = A6207_ModelForm(instance=A6207.objects.get(pid=kwargs['id']), prefix="a6207_form")
            a6215_form = A6215_ModelForm(instance=A6215.objects.get(pid=kwargs['id']), prefix="a6215_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['a6209_form'] = a6209_form
        context['a6204_form'] = a6204_form
        context['a6216_form'] = a6216_form
        context['a6206_form'] = a6206_form
        context['a6205_form'] = a6205_form
        context['a6208_form'] = a6208_form
        context['a6214_form'] = a6214_form
        context['a6210_form'] = a6210_form
        context['a6212_form'] = a6212_form
        context['a6203_form'] = a6203_form
        context['a6213_form'] = a6213_form
        context['a6207_form'] = a6207_form
        context['a6215_form'] = a6215_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a6209_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6204_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6216_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6206_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6205_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6208_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6214_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6210_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6212_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6203_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6213_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6207_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['a6215_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A6299_CreateView, self).form_valid(form)

class A3502_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'A3502_create.html'
    form_class = A3502_ModelForm  # the first form ModelForm class
    model = A3502
    context = {}

    def get_context_data(self, **kwargs):
        context = super(A3502_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            a3502_form = A3502_ModelForm(self.request.POST, prefix="a3502_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            a3502_form = A3502_ModelForm(prefix="a3502_form")
        # context
        context['base_form'] = base_form
        context['a3502_form'] = a3502_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a3502_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A3502_CreateView, self).form_valid(form)



class A3502_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'A3502_update.html'
    form_class = A3502_ModelForm # the first form ModelForm class
    model = A3502

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(A3502_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            a3502_form = A3502_ModelForm(self.request.POST, prefix="a3502_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            a3502_form = A3502_ModelForm(instance=A3502.objects.get(pid=kwargs['id']), prefix="a3502_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['a3502_form'] = a3502_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a3502_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(A3502_CreateView, self).form_valid(form)

class Tang_niao_bing_cha_ti_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'tang_niao_bing_cha_ti_create.html'
    form_class = T3003_ModelForm  # the first form ModelForm class
    model = T3003
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Tang_niao_bing_cha_ti_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            t3003_form = T3003_ModelForm(self.request.POST, prefix="t3003_form")
            t3002_form = T3002_ModelForm(self.request.POST, prefix="t3002_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            t3003_form = T3003_ModelForm(prefix="t3003_form")
            t3002_form = T3002_ModelForm(prefix="t3002_form")
        # context
        context['base_form'] = base_form
        context['t3003_form'] = t3003_form
        context['t3002_form'] = t3002_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['t3003_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['t3002_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Tang_niao_bing_cha_ti_CreateView, self).form_valid(form)



class Tang_niao_bing_cha_ti_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'tang_niao_bing_cha_ti_update.html'
    form_class = T3003_ModelForm # the first form ModelForm class
    model = T3003

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Tang_niao_bing_cha_ti_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            t3003_form = T3003_ModelForm(self.request.POST, prefix="t3003_form")
            t3002_form = T3002_ModelForm(self.request.POST, prefix="t3002_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            t3003_form = T3003_ModelForm(instance=T3003.objects.get(pid=kwargs['id']), prefix="t3003_form")
            t3002_form = T3002_ModelForm(instance=T3002.objects.get(pid=kwargs['id']), prefix="t3002_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['t3003_form'] = t3003_form
        context['t3002_form'] = t3002_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['t3003_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        f = context['t3002_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Tang_niao_bing_cha_ti_CreateView, self).form_valid(form)

class Xue_ya_jian_ce_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'xue_ya_jian_ce_create.html'
    form_class = A3105_ModelForm  # the first form ModelForm class
    model = A3105
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Xue_ya_jian_ce_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            a3105_form = A3105_ModelForm(self.request.POST, prefix="a3105_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            a3105_form = A3105_ModelForm(prefix="a3105_form")
        # context
        context['base_form'] = base_form
        context['a3105_form'] = a3105_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a3105_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Xue_ya_jian_ce_CreateView, self).form_valid(form)



class Xue_ya_jian_ce_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'xue_ya_jian_ce_update.html'
    form_class = A3105_ModelForm # the first form ModelForm class
    model = A3105

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Xue_ya_jian_ce_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            a3105_form = A3105_ModelForm(self.request.POST, prefix="a3105_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            a3105_form = A3105_ModelForm(instance=A3105.objects.get(pid=kwargs['id']), prefix="a3105_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['a3105_form'] = a3105_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['a3105_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Xue_ya_jian_ce_CreateView, self).form_valid(form)

class Kong_fu_xue_tang_jian_cha_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'kong_fu_xue_tang_jian_cha_create.html'
    form_class = T3404_ModelForm  # the first form ModelForm class
    model = T3404
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Kong_fu_xue_tang_jian_cha_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            t3404_form = T3404_ModelForm(self.request.POST, prefix="t3404_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            t3404_form = T3404_ModelForm(prefix="t3404_form")
        # context
        context['base_form'] = base_form
        context['t3404_form'] = t3404_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['t3404_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Kong_fu_xue_tang_jian_cha_CreateView, self).form_valid(form)



class Kong_fu_xue_tang_jian_cha_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'kong_fu_xue_tang_jian_cha_update.html'
    form_class = T3404_ModelForm # the first form ModelForm class
    model = T3404

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Kong_fu_xue_tang_jian_cha_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            t3404_form = T3404_ModelForm(self.request.POST, prefix="t3404_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            t3404_form = T3404_ModelForm(instance=T3404.objects.get(pid=kwargs['id']), prefix="t3404_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['t3404_form'] = t3404_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['t3404_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Kong_fu_xue_tang_jian_cha_CreateView, self).form_valid(form)

class Tang_hua_xue_hong_dan_bai_jian_cha_biao_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'tang_hua_xue_hong_dan_bai_jian_cha_biao_create.html'
    form_class = T3405_ModelForm  # the first form ModelForm class
    model = T3405
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Tang_hua_xue_hong_dan_bai_jian_cha_biao_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            t3405_form = T3405_ModelForm(self.request.POST, prefix="t3405_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            t3405_form = T3405_ModelForm(prefix="t3405_form")
        # context
        context['base_form'] = base_form
        context['t3405_form'] = t3405_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['t3405_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Tang_hua_xue_hong_dan_bai_jian_cha_biao_CreateView, self).form_valid(form)



class Tang_hua_xue_hong_dan_bai_jian_cha_biao_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'tang_hua_xue_hong_dan_bai_jian_cha_biao_update.html'
    form_class = T3405_ModelForm # the first form ModelForm class
    model = T3405

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Tang_hua_xue_hong_dan_bai_jian_cha_biao_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            t3405_form = T3405_ModelForm(self.request.POST, prefix="t3405_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            t3405_form = T3405_ModelForm(instance=T3405.objects.get(pid=kwargs['id']), prefix="t3405_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['t3405_form'] = t3405_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['t3405_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Tang_hua_xue_hong_dan_bai_jian_cha_biao_CreateView, self).form_valid(form)

class T9001_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'T9001_create.html'
    form_class = T9001_ModelForm  # the first form ModelForm class
    model = T9001
    context = {}

    def get_context_data(self, **kwargs):
        context = super(T9001_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            t9001_form = T9001_ModelForm(self.request.POST, prefix="t9001_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            t9001_form = T9001_ModelForm(prefix="t9001_form")
        # context
        context['base_form'] = base_form
        context['t9001_form'] = t9001_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['t9001_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(T9001_CreateView, self).form_valid(form)



class T9001_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'T9001_update.html'
    form_class = T9001_ModelForm # the first form ModelForm class
    model = T9001

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(T9001_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            t9001_form = T9001_ModelForm(self.request.POST, prefix="t9001_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            t9001_form = T9001_ModelForm(instance=T9001.objects.get(pid=kwargs['id']), prefix="t9001_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['t9001_form'] = t9001_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['t9001_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(T9001_CreateView, self).form_valid(form)

class Qian_yue_fu_wu_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'qian_yue_fu_wu_create.html'
    form_class = Z6261_ModelForm  # the first form ModelForm class
    model = Z6261
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Qian_yue_fu_wu_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            z6261_form = Z6261_ModelForm(self.request.POST, prefix="z6261_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            z6261_form = Z6261_ModelForm(prefix="z6261_form")
        # context
        context['base_form'] = base_form
        context['z6261_form'] = z6261_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['z6261_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Qian_yue_fu_wu_CreateView, self).form_valid(form)



class Qian_yue_fu_wu_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'qian_yue_fu_wu_update.html'
    form_class = Z6261_ModelForm # the first form ModelForm class
    model = Z6261

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Qian_yue_fu_wu_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            z6261_form = Z6261_ModelForm(self.request.POST, prefix="z6261_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            z6261_form = Z6261_ModelForm(instance=Z6261.objects.get(pid=kwargs['id']), prefix="z6261_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['z6261_form'] = z6261_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['z6261_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Qian_yue_fu_wu_CreateView, self).form_valid(form)

class Shu_ye_zhu_she_CreateView(CreateView):
    success_url = 'forms/'
    template_name = 'shu_ye_zhu_she_create.html'
    form_class = Shu_ye_zhu_she_dan_ModelForm  # the first form ModelForm class
    model = Shu_ye_zhu_she_dan
    context = {}

    def get_context_data(self, **kwargs):
        context = super(Shu_ye_zhu_she_CreateView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            base_form = A6203_ModelForm(self.request.POST, prefix="base_form")
            shu_ye_zhu_she_dan_form = Shu_ye_zhu_she_dan_ModelForm(self.request.POST, prefix="shu_ye_zhu_she_dan_form")
        else:
            base_form = A6203_ModelForm(prefix="base_form")
            shu_ye_zhu_she_dan_form = Shu_ye_zhu_she_dan_ModelForm(prefix="shu_ye_zhu_she_dan_form")
        # context
        context['base_form'] = base_form
        context['shu_ye_zhu_she_dan_form'] = shu_ye_zhu_she_dan_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['shu_ye_zhu_she_dan_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Shu_ye_zhu_she_CreateView, self).form_valid(form)



class Shu_ye_zhu_she_UpdateView(SendSignalsMixin, UpdateView):
    success_url = 'forms/'
    template_name = 'shu_ye_zhu_she_update.html'
    form_class = Shu_ye_zhu_she_dan_ModelForm # the first form ModelForm class
    model = Shu_ye_zhu_she_dan

    # if operation_proc.group is None:  # 如果进程角色已经被置为空，说明已有其他人处理，退出本修改作业进程
    #     return redirect(reverse('index'))
    # operation_proc.group.set([])  # 设置作业进程所属角色组为空

    context = {}
        
    def get_context_data(self, **kwargs):
        context = super(Shu_ye_zhu_she_UpdateView, self).get_context_data(**kwargs)
        operation_proc = get_object_or_404(OperationProc, id=kwargs['id'])
        customer = operation_proc.customer
        base_form = A6203_ModelForm(instance=A6203.objects.get(customer=1), prefix="base_form")
        if self.request.method == 'POST':
            shu_ye_zhu_she_dan_form = Shu_ye_zhu_she_dan_ModelForm(self.request.POST, prefix="shu_ye_zhu_she_dan_form")
            # 构造作业完成消息参数
            self.send_operand_finished(kwargs)
            return redirect(reverse('index'))
        else:
            shu_ye_zhu_she_dan_form = Shu_ye_zhu_she_dan_ModelForm(instance=Shu_ye_zhu_she_dan.objects.get(pid=kwargs['id']), prefix="shu_ye_zhu_she_dan_form")
            # 构造作业开始消息参数
            self.send_operand_started(kwargs['id'])
        # context
        context['base_form'] = base_form
        context['shu_ye_zhu_she_dan_form'] = shu_ye_zhu_she_dan_form
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        customer = Customer.objects.get(user=context['user'])
        operator = Staff.objects.get(user=context['user'])
        # form_valid
        f = context['shu_ye_zhu_she_dan_form'].save(commit=False)
        f.customer = customer
        f.operator = operator
        f.save()
        return super(Shu_ye_zhu_she_CreateView, self).form_valid(form)
