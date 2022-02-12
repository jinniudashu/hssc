from django.core.management import BaseCommand
from icpc.models import icpc_list, Icpc1_register_logins, Icpc2_reservation_investigations, Icpc3_symptoms_and_problems, Icpc4_physical_examination_and_tests, Icpc5_evaluation_and_diagnoses, Icpc6_prescribe_medicines, Icpc7_treatments, Icpc8_other_health_interventions, Icpc9_referral_consultations, Icpc10_test_results_and_statistics
import requests
import json

class Command(BaseCommand):
    help = '从设计系统导入ICPC数据'

    def handle(self, *args, **kwargs):
        url = 'https://hssc-formdesign.herokuapp.com/define_icpc/get_icpc_backup/'
        # url = 'http://127.0.0.1:8000/define_icpc/get_icpc_backup/'
        print(f'从{url}导入ICPC数据备份...')
        res = requests.get(url)
        res_json = res.json()[0]
        icpc_data =json.loads(res_json['code'])

        for icpc in icpc_list:
            Icpc_model = eval(icpc['name'])  # 反射出model
            _key = icpc['name'].lower()  # 获取小写键名
            _l = len(icpc_data[_key])  # 当前ICPC数据的长度

            Icpc_model.objects.all().delete()  # 删除ICPC数据
            print(f'正在导入{icpc["name"]}，共{_l}条记录...')
            for item in icpc_data[_key]:  # 导入ICPC数据
                Icpc_model.objects.create(**item)
            print(f'{icpc["name"]} 数据导入成功')

        print('导入ICPC数据完成！')