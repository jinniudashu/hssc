from django.core.management import BaseCommand
import json

from core.models import *
from icpc.models import Icpc
# from service.models import Yao_pin_ji_ben_xin_xi_biao

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
        {
            'username': '林丽',
            'password': 'info1234',
            'email': 'test@test.com',
            'is_superuser': False,
            'is_staff': True,
            'first_name': '丽',
            'last_name': '林',
            'role': ['检验师'],
        },
        {
            'username': '化验小李',
            'password': 'info1234',
            'email': 'test@test.com',
            'is_superuser': False,
            'is_staff': True,
            'first_name': '小李',
            'last_name': '化验',
            'role': ['检验师'],
        },
        # {
        #     'username': '金盘口腔诊所',
        #     'password': 'info1234',
        #     'email': 'test@test.com',
        #     'is_superuser': False,
        #     'is_staff': True,
        #     'first_name': '口腔诊所',
        #     'last_name': '金盘',
        #     'role': ['牙科诊所管理员'],
        # },
        # {
        #     'username': '金盘口腔小王',
        #     'password': 'info1234',
        #     'email': 'test@test.com',
        #     'is_superuser': False,
        #     'is_staff': True,
        #     'first_name': '小王',
        #     'last_name': '金盘口腔',
        #     'role': ['牙科诊所管理员'],
        # },
        # {
        #     'username': '金盘口腔小赵',
        #     'password': 'info1234',
        #     'email': 'test@test.com',
        #     'is_superuser': False,
        #     'is_staff': True,
        #     'first_name': '小赵',
        #     'last_name': '金盘口腔',
        #     'role': ['牙科诊所管理员'],
        # },
        # {
        #     'username': '张三',
        #     'password': 'info1234',
        #     'email': 'test@test.com',
        #     'is_superuser': False,
        #     'is_staff': True,
        #     'first_name': '三',
        #     'last_name': '张',
        #     'role': ['保险人员'],
        # },
    ],
}

class Command(BaseCommand):
    help = 'Restore design data from backuped json file'

    def handle(self, *args, **options):
        # 读取初始业务定义数据文件
        with open('core/initial_data.json', encoding="utf8") as f:
            initial_data = json.loads(f.read())

        initial_models=[
            SystemOperand,
            CycleUnit,
            Role,
            BuessinessForm,
            ManagedEntity,
            Service,
            BuessinessFormsSetting,
            ServicePackage,
            ServicePackageDetail,
            EventRule,
            ServiceRule,
            ExternalServiceMapping,
            Medicine,
        ]
        for model in initial_models:
            print(model._meta.model_name)
            result = model.objects.restore_data(initial_data[model._meta.model_name])
            print(result)
            
        print('恢复设计数据完成！')

        from django.contrib.auth.models import User, Group, Permission
        # 创建管理员组, 赋权管理员组所有权限
        admin_group, created = Group.objects.get_or_create(name='admin')
        admin_group.permissions.add(*Permission.objects.all())

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

            # 把测试用户增加到管理员组
            user.groups.add(admin_group)

            # 为测试用户的职员表增加角色
            staff = user.customer.staff
            for role_name in user_data['role']:
                print('role_name:', role_name)
                role = Role.objects.get(label=role_name)
                staff.role.add(role)
            staff.save()

        print('导入测试用户数据完成！')

        # 创建周期任务
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        # 创建检查服务进程等待超时的周期任务
        schedule, create = IntervalSchedule.objects.get_or_create(every=30, period='seconds')
        task, create = PeriodicTask.objects.get_or_create(
            interval=schedule, 
            name='check_proc_awaiting_timeout', 
            task='core.tasks.check_proc_awaiting_timeout'
        )

        print('创建周期任务完成！')

