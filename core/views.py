from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import Group
from django.db.models import Q

from core.models import Staff, Customer, Operation_proc


def htmx_test(request):
    print('From htmx_test:', request)
    return HttpResponse('From: htmx_test')


def index_staff(request):
    context = {}
    operator=Staff.objects.get(user=request.user)
    group = Group.objects.filter(user=request.user)
    # 获取当前用户所属角色组的所有作业进程
    procs = Operation_proc.objects.exclude(state=4).filter(Q(group__in=group) | Q(operator=operator)).distinct()
    print('procs:', procs)

    todos = []
    for proc in procs:
        todo = {}
        todo['operation'] = proc.operation.label
        todo['url'] = f'{proc.operation.name}_update_url'
        todo['proc_id'] = proc.id
        todos.append(todo)
    context['todos'] = todos
    return render(request, 'index_staff.html', context)


def index_customer(request):
    context = {}
    customer = Customer.objects.get(user=request.user)
    context ['customer'] = customer.name
    print('customer:', customer)
    # 获取当前用户所属的所有作业进程
    procs = Operation_proc.objects.exclude(state=4).filter(customer=customer)
    print('procs:', procs)
    todos = []
    for proc in procs:
        todo = {}
        todo['operation'] = proc.operation.label
        todo['url'] = f'{proc.operation.name}_update_url'
        todo['proc_id'] = proc.id
        todos.append(todo)
    context['todos'] = todos

    return render(request, 'index_customer.html', context)
