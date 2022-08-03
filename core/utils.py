from hssc.settings import env

def send_wecom_message(uid, message):
    """
    发送企业微信消息
    param uid, message
    return
    """
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

    wechat_client.message.send_text(env('AGENT_ID'), uid, message)

    # user = wechat_client.user.get('user id')
    # menu = wechat_client.menu.get()

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def send_wechat_template_message(open_id, template_id, message):
    import time
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
    data =  {
        "touser": open_id,
        "template_id": template_id,
        "url":"https://9ee9-115-42-122-94.ap.ngrok.io",
        "data":{
                "first": {
                    "value": message,
                    "color": "#173177"
                },
                "keyword1":{
                    "value": 'value1',
                    "color":"#173177"
                },
                "keyword2": {
                    "value": message,
                    "color":"#173177"
                },
                "keyword3": {
                    "value": 'value3',
                    "color":"#173177"
                },
                "remark":{
                    "value": '请准时抵达',
                    "color":"#173177"
                }
        }
    }
    url = f'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}'
    r = requests.post(url, json.dumps(data))
    print('send wechat template message:', r)