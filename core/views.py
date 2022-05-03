from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
import datetime

from core.models import Customer, OperationProc, Service
from service.models import *

def index_customer(request):
    context = {}
    customer = Customer.objects.get(user=request.user)
    context ['customer'] = customer.name
    # 获取当前用户所属的所有作业进程
    procs = OperationProc.objects.exclude(state=4).filter(customer=customer)
    todos = []
    for proc in procs:
        todo = {}
        todo['service'] = proc.service.label
        todos.append(todo)
    context['todos'] = todos

    return render(request, 'index_customer.html', context)


def get_services(request, **kwargs):
    '''
    从kwargs获取参数：customer_id
    返回context可用服务列表,customer_id
    '''
    context = {}
    # staff_roles = User.objects.get(username=request.user).customer.staff.role.all()
    # context['services'] = Service.objects.filter(role__in=staff_roles)  
    context['services'] = Service.objects.filter(is_system_service=False)
    context['customer_id'] = kwargs['customer_id']
    return render(request, 'popup_menu.html', context)


def new_service(request, **kwargs):
    '''
    人工创建新服务：作业进程+表单进程
    从kwargs获取参数：customer_id, service_id
    '''
    # 从request获取参数：customer, service, operator, creator
    customer = Customer.objects.get(id=kwargs['customer_id'])
    operator = User.objects.get(username=request.user).customer
    service = Service.objects.get(id=kwargs['service_id'])

    # 创建新的OperationProc服务作业进程实例
    new_proc=OperationProc.objects.create(
        service=service,  # 服务
        customer=customer,  # 客户
        operator=operator,  # 操作员
        creater=operator,  # 创建者
        state=1,  # 进程状态为创建
        scheduled_time=datetime.datetime.now(),  # 创建时间
        # contract_service_proc=contract_service_proc,  # 所属合约服务进程
    )

    # 创建新的model实例
    form = eval(service.name.capitalize()).objects.create(
        customer=customer,
        creater=operator,
        operator=operator,
        pid=new_proc,
        cpid=new_proc.contract_service_proc,
    )

    # 添加model的客户基本信息
    form.characterfield_name = new_proc.customer.name
    # form.characterfield_gender = new_proc.customer.a6299_customer.characterfield_gender
    # form.characterfield_age = new_proc.customer.a6299_customer.characterfield_age
    form.characterfield_contact_information = new_proc.customer.phone
    form.characterfield_contact_address = new_proc.customer.address
    form.save()

    # 更新OperationProc服务进程的入口url
    new_proc.entry = f'/clinic/service/{service.name.lower()}/{form.id}/change'
    new_proc.save()


    # 重定向到/clinic/service/model/id/change
    return redirect(new_proc.entry)
