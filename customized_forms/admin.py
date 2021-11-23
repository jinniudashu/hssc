from django.contrib import admin
from .models import Component, SubForm, Operand_View
from .utils import export_scripts


class Operand_ViewAdmin(admin.ModelAdmin):
    actions = [export_scripts]

admin.site.register(Component)
admin.site.register(SubForm)
admin.site.register(Operand_View, Operand_ViewAdmin)
