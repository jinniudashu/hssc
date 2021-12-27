from django.core.management import BaseCommand
import requests
from dictionaries.models import *


class Command(BaseCommand):
    help = '从设计系统导入字典数据'

    def handle(self, *args, **kwargs):

        # 获取脚本源码，创建文件
        print('开始导入字典数据...')
        # url = 'http://127.0.0.1:8000/define/source_codes_list/'
        url = 'https://hssc-formdesign.herokuapp.com/define/source_codes_list/'
        res = requests.get(url)
        res_json = res.json()[0]
        dicts =eval(res_json['code'])['dicts_data']
        for dict in dicts:
            (key, value), = dict.items()
            Dic_model= globals()[key]
            # 先删除原有字典数据
            Dic_model.objects.all().delete()
            # 写入新的字典数据
            for v in value.split('\n'):
                d = Dic_model.objects.create(
                    value = v
                )
                print(key, d, v)

        print('导入字典数据完成')

