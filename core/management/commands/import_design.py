from django.core.management import BaseCommand
import requests
import json

class Command(BaseCommand):
    help = '从设计系统导入脚本'
    def handle(self, *args, **kwargs):
        '''
        获取Hssc源码，创建脚本文件
        '''
        print('开始导入脚本')
        # SOURCECODE_URL = 'https://hssc-formdesign.herokuapp.com/define_backup/source_codes_list/'
        # SOURCECODE_URL = 'https://hssc-dental.herokuapp.com/define_backup/source_codes_list/'
        SOURCECODE_URL = 'http://design.tpahn.com/define_backup/source_codes_list/'
        # SOURCECODE_URL = 'http://127.0.0.1:8000/define_backup/source_codes_list/'
        res = requests.get(SOURCECODE_URL)
        res_json = res.json()[0]
        source_code =json.loads(res_json['code'])

        self._create_code_file(source_code['script'])  # 创建脚本文件
        self._create_data_file(source_code['data'])  # 创建数据文件

        print('导入脚本成功！')

    def _create_code_file(self, code_script):
        print('写入脚本文件...')
        for app_name, scripts in code_script.items():
            for file_name, script in scripts.items():
                self._write_file(f'./{app_name}/{file_name}.py', script)

    def _create_data_file(self, data_script):
        print('写入json数据文件...')
        for app_name, _json_data in data_script.items():
            if app_name in ['dictionaries', 'icpc']:
                _file_name = f'./{app_name}/fixtures/initial_data.json'
            elif app_name == 'core':
                _file_name = './core/initial_data.json'
            json_data = json.dumps(_json_data, ensure_ascii=False, indent=4)
            self._write_file(_file_name, json_data)

    @staticmethod
    def _write_file(file_name, content):
        with open(file_name, 'w', encoding='utf-8') as f:
            _r = f.write(content)
            if _r:
                print(f'{file_name}    ok')
            else:
                print(f'文件{file_name}写入失败！！！')