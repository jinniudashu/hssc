from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
import datetime

from core.models import Service, Customer, OperationProc
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


def get_services_list(request, **kwargs):
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

    content_type = ContentType.objects.get(app_label='service', model=service.name.lower())

    # 创建新的OperationProc服务作业进程实例
    new_proc=OperationProc.objects.create(
        service=service,  # 服务
        customer=customer,  # 客户
        operator=operator,  # 操作员
        creater=operator,  # 创建者
        state=1,  # 进程状态为创建
        scheduled_time=datetime.datetime.now(),  # 创建时间
        # contract_service_proc=contract_service_proc,  # 所属合约服务进程
        content_type=content_type,  # 内容类型
    )

    # 更新允许作业岗位
    role = service.role.all()
    new_proc.role.set(role)

    # 创建新的model实例
    # form = create_form_instance(new_proc)
    form = eval(service.name.capitalize()).objects.create(
        customer=customer,
        creater=operator,
        operator=operator,
        pid=new_proc,
        cpid=new_proc.contract_service_proc,
    )

    # 添加model的表头信息
    # set_form_header(form)
    form.characterfield_name = new_proc.customer.name
    # form.characterfield_gender = new_proc.customer.a6299_customer.characterfield_gender
    # form.characterfield_age = new_proc.customer.a6299_customer.characterfield_age
    form.characterfield_contact_information = new_proc.customer.phone
    form.characterfield_contact_address = new_proc.customer.address
    form.save()

    # 更新OperationProc服务进程的form实例信息
    new_proc.object_id = form.id
    new_proc.entry = f'/clinic/service/{new_proc.service.name.lower()}/{form.id}/change'
    new_proc.save()

    # 重定向到/clinic/service/model/id/change
    return redirect(new_proc.entry)
