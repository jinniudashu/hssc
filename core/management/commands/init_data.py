from django.core.management import BaseCommand
from django.contrib.auth.models import User, Group
from core.models import Staff, Customer, Operation, Service, Event, Event_instructions, Operation_proc, Instruction
from core.models import SYSTEM_EVENTS, SYSTEM_OPERAND
from dictionaries.models import *
from forms.models import Basic_personal_information
import requests


class Command(BaseCommand):
    help = '从设计系统导入设计数据：字典、角色、作业、服务、事件、指令、事件指令集'

    def handle(self, *args, **kwargs):
        # WEBSITE = 'https://hssc-formdesign.herokuapp.com/'
        WEBSITE = 'http://127.0.0.1:8000/'
        URL = {
            'dic_list': f'{WEBSITE}define_dict/dic_list/',
            'role': f'{WEBSITE}define_operand/get_roles/',
            'operation': f'{WEBSITE}define_operand/get_operations/',
            'service': f'{WEBSITE}define_operand/get_services/',
            'event': f'{WEBSITE}define_operand/get_events/',
            'instruction': f'{WEBSITE}define_operand/get_instructions/',
            'event_instruction': f'{WEBSITE}define_operand/get_event_instructions/',
        }


        # 0. 从设计系统导入字典数据
        print('开始导入字典数据...')
        res = requests.get(URL['dic_list'])
        res_json = res.json()
        print(res_json)
        for _dict in res_json:
            print(_dict)
            Dict =eval(_dict['name'].capitalize())
            values = _dict['content'].split('\n')
            print(Dict)
            try:
                Dict.objects.all().delete()  # 先删除原有字典数据
                for value in values:  # 写入新的字典数据
                    Dict.objects.create(value=value)
                    print(value)
            except:
                pass
        print('导入字典数据完成')


        # 1. 导入角色数据
        print('开始导入角色数据...')
        res = requests.get(URL['role'])
        res_json = res.json()
        Group.objects.all().delete()  # 先删除原有角色数据
        for item in res_json:
            Group.objects.create(name=item['label'])  # 使用角色中文名称作为角色名称
            # 赋予角色默认权限
            print(item['label'])
        print('导入角色数据完成')


        # 2. 导入作业数据
        print('开始导入作业数据...')
        res = requests.get(URL['operation'])
        res_json = res.json()
        Operation.objects.all().delete()  # 先删除原有作业数据
        for item in res_json:  # 写入新的作业数据
            operation = Operation.objects.create(
                name=item['name'],
                label=item['label'],
                forms=item['meta_data'],
                priority=item['priority'],
                suppliers=item['suppliers'],
                not_suitable=item['not_suitable'],
                time_limits=item['time_limits'],
                working_hours=item['working_hours'],
                frequency=item['frequency'],
                cost=item['cost'],
                load_feedback=item['load_feedback'],
                resource_materials=item['resource_materials'],
                resource_devices=item['resource_devices'],
                resource_knowledge=item['resource_knowledge'],
            )
            # 写入Operation.group 多对多字段
            groups = []
            for _role in item['group']:
                group = Group.objects.get(name=_role['label'])  # 使用角色中文名称查询角色
                groups.append(group)
            operation.group.add(*groups)
            print(operation)
        print('导入作业数据完成')


        # 3. 导入服务数据
        print('开始导入服务数据...')
        res = requests.get(URL['service'])
        res_json = res.json()
        Service.objects.all().delete()  # 先删除原有服务数据
        for item in res_json:  # 写入新的服务数据
            service = Service.objects.create(
                name=item['name'],
                label=item['label'],
                first_operation=Operation.objects.get(name=item['first_operation']['name']),
            )
            print(service)
        print('导入服务数据完成')


        # 4. 导入事件数据
        print('开始导入事件数据...')
        res = requests.get(URL['event'])
        res_json = res.json()
        Event.objects.all().delete()  # 先删除原有事件数据
        for item in res_json:  # 写入新的事件数据
            event = Event.objects.create(
                name=item['name'],
                label=item['label'],
                operation=Operation.objects.get(name=item['operation']['name']),
                description=item['description'],
                expression=item['expression'],
                parameters=item['parameters'],
                fields=item['fields'],
            )
            # 写入Event.next 多对多字段
            next_operations = []
            for _operation in item['next']:
                operation = Operation.objects.get(name=_operation['name'])
                next_operations.append(operation)
            event.next.add(*next_operations)
            print(event)
        print('导入事件数据完成')


        # 5. 导入指令数据
        print('开始导入指令数据...')
        res = requests.get(URL['instruction'])
        res_json = res.json()
        Instruction.objects.all().delete()  # 先删除原有指令数据
        for item in res_json:  # 写入新的指令数据
            instruction = Instruction.objects.create(
                name=item['name'],
                label=item['label'],
                code=item['code'],
                func=item['func'],
                description=item['description'],
            )
            print(instruction)
        print('导入指令数据完成')


        # 6. 导入事件指令集数据
        print('开始导入事件指令集数据...')
        res = requests.get(URL['event_instruction'])
        res_json = res.json()
        Event_instructions.objects.all().delete()  # 先删除原有事件指令集数据
        for item in res_json:  # 写入新的事件指令集数据
            event_instruction = Event_instructions.objects.create(
                event=Event.objects.get(name=item['event']['name']),
                instruction=Instruction.objects.get(name=item['instruction']['name']),
                order=item['order'],
                params=item['params'],
            )
            print(event_instruction)
        print('导入事件指令集数据完成')
