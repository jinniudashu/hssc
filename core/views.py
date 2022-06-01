from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
import datetime

from core.models import Service, Customer, OperationProc, RecommendedService
from core.business_functions import create_service_proc, dispatch_operator


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
    current_operator = User.objects.get(username=request.user).customer
    service = Service.objects.get(id=kwargs['service_id'])
    service_operator = dispatch_operator(customer, service, current_operator)
    content_type = ContentType.objects.get(app_label='service', model=service.name.lower())

    # 准备新的服务作业进程参数
    proc_params = {}
    proc_params['service'] = service
    proc_params['customer'] = customer
    proc_params['creater'] = current_operator
    proc_params['operator'] = service_operator
    proc_params['state'] = 0  # or 0 根据服务作业权限判断
    proc_params['scheduled_time'] = datetime.datetime.now() # or None 根据服务作业权限判断
    proc_params['contract_service_proc'] = None
    proc_params['content_type'] = content_type
    

    # 如果是推荐服务，处理passing_data
    if service.is_recommended_service:
        proc_params['parent_proc'] = None  # or 作业员登录进程
        proc_params['passing_data'] = 0
    else:
        proc_params['parent_proc'] = None
        proc_params['passing_data'] = 0


    # 创建新的OperationProc服务作业进程实例
    new_proc = create_service_proc(**proc_params)

    # 如果请求来自可选服务，从可选服务队列中删除服务
    if kwargs['recommended_service_id']:
        RecommendedService.objects.get(id=kwargs['recommended_service_id']).delete()

    # 如果开单给作业员本人，进入修改界面
    if service_operator == current_operator:
        # 重定向到/clinic/service/model/id/change
        return redirect(new_proc.entry)
    else:  # 否则显示提示消息：开单成功
        from django.contrib import messages
        messages.add_message(request, messages.INFO, f'{service.label}已开单')
        return redirect(customer)
