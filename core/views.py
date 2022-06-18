from urllib import response
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
import datetime

from requests import Response

from core.models import Service, Customer, OperationProc, RecommendedService
from core.business_functions import create_service_proc, dispatch_operator

def test_celery(request):
    from core.tasks import test_task
    test_task.delay()
    return HttpResponse('ok')


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

def search_services(request, **kwargs):
    from django.db.models import Q
    # 从request.POST获取search
    print('request.POST:', request.POST)
    search_text = request.POST.get('search')
    context = {}
    if search_text is None or search_text == '':
        context['services'] = None
    else:
        context['services'] = [
            {
                'id': service.id, 
                'label': service.label,
                'enable_queue_counter': service.enable_queue_counter,
                'queue_count': OperationProc.objects.get_service_queue_count(service)
            } for service in Service.objects.filter(Q(is_system_service=False) & (Q(label__icontains=search_text) | Q(pym__icontains=search_text)))
        ]

    context['customer_id'] = kwargs['customer_id']

    return render(request, 'services_list.html', context)


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
    proc_params['form_data'] = None
    

    # 如果是推荐服务，解析parent_proc和passing_data
    if kwargs['recommended_service_id']:
        recommended_service = RecommendedService.objects.get(id=kwargs['recommended_service_id'])
        proc_params['parent_proc'] = recommended_service.pid
        proc_params['passing_data'] = recommended_service.passing_data
    else:
        # 人工创建服务，没有父进程
        proc_params['parent_proc'] = None
        # 人工创建服务，没有传递数据
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


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def jinshuju_test(request, **kwargs):
    # 测试接口
    import json
    from django.core.exceptions import ObjectDoesNotExist
    from core.models import ExternalServiceMapping    
    # xmlhttp.setRequestHeader("Content-type","application/json")
    print("收到请求")

    if(request.method == 'POST'):
            print("收到POST请求")
            print('Headers:', request.headers)
            postBody = request.body
            json_result = json.loads(postBody)

            # 接收到外部表单处理步骤：查找用户，判断服务状态，查找表单，复制表单内容，或创建错误日志
            external_form_id = json_result.get('form')
            external_form_name = json_result.get('form_name')
            entry = json_result.get('entry')
            # 1. 用微信OpenID查找是否有对应的用户：open_id = json_result.get('x_field_weixin_openid')
            weixin_openid = entry.get('x_field_weixin_openid')
            print('收到微信OpenID：', weixin_openid)

            # 2. 如果查到对应用户，判断是否在服务期内，如果不在服务期，则不处理，如果在服务期，则开始处理表单
            # 3. 用外部表单名称在表单映射表中查找内部对应表单，如果查到，则复制表单内容，如果没查到，则创建新的映射记录，并通知管理员补充映射表
            try:
                mapping = ExternalServiceMapping.objects.get(external_form_id = external_form_id)
                print('查到映射记录：', mapping)
                fields_mapping = json.loads(mapping.fields_mapping)
                print(fields_mapping)
                for field_map in fields_mapping:
                    (external_field, internal_field), = field_map.items()
                    form_data = {internal_field: entry.get(external_field)}
                    print(form_data)
                
                # 新建mapping.service，传递表单内容form_data

            except ObjectDoesNotExist:
                pass

    response = HttpResponse()
    response.content = 'Hi, this is Jinshuju Test 127.0.0.1:8000'
    # response.status_code = 200 # 默认值是200

    return response
