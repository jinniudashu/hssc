from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.apps import apps
from django.views import View
from django.core import serializers

from django_celery_beat.models import PeriodicTask, CrontabSchedule

from core.models import Service, Customer, OperationProc, CustomerServiceLog, Medicine
from core.hsscbase_class import FieldsType
from icpc.models import IcpcBase
from dictionaries.models import *
from service.models import *

class CustomerServiceLogView(View):
    def get(self, request, *args, **kwargs):
        customer = request.GET.get('customer', None)
        period = request.GET.get('period', 'ALL')
        form_class = request.GET.get('form_class', 0)
        if customer is not None:
            logs = CustomerServiceLog.logs.get_customer_service_log(customer, period, int(form_class))
            logs_json = serializers.serialize('json', logs)
            return JsonResponse(logs_json, safe=False)
        else:
            return JsonResponse({"error": "Customer parameter is required"}, status=400)

class MedicineItemView(View):
    def get(self, request, *args, **kwargs):
        itemId = request.GET.get('itemId', None)
        if itemId is not None:
            medicine = Medicine.objects.get(id=itemId)
            medicine_dict = model_to_dict(medicine)
            medicine_verbose_dict = {}
            for field in Medicine._meta.fields:
                if field.verbose_name:
                    medicine_verbose_dict[field.verbose_name] = medicine_dict[field.name]
                else:
                    medicine_verbose_dict[field.name] = medicine_dict[field.name]
            return JsonResponse(medicine_verbose_dict)
        else:
            return JsonResponse({"error": "itemId parameter is required"}, status=400)

class IcpcItemView(View):
    def get(self, request, *args, **kwargs):
        field_name = request.GET.get('fieldName', None)
        item_id = request.GET.get('itemId', None)
        if field_name and item_id is not None:
            try:
                fieldType = FieldsType[field_name].value
                app_name = fieldType.split('.')[0]
                model_name = fieldType.split('.')[1]
                Model = apps.get_model(app_name, model_name)
                try:
                    # Retrieve the item from the model
                    item = Model.objects.get(id=item_id)
                    icpc_dict = model_to_dict(item)
                    icpc_verbose_dict = {}
                    for field in IcpcBase._meta.fields:
                        if field.verbose_name:
                            icpc_verbose_dict[field.verbose_name] = icpc_dict[field.name]
                        else:
                            icpc_verbose_dict[field.name] = icpc_dict[field.name]
                except Model.DoesNotExist:
                    print(f"No {model_name} found with ID={item_id}")
                    return None
            except KeyError:
                print(f"Field {field_name} is not defined in FieldsType Enum.")
            return JsonResponse(icpc_verbose_dict)
        else:
            return JsonResponse({"error": "itemId parameter is required"}, status=400)

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

# 获取员工列表，过滤掉操作员自己，用于排班
def get_employees(request):
    operator = User.objects.get(username=request.user).customer.staff
    shift_employees = []
    for staff in Staff.objects.filter(role__isnull=False).distinct().exclude(id=operator.id):
        allowed_services = [service.id for service in Service.objects.filter(service_type__in=[1,2]) if set(service.role.all()).intersection(set(staff.role.all()))]
        shift_employees.append({'id': staff.customer.id, 'name': staff.name, 'allowed_services': allowed_services})
    return JsonResponse(shift_employees, safe=False)


# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
# def jinshuju_post(request, **kwargs):
#     # 测试接口
#     import json
#     from django.core.exceptions import ObjectDoesNotExist
#     from core.models import ExternalServiceMapping    
#     from core.utils import get_customer_status
#     from core.business_functions import create_service_proc
#     from core.signals import operand_finished
#     from core.hsscbase_class import FieldsType
#     # xmlhttp.setRequestHeader("Content-type","application/json")

#     def _convert_type(_type, _value):
#         # 将字符串转换为对应的类型
#         if _type == 'Datetime':  # 日期时间类型
#             from datetime import datetime
#             # 把_value从字符串转换为datetime类型
#             _value = datetime.strptime(_value, '%Y-%m-%d %H:%M')
#             return _value
#         elif _type == 'Numbers':  # 数字类型
#             return float(_value)
#         elif _type == 'String':  # 字符串类型
#             return _value
#         else:  # 如果字段类型是关联类型，返回对应字典实例对象
#             # 如果是外键关联类型，返回对应的字典实例对象
#             model = eval(_type.split('.')[1]).objects.get(value=_value)
#             # 如果是多对多关联类型，返回对应的字典实例对象列表
#             # model = eval(_type.split('.')[1]).objects.filter(value=_value)
#             return model

#     if(request.method == 'POST'):
#         print("收到POST请求")
#         postBody = request.body
#         json_result = json.loads(postBody)
#         print('Bodys:', json_result)

#         # 接收到外部表单，查找用户服务状态，查找表单，复制表单内容，或创建错误日志
#         external_form_id = json_result.get('form')
#         entry = json_result.get('entry')
#         weixin_openid = entry.get('x_field_weixin_openid')
#         print('微信ID：', weixin_openid)

#         # 1. 用微信OpenID获取用户服务状态
#         customer, customer_service_status = get_customer_status(weixin_openid)

#         # 2. 如果服务状态在服务期，则完成一个服务进程（创建服务进程，填写表单，置服务进程完成）
#         if customer_service_status:
#             # 用外部表单名称在表单映射表中查找内部对应表单，如果查到，则复制表单内容（待补充：如果没查到，则创建新的映射记录，并通知管理员补充映射表）
#             try:
#                 mapping = ExternalServiceMapping.objects.get(external_form_id = external_form_id)
#                 _service = mapping.service
#                 model = eval(_service.name.capitalize())
#                 form = _service.buessiness_forms.first()
#                 print('查到映射记录：', mapping, _service.name, form)

#                 # 提取表单内容
#                 fields_mapping = json.loads(mapping.fields_mapping)
#                 print('fields_mapping:', fields_mapping)
#                 form_data = {}
#                 for field_map in fields_mapping:
#                     (external_field, internal_field), = field_map.items()
#                     # 查找内部表单字段类型，转换外部传入的字段值的格式                    
#                     _type = eval(f'FieldsType.{internal_field}').value
#                     _value = entry.get(external_field)                    
#                     form_data[internal_field] = _convert_type(_type, _value)
#                     print('内部字段：', internal_field, '类型：', _type, '转换后内容：', form_data[internal_field])

#                 print('表单数据：', form_data)

#                 # 新建mapping.service
#                 print('创建service:', _service, _service.name)
#                 # 准备新的服务作业进程参数
#                 content_type = ContentType.objects.get(app_label='service', model=_service.name.lower())
#                 proc_params = {}
#                 proc_params['service'] = _service
#                 proc_params['customer'] = customer
#                 proc_params['creater'] = customer
#                 proc_params['operator'] = customer
#                 proc_params['state'] = 0  # or 0 根据服务作业权限判断
#                 proc_params['scheduled_time'] = timezone.now() # or None 根据服务作业权限判断
#                 proc_params['content_type'] = content_type
#                 proc_params['passing_data'] = 3  # 传递表单数据：(0, '否'), (1, '接收，不可编辑', 复制父进程表单控制信息), (2, '接收，可以编辑', 复制父进程表单控制信息), (3, 复制form_data)
#                 proc_params['form_data'] = form_data

#                 # # 创建新的服务作业进程
#                 # new_proc = create_service_proc(**proc_params)
#                 # print('Debug: jinshuju_post: 创建新的服务作业进程：', new_proc, 'proc_params:', proc_params)

#                 # # 置服务进程完成
#                 # new_proc.update_state('RTC')

#                 # # 发送服务完成信号
#                 # print('发送操作完成信号, 收到金数据表单，form_data:', form_data)
#                 # operand_finished.send(sender=jinshuju_post, pid=new_proc, request=request, form_data=form_data)

#             except ObjectDoesNotExist:
#                 pass

#     response = HttpResponse()
#     response.content = 'Hi, this is Jinshuju Test 127.0.0.1:8000'
#     # response.status_code = 200 # 默认值是200
#     return response


# # 微信消息接口
# from rest_framework.views import APIView
# import redis
# import requests
# import configparser

# r = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)  # 创建redis对象
# config = configparser.ConfigParser()
# config.read('config.ini', encoding="utf-8")
# wx_config = config.items("wechat")
# wx_config = dict(map(lambda x: [x[0], x[1]], wx_config))
# wx_config.update({"token_exp": int(wx_config.get("token_exp"))})


# class AccessToken(APIView):
#     def get(self, request):
#         access_token = r.get("access_token")  # 从redis中获取ACCESS_TOKEN
#         if not access_token:
#             appid = wx_config.get("appid")
#             appsecret = wx_config.get("appsecret")
#             token_api = wx_config.get("token_api")
#             exp = wx_config.get("token_exp")
#             api = token_api.format(appid=appid, secret=appsecret)
#             response = requests.get(api, headers=settings.HEADER).json()
#             access_token = response.get("access_token")
#             r.setex('access_token', exp, access_token)
#         return JsonResponse({"code": 1, "token": access_token})



# from wechatpy.utils import check_signature
# from wechatpy import parse_message, create_reply
# from wechatpy.exceptions import InvalidSignatureException


# class Message(APIView):
#     def get(self, request):
#         signature = request.GET.get('signature', '')
#         timestamp = request.GET.get('timestamp', '')
#         nonce = request.GET.get('nonce', '')
#         echostr = request.GET.get('echostr', '')
#         token = wx_config.get("token")
#         try:
#             check_signature(token, signature, timestamp, nonce)
#         except InvalidSignatureException:
#             echostr = '错误的请求'
#         response = HttpResponse(echostr)
#         return response

#     def post(self, request):
#         msg = parse_message(request.body)
#         wel_msg = "欢迎关注微信公众号：程序员9527"
#         openid = msg.source  # 获取用户openid
#         if msg.type == 'text':
#             reply = create_reply(content, msg)
#         elif msg.type == 'image':
#             reply = create_reply(content, msg)
#         elif msg.type == 'voice':
#             reply = create_reply(content, msg)
#         else:
#             reply = create_reply(content, msg)
#         if hasattr(msg, 'event') and msg.event == "subscribe":
#             print("用户关注", openid)
#         elif hasattr(msg, 'event') and msg.event == 'unsubscribe':
#             print("取消关注", openid)
#         response = HttpResponse(reply.render(), content_type="application/xml")
#         return response