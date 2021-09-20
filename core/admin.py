from django.contrib import admin
from .models import Service, Operation, Event_instruction
from .models import Service_proc, Operation_proc


class Event_instructionInline(admin.TabularInline):
    model = Event_instruction
    extra = 1

class OperationAdmin(admin.ModelAdmin):
    list_display = ['name', 'icpc', 'entry', 'id']
    list_display_links = ['name', 'icpc']
    autocomplete_fields = ['icpc']
    search_fields = ['name', 'icpc']
    # inlines = [Event_instructionInline]
    ordering = ['id']
admin.site.register(Operation, OperationAdmin)


class Event_instructionAdmin(admin.ModelAdmin):
    list_display = ['operation', 'name', 'icpc', 'id']
    list_display_links = ['operation', 'name', 'icpc']
    autocomplete_fields = ['icpc']
    search_fields = ['name', 'icpc']
    ordering = ['id']
admin.site.register(Event_instruction, Event_instructionAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'icpc', 'id']
    list_display_links = ['name', 'icpc']
    autocomplete_fields = ['icpc']
    search_fields = ['name', 'icpc']
    ordering = ['id']
admin.site.register(Service, ServiceAdmin)


# admin.site.register(Service_proc)
# admin.site.register(Operation_proc)
