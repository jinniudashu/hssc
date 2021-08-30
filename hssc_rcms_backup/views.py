from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import *

# 响应需求管理系统的Webhook调用，同步ICPC总表的更改到测试系统（本系统）的ICPC总表

icpc_list = (
    (0, 'Icpcs'),
    (1, 'Icpc1S'),
    (2, 'Icpc2S'),
    (3, 'Icpc3S'),
    (4, 'Icpc4S'),
    (5, 'Icpc5S'),
    (6, 'Icpc6S'),
    (7, 'Icpc7S'),
    (8, 'Icpc8S'),
    (9, 'Icpc9S'),
    (10, 'Icpc10TestResultsAndStatistics'),
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


