from django.core.management import BaseCommand
import json

from core.models import *
from icpc.models import Icpc


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
