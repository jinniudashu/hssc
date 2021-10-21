from django.core.management import BaseCommand
from forms.form_list import form_list
from core.models import Form, Operation, Event, Event_instructions, Operation_proc


# python manage.py import_form_list

class Command(BaseCommand):
    help = '把form_list导入core.models.Form'

    # def add_arguments(self, parser):
    #     parser.add_argument('--dic', type=str)
    def handle(self, *args, **kwargs):
        # 删除原有作业进程，事件指令，事件，作业，表单
        Operation_proc.objects.all().delete()
        Event_instructions.objects.all().delete()
        Event.objects.all().delete()
        Operation.objects.all().delete()
        Form.objects.all().delete()
        
        # 导入新表单清单
        for form in form_list:
            print(form[0], form[1],form[2])
            Form.objects.create(
                name=form[0],
                label=form[1],
                style=form[2],
                fields_list=', '.join(form[3]),
            )