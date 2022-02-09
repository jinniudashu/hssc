from django.core.management import BaseCommand
import requests
from core.models import SOURCECODE_URL

class Command(BaseCommand):
    help = '从设计系统导入脚本'

    def handle(self, *args, **kwargs):
        # 表单系统脚本源代码URL
        # SOURCECODE_URL = 'https://hssc-formdesign.herokuapp.com/define_operand/source_codes_list/'
        SOURCECODE_URL = 'http://127.0.0.1:8000/define_operand/source_codes_list/'

        # 获取脚本源码，创建文件
        print('开始导入脚本...')
        res = requests.get(SOURCECODE_URL)
        res_json = res.json()[0]
        code =eval(res_json['code'])

        for key, value in code.items():
            if key == 'templates':
                for item in value:
                    (k, v), = item.items()
                    self.write_file(f'.\\forms\\templates\\{k}', v)
                    print(k)
            elif key == 'dicts_models':
                self.write_file(f'.\\dictionaries\\models.py', value)
                print(key)
            elif key == 'dicts_admin':
                self.write_file(f'.\\dictionaries\\admin.py', value)
                print(key)
            elif key in ['dicts_data', 'operand_views']:
                print(value)
            else:
                self.write_file(f'.\\forms\\{key}.py', value)
                print(key)

    def write_file(self, file_name, content):
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)