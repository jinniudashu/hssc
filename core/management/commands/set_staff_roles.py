from django.core.management import BaseCommand
from django.contrib.auth.models import User, Group
import json

from core.models import *
from icpc.models import Icpc

from .init_core_data import test_user_data

class Command(BaseCommand):
    help = 'Restore design data from backuped json file'

    def handle(self, *args, **options):
        # 如果不存在管理员组，则创建admin Group，赋予所有权限
        admin_group = Group.objects.get(name='admin')  # 获取管理员组

        for user_data in test_user_data['user']:
            user = User.objects.get(username=user_data['username'])
            # 把测试用户增加到管理员组
            user.groups.add(admin_group)

            # 为测试用户的职员表增加角色
            staff = user.customer.staff
            for role_name in user_data['role']:
                role = Role.objects.get(label=role_name)
                staff.role.add(role)
            staff.save()
            print('测试用户职员表增加角色成功')

            