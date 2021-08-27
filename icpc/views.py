from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import *

# 响应需求管理系统的Webhook调用，同步ICPC总表的更改到测试系统（本系统）的ICPC子类表

icpc_list = (
    (0, 'Icpc'),
    (1, 'Icpc1_register_logins'),
    (2, 'Icpc2_reservation_investigations'),
    (3, 'Icpc3_symptoms_and_problems'),
    (4, 'Icpc4_physical_examination_and_tests'),
    (5, 'Icpc5_evaluation_and_diagnoses'),
    (6, 'Icpc6_prescribe_medicines'),
    (7, 'Icpc7_treatments'),
    (8, 'Icpc8_other_health_interventions'),
    (9, 'Icpc9_referral_consultations'),
    (10, 'Icpc10_test_results_and_statistics'),
)

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        res = json.loads(request.body)
        event = res['event']
        model = res['model']
        entry = res.get('entry')
        print (entry)
        if model =='icpc':
            icpc_code = entry['icpc_code']
            if 'create' in event:
                # 从元组中把model名称转为 model class
                des_model= globals()[icpc_list[entry['subclass']['id']][1]]
                des_model.objects.create(
                    icpc_code = entry['icpc_code'],
                    icode = entry['icode'],
                    iname = entry['iname'],
                    iename = entry['iename'],
                    include = entry['include'],
                    criteria = entry['criteria'],
                    exclude = entry['exclude'],
                    consider = entry['consider'],
                    icd10 = entry['icd10'],
                    icpc2 = entry['icpc2'],
                    note = entry['note'],
                    pym = entry['pym'],
                )
                print('icpc create')

            elif 'update' in event:
                des_model = globals()[icpc_list[entry['subclass']['id']][1]].objects.filter(icpc_code = icpc_code).update(
                    icpc_code = entry.get('icpc_code'),
                    icode = entry.get('icode'),
                    iname = entry.get('iname'),
                    iename = entry.get('iename'),
                    include = entry.get('include'),
                    criteria = entry.get('criteria'),
                    exclude = entry.get('exclude'),
                    consider = entry.get('consider'),
                    icd10 = entry.get('icd10'),
                    icpc2 = entry.get('icpc2'),
                    note = entry.get('note'),
                    pym = entry.get('pym'),
                )
                print('icpc update')

            elif 'delete' in event:
                des_model = globals()[icpc_list[entry['subclass']['id']][1]].objects.filter(icpc_code = icpc_code)
                des_model.delete()
                print('icpc deleted')

    return HttpResponse('icpc updated')


