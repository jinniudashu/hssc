from django.shortcuts import render, redirect

def index(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/clinic/')
        else:
            return redirect('/core/index_customer/')
    else:
        return redirect('/accounts/login/')



# 接入微信公众平台服务器配置验证
from django.http.response import HttpResponse
import hashlib
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def check_signature(request):
    if request.method == 'GET':
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echostr = request.GET.get('echostr')
        token = 'hssc'

        hashlist = [token, timestamp, nonce]
        hashlist.sort()
        print('[token, timestamp, nonce]', hashlist)
        hashstr = ''.join([s for s in hashlist]).encode('utf-8')  #这里必须增加encode('utf-8'),否则会报错
        print('hashstr befor sha1', hashstr)
        hashstr = hashlib.sha1(hashstr).hexdigest()
        print('hashstr sha1', hashstr)
        if hashstr == signature:
            print('返回echostr')
            return HttpResponse(echostr)  #必须返回echostr
        else:
            print('error!!!')
            return HttpResponse('error')  #可根据实际需要返回
    else:
        return HttpResponse('chenggong')  #可根据实际需要返回


def create_menu(request):
    from hssc.settings import env
    from wechatpy import WeChatClient
    client = WeChatClient(env('WECHAT_APP_ID'), env('WECHAT_APP_SECRET'))
    client.menu.create({
        "button": [
            {
                "name": "我的服务", 
                "sub_button": [
                    {
                        "type": "view", 
                        "name": "预约服务", 
                        "url": "https://jinshuju.net/f/E92p3G"
                    }
                ]
            },
            {
                "name": "个人中心", 
                "sub_button": [
                    {
                        "type": "view", 
                        "name": "基本信息", 
                        "url": "https://jinshuju.net/f/mXA5h0"
                    },
                    {
                        "type": "view", 
                        "name": "已安排服务", 
                        "url": "https://jinshuju.net/f/z5TFlG"
                    },
                    {
                        "type": "view", 
                        "name": "投诉建议", 
                        "url": "https://jinshuju.net/f/fiCaRb"
                    },
                ]
            },
        ]
    })
    return HttpResponse('ok')
