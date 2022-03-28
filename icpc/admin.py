from django.contrib import admin
from .models import Icpc

@admin.register(Icpc)
class IcpcAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Icpc._meta.fields]
    search_fields=["iname", "pym", "icpc_code"]
    ordering = ["icpc_code"]
    readonly_fields = [field.name for field in Icpc._meta.fields]
    actions = None

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
