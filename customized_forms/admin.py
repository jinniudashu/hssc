from django.contrib import admin
from time import time

from .models import CharacterField, NumberField, DTField, ChoiceField, RelatedField, Component, BaseModel, BaseForm, OperandView
from .utils import generate_models_forms_scripts, generate_views_urls_templates_scripts


def copy_form(modeladmin, request, queryset):
    for obj in queryset:
        t = int(time())
        BaseForm.objects.create(
            name=f'{obj.name}_query_{t}',
            label=f'{obj.label}_查询视图_{t}',
            basemodel=obj.basemodel,
            is_inquiry=True,
            style=obj.style,
            display_fields=obj.display_fields,
        )

copy_form.short_description = '生成查询视图'


class CharacterFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name']

class NumberFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name']

class DTFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name']

class ChoiceFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name']

class RelatedFieldAdmin(admin.ModelAdmin):
    readonly_fields = ['name']

class ComponentAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'label', 'content_type', 'object_id']

class BaseModelAdmin(admin.ModelAdmin):
    readonly_fields = ['name']
    actions = [generate_models_forms_scripts]

class BaseFormAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'basemodel']
    actions = [copy_form]

class OperandViewAdmin(admin.ModelAdmin):
    readonly_fields = ['name']
    actions = [generate_views_urls_templates_scripts]

admin.site.register(CharacterField, CharacterFieldAdmin)
admin.site.register(NumberField, NumberFieldAdmin)
admin.site.register(DTField, DTFieldAdmin)
admin.site.register(ChoiceField, ChoiceFieldAdmin)
admin.site.register(RelatedField, RelatedFieldAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(BaseModel, BaseModelAdmin)
admin.site.register(BaseForm, BaseFormAdmin)
admin.site.register(OperandView, OperandViewAdmin)
