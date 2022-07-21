def send_wechat_message(uid, message):
    """
    发送微信消息
    :param message:
    :return:
    """
    from wechatpy.enterprise import WeChatClient
    from wechatpy.session.redisstorage import RedisStorage
    from redis import Redis

    from hssc.settings import env

    redis_client = Redis.from_url('redis://default:redispw@localhost:49153/15')
    session_interface = RedisStorage(
        redis_client,
        prefix="wechatpy"
    )

    wechat_client = WeChatClient(
        # CORP_ID,
        env('CORP_ID'),
        # SECRET,
        env('SECRET'),
        session=session_interface
    )

    # wechat_client = WeChatClient(CORP_ID, SECRET)
    wechat_client.message.send_text(env('AGENT_ID'), uid, message)
    # user = wechat_client.user.get('user id')
    # menu = wechat_client.menu.get()