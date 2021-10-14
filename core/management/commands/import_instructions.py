from django.core.management import BaseCommand
from core.models import Instruction


# python manage.py import_form_list

class Command(BaseCommand):
    help = '向core.models.Instruction导入指令'

    # def add_arguments(self, parser):
    #     parser.add_argument('--dic', type=str)
    def handle(self, *args, **kwargs):
        Instruction.objects.all().delete()
        instruction=Instruction.objects.create(
            name='create_operation_proc',
            label='创建作业进程',
            code='cop',
            func='create_operation_proc',
            description='新建一个人工作业进程',
        )
        print('新建指令成功：', instruction)
    
