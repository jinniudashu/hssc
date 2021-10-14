from django.core.management import BaseCommand
import requests
import math

from icpc.models import *


# python manage.py import_icpc

icpc = (
    ('Icpc', 'icpcs'),
    ('Icpc1_register_logins', 'icpc-1-s'),
    ('Icpc2_reservation_investigations', 'icpc-2-s'),
    ('Icpc3_symptoms_and_problems', 'icpc-3-s'),
    ('Icpc4_physical_examination_and_tests', 'icpc-4-s'),
    ('Icpc5_evaluation_and_diagnoses', 'icpc-5-s'),
    ('Icpc6_prescribe_medicines', 'icpc-6-s'),
    ('Icpc7_treatments', 'icpc-7-s'),
    ('Icpc8_other_health_interventions', 'icpc-8-s'),
    ('Icpc9_referral_consultations', 'icpc-9-s'),
    ('Icpc10_test_results_and_statistics', 'icpc-10-test-results-and-statistics'),
)

class Command(BaseCommand):
    help = '从需求系统中导入ICPC编码，参数：--subclass, 0-icpc总表，1~10-单独导入icpc分类编码, 11-全部导入icpc1~10分类编码'

    def run_import(self, num):
        print('正在查询总记录数……')
        url = f'https://hssc-rcms.herokuapp.com/{icpc[num][1]}'
        res = requests.get(f'{url}/count?_publicationState=preview')
        print(f'{res.text}条记录正在导入：{url}')

        pages = math.ceil(int(res.text)/100)
        
        # print('6036条记录正在导入')
        # pages = math.ceil(6036/100)

        page = 1
        i = 0

        # 每100条记录GET一次
        while page <= pages:
            res = requests.get(f'{url}?_publicationState=preview&_start={(page-1)*100}')
            res_json = res.json()

            # 从元组中把model名称转为 model class
            icpc_model= globals()[icpc[num][0]]
            for obj in res_json:
                i += 1
                try:
                    icpc_model.objects.create(
                        icpc_code = obj['icpc_code'],
                        icode = obj['icode'],
                        iname = obj['iname'],
                        iename = obj['iename'],
                        include = obj['include'],
                        criteria = obj['criteria'],
                        exclude = obj['exclude'],
                        consider = obj['consider'],
                        icd10 = obj['icd10'],
                        icpc2 = obj['icpc2'],
                        note = obj['note'],
                        pym = obj['pym'],
                    )
                except Exception as e:
                    print (f'{e}:{i}')
                else:
                    print (f'{i}')

            page += 1

        print(f'成功导入{i}条记录')


    def add_arguments(self, parser):
        parser.add_argument('--subclass', type=int)
    
    def handle(self, *args, **kwargs):
        subclass = kwargs['subclass']
        
        # 单独导入0-icpc总表，或1~10-icpc分类编码
        if subclass < 11:
            self.run_import(subclass)

        # 一次性导入1~10分类编码
        elif subclass == 11:
            for num in range(1,11):
                self.run_import(num)
        else:
            print('参数只能取值0~11，0-总表，1~10-独立分类表，11-所有分类表')
