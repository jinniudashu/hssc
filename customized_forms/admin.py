from django.contrib import admin
from .models import CharacterField, NumberField, DTField, ChoiceField, RelatedField, Component, BaseModel, SubForm, OperandView
from .utils import export_scripts


class OperandViewAdmin(admin.ModelAdmin):
    actions = [export_scripts]

admin.site.register(CharacterField)
admin.site.register(NumberField)
admin.site.register(DTField)
admin.site.register(ChoiceField)
admin.site.register(RelatedField)
admin.site.register(Component)
admin.site.register(BaseModel)
admin.site.register(SubForm)
admin.site.register(OperandView, OperandViewAdmin)
