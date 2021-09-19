from django.contrib import admin
from .models import Service, Operation, Event, Instruction
from .models import Service_proc, Operation_proc


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'icpc', 'init_operation', 'id']
    list_display_links = ['name', 'icpc']
    autocomplete_fields = ['icpc']
    search_fields = ['name', 'icpc']
    ordering = ['id']
admin.site.register(Service, ServiceAdmin)

class OperationAdmin(admin.ModelAdmin):
    list_display = ['name', 'icpc', 'entry', 'id']
    list_display_links = ['name', 'icpc']
    autocomplete_fields = ['icpc']
    search_fields = ['name', 'icpc']
    ordering = ['id']
admin.site.register(Operation, OperationAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'icpc', 'operation', 'id']
    list_display_links = ['name', 'icpc']
    autocomplete_fields = ['icpc']
    search_fields = ['name', 'icpc']
    ordering = ['id']
admin.site.register(Event, EventAdmin)

class InstructionAdmin(admin.ModelAdmin):
    list_display = ['service', 'event', 'next', 'id']
    list_display_links = ['service', 'event', 'next']
    search_fields = ['service', 'event', 'next']
    ordering = ['id']
admin.site.register(Instruction, InstructionAdmin)

# admin.site.register(Service_proc)
# admin.site.register(Operation_proc)
