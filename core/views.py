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
    context ['user'] = request.user.username

    # 获取当前用户所属的所有作业进程
    customer = Customer.objects.get(user=request.user)
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