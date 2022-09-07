from hssc.settings import env

# 构造公众号模板消息data
def get_wechat_template_message_data(open_id, message, form_data):
    # open_id: oh-n76oPPMqx21HoXNW0T1kEACGQ
    data =  {
        "touser": open_id,
        "template_id": "",
        "url":"",
        "data":{
                "first": {
                    "value": "",
                    "color": "#173177"
                },
                "remark":{
                    "value": "",
                    "color":"#173177"
                }
        }
    }

    data['template_id'] = message.pop('template_id', None)  # 从message中取出模板参数template_id
    data['data']['first']['value'] = message.pop('title', None)  # 从message中取出模板参数title
    data['data']['remark']['value'] = message.pop('remark', None)  # 从message中取出模板参数remark
    print('template_id:', data['template_id'])
    print('title:', data['data']['first']['value'])
    print('remark:', data['data']['remark']['value'])

    # 构造模板参数keyword
    for key in message:
        print(key, form_data[message[key]])
        data['data'][key] = {"value": "", "color":"#173177"}

        # 获取模板参数keyword包含的表单字段的值
        data['data'][key]['value'] = form_data[message[key]]

    return data


# 发送公众号模板消息
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def send_wechat_template_message(data):
    import requests
    import json

    access_token = ''
    # exp_time = 0
    def get_access_token():
        # global exp_time
        APPID = env('WECHAT_APP_ID')
        APPSECRET = env('WECHAT_APP_SECRET')
        # if time.time() > exp_time:
        _url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'
        _r = requests.get(_url)
        _d = json.loads(_r.text)
        print('get access token:', _d)
        access_token = _d['access_token']
            # exp_time = time.time() + _d['expires_in'] - 10  # 减一点防止快到时间的时候已经失效了
        return access_token

    access_token = get_access_token()
    url = f'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}'
    result = requests.post(url, json.dumps(data))
    
    return result


# 发送企业微信消息
def send_wecom_message(uid, message):
    from wechatpy.enterprise import WeChatClient
    from wechatpy.session.redisstorage import RedisStorage
    from redis import Redis

    redis_client = Redis.from_url(env('REDIS_URL'))
    session_interface = RedisStorage(
        redis_client,
        prefix="wechatpy"
    )

    wechat_client = WeChatClient(
        env('CORP_ID'),
        env('SECRET'),
        session=session_interface
    )

    uid = 'XiaoMai'  # 待修改
    result = wechat_client.message.send_text(env('AGENT_ID'), uid, message)
    # user = wechat_client.user.get('user id')
    # menu = wechat_client.menu.get()
    return result


def get_customer_status(open_id):
    """
    查找是否有对应的用户
    如果查到对应用户，返回服务状态
    param open_id
    return: 服务状态 Boolean
    """
    from django.core.exceptions import ObjectDoesNotExist
    from core.models import Customer
    try:
        # open_id: oh-n76oPPMqx21HoXNW0T1kEACGQ
        customer = Customer.objects.get(weixin_openid=open_id)
        return customer, True  # 找到对应用户
    except ObjectDoesNotExist:
        return None, False  # 没有对应用户