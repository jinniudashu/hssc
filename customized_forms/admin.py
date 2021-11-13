from django.contrib import admin
from .models import Component, SubForm, Operand_Form
from .utils import export_scripts


class Operand_FormAdmin(admin.ModelAdmin):
    actions = [export_scripts]

admin.site.register(Component)
admin.site.register(SubForm)
admin.site.register(Operand_Form, Operand_FormAdmin)
