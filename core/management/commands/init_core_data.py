from django.core.management import BaseCommand
from django.apps import apps
import json
import os

from django.conf import settings
from core.models import *
from icpc.models import Icpc
# from service.models import Yao_pin_ji_ben_xin_xi_biao

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
            ServicePackage,
            Service,
            BuessinessFormsSetting,
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


        # 读取测试数据文件
        with open(settings.PROJECT_TEST_DATA, encoding="utf8") as f:
            test_data = json.loads(f.read())

        # 导入测试用户数据
        User.objects.all().exclude(username='admin').delete()
        for user_data in test_data['user']:
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

        # 导入工作小组测试数据
        Workgroup.objects.all().delete()
        for workgroup_data in test_data['workgroup']:
            # 通过姓名字符串匹配，获取组长实例
            leader_name = workgroup_data['leader']
            leader_instance = Staff.objects.get(customer__name=leader_name)

            # 创建新的工作小组并设置组长
            new_workgroup = Workgroup.objects.create(leader=leader_instance)

            # 通过姓名字符串匹配，获取组员实例并添加到工作小组中
            for member_name in workgroup_data['members']:
                member_instance = Staff.objects.get(customer__name=member_name)
                new_workgroup.members.add(member_instance)

            # 保存工作小组实例
            new_workgroup.save()        

        print('导入工作小组测试数据完成！')
        

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


        # 生成数据备份命令脚本, 备份三类models数据：
        # 1. 系统组和用户: auth.User, auth.Group
        # 2. app core中的运行时model:
        # Backup_core_models = [
        #     Customer,
        #     ContractServiceProc,
        #     OperationProc,
        #     StaffTodo,
        #     Institution,
        #     Staff,
        #     Workgroup,
        #     VirtualStaff,
        #     CustomerServiceLog,
        #     RecommendedService,
        #     Message,
        #     Medicine,
        #     ChengBaoRenYuanQingDan,
        # ]
        # 3. app service中的所有model

        # Django的管理脚本路径
        manage_py_path = "python manage.py"

        # 需要备份的模型
        backup_models = [
            "auth.User", "auth.Group",  # 系统用户和组
            "core.Customer",
            "core.ContractServiceProc",
            "core.OperationProc",
            "core.StaffTodo",
            "core.Institution",
            "core.Staff",
            "core.Workgroup",
            "core.VirtualStaff",
            "core.CustomerServiceLog",
            "core.RecommendedService",
            "core.Message",
            "core.Medicine",
            "core.ChengBaoRenYuanQingDan",  # core app的模型
        ]

        # 获取service app中的所有模型
        service_app_config = apps.get_app_config('service')
        for model in service_app_config.get_models():
            backup_models.append(f"service.{model._meta.object_name}")

        # 生成命令
        backup_command = f"{manage_py_path} dumpdata {' '.join(backup_models)} --output=./backup/backup.json"

        # 保存到文件
        with open("backup.py", "w", encoding='utf-8') as file:
            file.write(f"import os\nos.system('{backup_command}')\n\n# 恢复数据命令：\n# python manage.py loaddata ./backup/backup.json")
