from django.core.management import BaseCommand
import requests
import json

class Command(BaseCommand):
    help = '从设计系统导入脚本'

    def handle(self, *args, **kwargs):
        # 表单系统脚本源代码URL
        # 获取脚本源码，创建文件

        # SOURCECODE_URL = 'https://hssc-formdesign.herokuapp.com/define_operand/source_codes_list/'
        SOURCECODE_URL = 'http://127.0.0.1:8000/define_backup/source_codes_list/'
        print('开始导入脚本...')
        res = requests.get(SOURCECODE_URL)
        res_json = res.json()[0]
        code =json.loads(res_json['code'])

        for key, value in code.items():
            if key == 'templates':
                for item in value:
                    (k, v), = item.items()
                    self.write_file(f'./forms/templates/{k}', v)
                    print(k)
            elif key == 'dict_models':
                self.write_file('./dictionaries/models.py', value)
                print(key)
            elif key == 'dict_admin':
                self.write_file('./dictionaries/admin.py', value)
                print(key)
            elif key == 'dict_data':
                self.write_file('./dictionaries/fixtures/initial_data.json', json.dumps(value, ensure_ascii=False, indent=4))
            elif key == 'icpc_models':
                self.write_file('./icpc/models.py', value)
                print(key)
            elif key == 'icpc_admin':
                self.write_file('./icpc/admin.py', value)
                print(key)
            elif key == 'icpc_data':
                self.write_file('./icpc/fixtures/initial_data.json', json.dumps(value, ensure_ascii=False, indent=4))
            elif key == 'core_initial_data':
                self.write_file('./core/initial_data.json', json.dumps(value, ensure_ascii=False, indent=4))
            else:
                self.write_file(f'./forms/{key}.py', value)
                print(key)

    def write_file(self, file_name, content):
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)