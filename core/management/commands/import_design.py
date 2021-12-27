from django.core.management import BaseCommand
import requests


class Command(BaseCommand):
    help = '从设计系统导入forms脚本'

    def handle(self, *args, **kwargs):

        # 获取脚本源码，创建文件
        print('开始导入forms脚本...')
        # url = 'http://127.0.0.1:8000/define/source_codes_list/'
        url = 'https://hssc-formdesign.herokuapp.com/define/source_codes_list/'
        res = requests.get(url)
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
            elif key == 'dicts_data':
                print(value)
            else:
                self.write_file(f'.\\forms\\{key}.py', value)
                print(key)

    def write_file(self, file_name, content):
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)