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
            else:
                self.write_file(f'.\\forms\\{key}.py', value)
                print(key)

    def write_file(self, file_name, content):
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)


# forms.Kong_fu_xue_tang_jian_cha.numberfield_kong_fu_xue_tang_down_limit: (fields.E130) DecimalFields must define a 'decimal_places' attribute.
# forms.Kong_fu_xue_tang_jian_cha.numberfield_kong_fu_xue_tang_down_limit: (fields.E132) DecimalFields must define a 'max_digits' attribute.
# forms.Kong_fu_xue_tang_jian_cha.numberfield_kong_fu_xue_tang_standard_value: (fields.E130) DecimalFields must define a 'decimal_places' attribute.
# forms.Kong_fu_xue_tang_jian_cha.numberfield_kong_fu_xue_tang_standard_value: (fields.E132) DecimalFields must define a 'max_digits' attribute.
# forms.Kong_fu_xue_tang_jian_cha.numberfield_kong_fu_xue_tang_up_limit: (fields.E130) DecimalFields must define a 'decimal_places' attribute.
# forms.Kong_fu_xue_tang_jian_cha.numberfield_kong_fu_xue_tang_up_limit: (fields.E132) DecimalFields must define a 'max_digits' attribute.
# forms.Tang_hua_xue_hong_dan_bai_jian_cha_biao.numberfield_tang_hua_xue_hong_dan_bai_down_limit: (fields.E130) DecimalFields must define a 'decimal_places' attribute.
# forms.Tang_hua_xue_hong_dan_bai_jian_cha_biao.numberfield_tang_hua_xue_hong_dan_bai_down_limit: (fields.E132) DecimalFields must define a 'max_digits' attribute.
# forms.Tang_hua_xue_hong_dan_bai_jian_cha_biao.numberfield_tang_hua_xue_hong_dan_bai_standard_value: (fields.E130) DecimalFields must define a 'decimal_places' attribute.
# forms.Tang_hua_xue_hong_dan_bai_jian_cha_biao.numberfield_tang_hua_xue_hong_dan_bai_standard_value: (fields.E132) DecimalFields must define a 'max_digits' attribute.
# forms.Tang_hua_xue_hong_dan_bai_jian_cha_biao.numberfield_tang_hua_xue_hong_dan_bai_up_limit: (fields.E130) DecimalFields must define a 'decimal_places' attribute.
# forms.Tang_hua_xue_hong_dan_bai_jian_cha_biao.numberfield_tang_hua_xue_hong_dan_bai_up_limit: (fields.E132) DecimalFields must define a 'max_digits' attribute.