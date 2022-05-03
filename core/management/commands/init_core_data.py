from django.core.management import BaseCommand
from django.contrib.auth.models import User
import json

from core.models import *
from icpc.models import Icpc

test_user_data = {
    'user': [
        {
            'username': '林管家',
            'password': 'info1234',
            'email': 'test@test.com',
            'is_superuser': False,
            'is_staff': True,
            'first_name': '管家',
            'last_name': '林',
            'role': ['健康管理师', '医生助理'],
        },
        {
            'username': '黄医生',
            'password': 'info1234',
            'email': 'test@test.com',
            'is_superuser': False,
            'is_staff': True,
            'first_name': '医生',
            'last_name': '黄',
            'role': ['健康管理师', '医生', '医生助理'],
        },
        {
            'username': '陈医生',
            'password': 'info1234',
            'email': 'test@test.com',
            'is_superuser': False,
            'is_staff': True,
            'first_name': '医生',
            'last_name': '陈',
            'role': ['健康管理师', '医生', '医生助理'],
        },
        {
            'username': '杨医生',
            'password': 'info1234',
            'email': 'test@test.com',
            'is_superuser': False,
            'is_staff': True,
            'first_name': '医生',
            'last_name': '杨',
            'role': ['健康管理师', '医生', '医生助理', '公卫'],
        },
        {
            'username': '孙护士',
            'password': 'info1234',
            'email': 'test@test.com',
            'is_superuser': False,
            'is_staff': True,
            'first_name': '护士',
            'last_name': '孙',
            'role': ['护士', '医生助理'],
        },
        {
            'username': '周药师',
            'password': 'info1234',
            'email': 'test@test.com',
            'is_superuser': False,
            'is_staff': True,
            'first_name': '药师',
            'last_name': '周',
            'role': ['药士', '药剂师'],
        },
    ],
}

class Command(BaseCommand):
    help = 'Restore design data from backuped json file'

    def handle(self, *args, **options):
        # 读取初始业务定义数据文件
        with open('core/initial_data.json', encoding="utf8") as f:
            initial_data = json.loads(f.read())

        initial_models=[
            Role,
            BuessinessForm,
            ManagedEntity,
            Service,
            BuessinessFormsSetting,
            ServicePackage,
            ServicePackageDetail,
            SystemOperand,
            EventRule,
            ServiceSpec,
            ServiceRule,
        ]
        for model in initial_models:
            print(model._meta.model_name)
            result = model.objects.restore_data(initial_data[model._meta.model_name])
            print(result)
            
        print('恢复设计数据完成！')


        # 导入测试用户数据
        User.objects.all().exclude(username='admin').delete()
        for user_data in test_user_data['user']:
            user = User.objects.create_user(
                username=user_data['username'],
                password=user_data['password'],
                email=user_data['email'],
                is_superuser=user_data['is_superuser'],
                is_staff=user_data['is_staff'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
            )
