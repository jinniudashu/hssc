from django.core.management import BaseCommand
from forms.form_list import form_list
from core.models import Form


# python manage.py import_form_list

class Command(BaseCommand):
    help = '把form_list导入core.models.Form'

    # def add_arguments(self, parser):
    #     parser.add_argument('--dic', type=str)
    def handle(self, *args, **kwargs):
        Form.objects.all().delete()
        for form in form_list:
            print(form[0], form[1],form[2])
            Form.objects.create(
                name=form[0],
                label=form[1],
                style=form[2],
            )
    
