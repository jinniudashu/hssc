'''
事件发生器
把Django表单Signals转为Icpc编码的业务事件

'''

from django.db.models.signals import post_save, pre_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from registration.signals import user_registered, user_activated, user_approved
from django.dispatch import receiver, Signal

# 导入服务调度器
from core.scheduler import service_scheduler

# 从app forms里获取所有表单model的名字
from django.apps import apps
Forms_models = apps.get_app_config('forms').get_models()
print('当前Forms:')
for Model in Forms_models:
    print(Model.__name__)


# 从表单保存信号生成表单作业业务事件
def form_post_save_handler(sender, **kwargs):
    print("表单保存：form_post_save_handler")
    print(sender)
    print(kwargs)
    print(kwargs['signal'])
    print(kwargs['request'])
    
    # 获得Event编码
    event = 'icpc_code'
    # 把Event编码发给调度器
    service_scheduler(event)

# 把注册信号生成注册事件
def user_registered_handler(sender, **kwargs):
    print("用户注册：user_registered_handler")
    print(sender)
    print(kwargs)
    print(kwargs['signal'])
    print(kwargs['request'])
    print(kwargs['user'])
    print('is_staff:', kwargs['user'].is_staff)
    print('is_superuser:', kwargs['user'].is_superuser)
    
    # 获得Event编码
    event = 'icpc_code'
    # 把Event编码发给调度器
    service_scheduler(event)



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

