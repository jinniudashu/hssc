from django.core.management import BaseCommand
from core.models import Staff, Customer, Operation, Event, Event_instructions, Operation_proc, Instruction
from core.models import SYSTEM_EVENTS, SOURCECODE_URL
from django.contrib.auth.models import User
import requests
import json

# python manage.py import_form_list

class Command(BaseCommand):
    help = '1. 把form_list导入core.models.Form； 2. 在core.models.Instruction中创建指令'

    # def add_arguments(self, parser):
    #     parser.add_argument('--dic', type=str)

    def handle(self, *args, **kwargs):

        # 删除原有作业进程，事件指令，事件，作业，表单，指令
        Operation_proc.objects.all().delete()
        Event_instructions.objects.all().delete()
        Event.objects.all().delete()
        Operation.objects.all().delete()
        Instruction.objects.all().delete()
        
        #############################
        # 导入作业目录
        #############################
        print('开始导入Operation...')
        res = requests.get(SOURCECODE_URL)
        res_json = res.json()[0]
        operations =eval(res_json['code'])['operand_views']
        for _o in operations:
            operation = Operation.objects.create(
                name = _o['name'],
                label = _o['label'],
                forms = _o['forms'],
            )
            # 如果是系统保留作业，生成系统保留事件SYSTEM_EVENTS
            if any(operation.name == fn[0] for fn in SYSTEM_EVENTS):
                sys_event = Event.objects.create(
                    operation = operation,
                    name = f'{operation.name}_completed',
                    label = f'{operation.label}_完成',
                    expression = 'completed',
                )
                print('生成系统保留事件：', sys_event)

        print('导入Operation完成')


        # 在core.models.Instruction中创建指令
        instruction=Instruction.objects.create(
            name='create_operation_proc',
            label='创建作业进程',
            code='cop',
            func='create_operation_proc',
            description='新建一个人工作业进程',
        )
        print('新建指令成功:', instruction)

        admin = User.objects.get(username='admin')
        # 创建一个管理员员工信息
        staff = Staff.objects.get_or_create(
            user = admin,
            name='admin',
            email='admin@test.com',
        )
        print('新建员工成功：', staff)

        # 创建一个管理员客户注册信息
        customer = Customer.objects.get_or_create(
            user = admin,
            name='admin',
        )
        print('新建客户成功：', customer)
