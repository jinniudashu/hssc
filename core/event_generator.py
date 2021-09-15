'''
1. 把signal转换为预定义的业务事件EVENT

2. 根据业务事件查询指令表，获得指令集

3. 指令集包括以下指令：
    （1）创建人工作业进程，状态：新建
        a. 创建一个作业进程
        b. 获得输入信息
        c. 获得作业员id
        c. 在相应表单Model中创建一条记录
        d. 把update作业入口插入作业员队列

    （2）变更人工作业进程状态：
        新建 --> 就绪
        就绪 --> 执行
        执行 --> 挂起
        挂起 --> 就绪
        执行 --> 完成
    
    （3）路由到下个场景
    （4）执行一个自动化作业

4. 管理员录入服务定义表，系统生成指令表

5. 

'''

from django.db.models.signals import post_save, pre_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from registration.signals import user_registered, user_activated, user_approved
from django.dispatch import receiver, Signal


# 把注册信号生成注册事件
def user_registered_handler(sender, **kwargs):
    print("用户注册：user_registered_handler")
    print(sender)
    print(kwargs)


# 把登录信号生成角色登录事件
def user_logged_in_handler(sender, **kwargs):
    print("用户登入：user_logged_in_handler")
    print(sender)
    print(kwargs)
    print(kwargs['signal'])
    print(kwargs['request'])
    print(kwargs['user'])
    print('is_staff:', kwargs['user'].is_staff)
    print('is_superuser:', kwargs['user'].is_superuser)


# 把退出信号生成角色退出事件
def user_logged_out_handler(sender, **kwargs):
    print("用户退出：user_logged_out_handler")
    print(sender)
    print(kwargs)
    print(kwargs['signal'])
    print(kwargs['request'])
    print(kwargs['user'])


user_registered.connect(user_registered_handler)

user_logged_in.connect(user_logged_in_handler)

user_logged_out.connect(user_logged_out_handler)

