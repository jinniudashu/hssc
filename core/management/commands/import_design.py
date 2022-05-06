from django.core.management import BaseCommand
import requests
import json

class Command(BaseCommand):
    help = '从设计系统导入脚本'
    def handle(self, *args, **kwargs):
        '''
        获取Hssc源码，创建脚本文件
        '''
        print('开始导入脚本...')
        # SOURCECODE_URL = 'https://hssc-formdesign.herokuapp.com/define_backup/source_codes_list/'
        SOURCECODE_URL = 'http://127.0.0.1:8000/define_backup/source_codes_list/'
        res = requests.get(SOURCECODE_URL)
        res_json = res.json()[0]
        source_code =json.loads(res_json['code'])

        # 写入脚本文件
        for app_name, scripts in source_code['script'].items():
            for file_name, script in scripts.items():
                self.write_file(f'./{app_name}/{file_name}.py', script)
                print(f'./{app_name}/{file_name}.py')

        print('写入json数据文件...')
        for app_name, _json_data in source_code['data'].items():
            json_data = json.dumps(_json_data, ensure_ascii=False, indent=4)
            if app_name in ['dictionaries', 'icpc']:
                self.write_file(f'./{app_name}/fixtures/initial_data.json', json_data)
                print(f'./{app_name}/fixtures/initial_data.json')
            elif app_name == 'core':
                self.write_file('./core/initial_data.json', json_data)
                print('./core/initial_data.json')

        print('导入脚本成功！')

    def write_file(self, file_name, content):
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)