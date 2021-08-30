from django.core.management import BaseCommand

from icpc.models import *
from rcms.models import Icpcs, Icpc1S, Icpc2S, Icpc3S, Icpc4S, Icpc5S, Icpc6S, Icpc7S, Icpc8S, Icpc9S, Icpc10TestResultsAndStatistics


# python manage.py export_icpc

icpc = (
    ('Icpc', 'Icpcs'),
    ('Icpc1_register_logins', 'Icpc1S'),
    ('Icpc2_reservation_investigations', 'Icpc2S'),
    ('Icpc3_symptoms_and_problems', 'Icpc3S'),
    ('Icpc4_physical_examination_and_tests', 'Icpc4S'),
    ('Icpc5_evaluation_and_diagnoses', 'Icpc5S'),
    ('Icpc6_prescribe_medicines', 'Icpc6S'),
    ('Icpc7_treatments', 'Icpc7S'),
    ('Icpc8_other_health_interventions', 'Icpc8S'),
    ('Icpc9_referral_consultations', 'Icpc9S'),
    ('Icpc10_test_results_and_statistics', 'Icpc10TestResultsAndStatistics'),
)

class Command(BaseCommand):
    help = '从测试系统中导出ICPC编码到需求管理系统，参数：--subclass, 0-icpc总表，1~10-单独导入icpc分类编码, 11-全部导入icpc1~10分类编码'

    def run_import(self, num):

        # 从元组中把model名称转为 model class
        src_model= globals()[icpc[num][0]]
        des_model= globals()[icpc[num][1]]

        objs = src_model.objects.all()
        
        print(f'{objs.count()}条记录正在导入：{icpc[num][1]}, {des_model}')

        i = 0
        for obj in objs:
            i += 1
            try:
                des_model.objects.create(
                    icpc_code = obj.icpc_code,
                    icode = obj.icode,
                    iname = obj.iname,
                    iename = obj.iename,
                    include = obj.include,
                    criteria = obj.criteria,
                    exclude = obj.exclude,
                    consider = obj.consider,
                    icd10 = obj.icd10,
                    icpc2 = obj.icpc2,
                    note = obj.note,
                    pym = obj.pym,
                )
            except Exception as e:
                print (f'{e}:{i}')
            else:
                print(i, obj.icpc_code)


        print(f'成功导入{i}条记录')


    def add_arguments(self, parser):
        parser.add_argument('--subclass', type=int)
    
    def handle(self, *args, **kwargs):
        subclass = kwargs['subclass']
        
        # 单独导入1~10-icpc分类编码
        if subclass > 0 and subclass < 11 :
            self.run_import(subclass)

        # 一次性导入1~10分类编码
        elif subclass == 11:
            for num in range(1,11):
                self.run_import(num)
        else:
            print('参数只能取值0~11，0-总表，1~10-独立分类表，11-所有分类表')
