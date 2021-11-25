from django.core.management import BaseCommand
from core.models import Staff, Customer, Form, Operation, Event, Event_instructions, Operation_proc, Instruction
from forms.form_list import form_list
from customized_forms.models import BaseForm
from django.contrib.auth.models import User

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
        Form.objects.all().delete()
        Instruction.objects.all().delete()
        
        # 导入新表单清单
        for form in form_list:
            print(form[0], form[1],form[2])
            Form.objects.create(
                name=form[0],
                label=form[1],
                style=form[2],
                fields_list=', '.join(form[3]),
            )

            # 临时导入子表单定义项
            # if form[2] == 1:
            #     style = 'list'
            # else:
            #     style = 'detail'
            # BaseForm.objects.create(
            #     name=form[0],
            #     label=form[1],
            #     style=style,
            #     fields_list=', '.join(form[3]),
            # )

        # 在core.models.Instruction中创建指令
        instruction=Instruction.objects.create(
            name='create_operation_proc',
            label='创建作业进程',
            code='cop',
            func='create_operation_proc',
            description='新建一个人工作业进程',
        )
        print('新建指令成功：', instruction)

        admin = User.objects.get(username='admin')
        # 创建一个管理员员工信息
        staff = Staff.objects.create(
            user = admin,
            name='admin',
            email='admin@test.com',
        )
        staff.save()
        print('新建员工成功：', staff)

        # 创建一个管理员客户注册信息
        customer = Customer.objects.create(
            user = admin,
            name='admin',
        )
        customer.save()
        print('新建客户成功：', customer)
