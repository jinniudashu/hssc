from django.core.management import BaseCommand
import requests

from dictionaries.models import *


# python manage.py import_dic

class Command(BaseCommand):
    help = '从需求系统的dictionary中导入字典编码（单个字典100条以内），参数：--dic, all-导入所有字典，dicname-导入单个字典。'

    # 只能导入100条以内的记录
    def run_import(self, dic):
        id = dic['id']
        name = dic['name'].strip()
        label = dic['label']
        print(f'正在导入 {name} ...')

        # GraphQl style ===================
        query = """
            query getDicData($id: ID!){
                dictionary(id: $id){
                    id
                    name
                    label
                    dictionary_data{
                        value
                        score
                    }
                }
            }              
        """
        variables = {'id': id}
        url = 'https://hssc-rcms.herokuapp.com/graphql'
        res = requests.post(url, json={'query': query, 'variables': variables})

        print(res.text)
        data = res.json()['data']['dictionary']

        # 如果data['dictionary_data']内有记录，导入
        if len(data['dictionary_data']) > 0:
            # 把name 转为 model class
            Dic_model= globals()[name.capitalize()]
            i = 0
            for dic in data['dictionary_data']:
                i += 1
                try:
                    Dic_model.objects.create(
                        name = dic['value'],
                        score = dic['score'],
                    )
                except:
                    print (f'Error:{i}')
                else:
                    print (dic['value'], dic['score'])

            print(f'{name}: 成功导入{i}条记录')
        else:
            print('空字典')


    def add_arguments(self, parser):
        parser.add_argument('--dic', type=str)
    
    def handle(self, *args, **kwargs):

        dic = kwargs['dic']

        if dic:
            dic = dic.lower()
            dic_list_url = 'https://hssc-rcms.herokuapp.com/dictionaries'

            # 参数为'all', 导入所有字典
            if dic == 'all':
                # 获取字典目录
                count = requests.get(f'{dic_list_url}/count')
                if int(count.text) > 0:
                    print(f'即将导入{count.text}个字典...')
                    res = requests.get('https://hssc-rcms.herokuapp.com/dictionaries')
                    dic_list = res.json()
                    #逐一导入字典
                    for dic in dic_list:
                        self.run_import(dic)
                else:
                    print('all-没有找到可以导入的字典！')

            # 参数为其它, 导入单个字典
            elif dic:
                # 验证字典表是否存在
                res = requests.get(f'{dic_list_url}?name={dic}')
                if len(res.json()) == 1:
                    dic = res.json()[0]
                    self.run_import(dic)
                else:
                    print(f'没有这个字典{dic}')
        else:
            print('需要提供一个字典名作为参数！ --dic [字典名]')
