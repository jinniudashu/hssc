from urllib import response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Q

from requests import Response

from django_celery_beat.models import PeriodicTask, CrontabSchedule

from core.models import Service, ServicePackage, Customer, OperationProc, RecommendedService


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


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def jinshuju_test(request, **kwargs):
    # 测试接口
    import json
    from django.core.exceptions import ObjectDoesNotExist
    from core.models import ExternalServiceMapping    
    from core.utils import send_wecom_message, send_wechat_template_message
    # xmlhttp.setRequestHeader("Content-type","application/json")
    print("收到请求")

    if(request.method == 'POST'):
        print("收到POST请求")
        print('Headers:', request.headers)
        postBody = request.body
        json_result = json.loads(postBody)
        print('bodys:', json_result)

        # 接收到外部表单处理步骤：查找用户，判断服务状态，查找表单，复制表单内容，或创建错误日志
        external_form_id = json_result.get('form')
        external_form_name = json_result.get('form_name')
        entry = json_result.get('entry')
        # 1. 用微信OpenID查找是否有对应的用户：open_id = json_result.get('x_field_weixin_openid')
        weixin_openid = entry.get('x_field_weixin_openid')
        print('微信ID：', weixin_openid)

        # 2. 如果查到对应用户，判断是否在服务期内，如果不在服务期，则不处理，如果在服务期，则开始处理表单
        
            # 获取用户负责人企业微信账号，用于发送通知消息

        # 3. 用外部表单名称在表单映射表中查找内部对应表单，如果查到，则复制表单内容，如果没查到，则创建新的映射记录，并通知管理员补充映射表
        try:
            mapping = ExternalServiceMapping.objects.get(external_form_id = external_form_id)
            print('查到映射记录：', mapping)
            fields_mapping = json.loads(mapping.fields_mapping)
            print(fields_mapping)
            form_data = []
            for field_map in fields_mapping:
                (external_field, internal_field), = field_map.items()
                form_data.append({internal_field: entry.get(external_field)})
            print(form_data)
            
            # 新建mapping.service，传递表单内容form_data
            service = mapping.service

        except ObjectDoesNotExist:
            pass

        # 回复企业微信消息
        # send_wechat_message(weixin_openid, '收到一个新的表单，请及时处理！')
        # send_wecom_message('XiaoMai', '收到一个新的表单，请及时处理！')

        # 回复公众号模板消息
        from hssc.settings import env
        template_id = env('WECHAT_TEMPLATE_ENROLL_SUCCESS')
        # openid: oh-n76oPPMqx21HoXNW0T1kEACGQ
        send_wechat_template_message(weixin_openid, template_id, '预约成功，请准时到达！')

    response = HttpResponse()
    response.content = 'Hi, this is Jinshuju Test 127.0.0.1:8000'
    # response.status_code = 200 # 默认值是200

    return response


def test_celery(request):
    from core.tasks import test_task
    test_task.delay()
    return HttpResponse('ok')


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