from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
import datetime

from core.models import Service, Customer, OperationProc
from core.business_functions import create_service_proc


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


def get_services_list(request, **kwargs):
    '''
    从kwargs获取参数：customer_id
    返回context可用服务列表,customer_id
    '''
    context = {}
    context['services'] = [
        {
            'id': service.id, 
            'label': service.label,
            'enable_queue_counter': service.enable_queue_counter,
            'queue_count': OperationProc.objects.get_service_queue_count(service)
        } for service in Service.objects.filter(is_system_service=False)
    ]
    context['customer_id'] = kwargs['customer_id']

    return render(request, 'popup_menu.html', context)


def new_service(request, **kwargs):
    '''
    人工创建新服务：作业进程+表单进程
    从kwargs获取参数：customer_id, service_id
    '''
    # 从request获取参数：customer, service, operator
    customer = Customer.objects.get(id=kwargs['customer_id'])
    operator = User.objects.get(username=request.user).customer
    service = Service.objects.get(id=kwargs['service_id'])
    content_type = ContentType.objects.get(app_label='service', model=service.name.lower())

    # 准备新的服务作业进程参数
    proc_params = {}
    proc_params['service'] = service
    proc_params['customer'] = customer
    proc_params['creater'] = operator  
    proc_params['operator'] = operator  # or None 根据服务作业权限判断
    proc_params['state'] = 1  # or 0 根据服务作业权限判断
    proc_params['scheduled_time'] = datetime.datetime.now() # or None 根据服务作业权限判断
    proc_params['parent_proc'] = None  # or 作业员登录进程
    proc_params['contract_service_proc'] = None
    proc_params['content_type'] = content_type

    # 创建新的OperationProc服务作业进程实例
    new_proc = create_service_proc(**proc_params)

    # 重定向到/clinic/service/model/id/change
    return redirect(new_proc.entry)
