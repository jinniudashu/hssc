from django.contrib import admin
from .models import Form, Service, Operation, Event, Instruction, Event_instructions
from .models import Service_proc, Operation_proc


class EventInline(admin.TabularInline):
    model = Event
    extra = 0

# class Event_instructionsInline(admin.TabularInline):
#     model = Event_instructions
#     extra = 0


class FormAdmin(admin.ModelAdmin):
    list_display = ['label', 'name', 'id']
    list_display_links = ['label', 'name', 'id']
    search_fields = ['name', 'label']
    ordering = ['id']
admin.site.register(Form, FormAdmin)


class OperationAdmin(admin.ModelAdmin):
    list_display = ['label', 'name', 'icpc', 'id']
    list_display_links = ['label', 'name', 'icpc']
    fieldsets = (
        (None, {
            'fields': (('label', 'name', 'icpc'), 'priority', ('form', 'group'), 'suppliers',)
        }),
        ('作业管理', {
            'fields': ('not_suitable', 'time_limits', 'working_hours', 'cost', 'load_feedback')
        }),
        ('资源配置', {
            'fields': ('resource_materials','resource_devices','resource_knowledge')
        }),
    )
    autocomplete_fields = ['icpc']
    search_fields = ['name', 'icpc', 'label']
    inlines = [EventInline]
    ordering = ['id']
admin.site.register(Operation, OperationAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ['label', 'name', 'operation', 'rule','id']
    list_display_links = ['label', 'name', 'operation', 'rule']
    search_fields = ['name', 'label']
    # inlines = [Event_instructionsInline]
    ordering = ['id']
admin.site.register(Event, EventAdmin)


class Operation_procAdmin(admin.ModelAdmin):
    list_display = ['id', 'operation', 'user', 'customer', 'state', 'entry', 'ppid', 'service_proc']
    list_display_links = ['operation', 'user', 'customer', 'state', 'entry', 'ppid', 'service_proc']
    ordering = ['id']
admin.site.register(Operation_proc, Operation_procAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'icpc', 'id']
    list_display_links = ['name', 'icpc']
    autocomplete_fields = ['icpc']
    search_fields = ['name', 'icpc']
    ordering = ['id']
admin.site.register(Service, ServiceAdmin)


# class Event_instructionsAdmin(admin.ModelAdmin):
#     list_display = ['event', 'instruction', 'order', 'params', 'id']
#     list_display_links = ['event', 'instruction', 'order', 'params']
#     search_fields = ['event']
#     ordering = ['id']
# admin.site.register(Event_instructions, Event_instructionsAdmin)


# class InstructionAdmin(admin.ModelAdmin):
#     list_display = ['name', 'code', 'func', 'description', 'id']
#     list_display_links = ['name', 'code', 'func']
#     search_fields = ['name']
#     ordering = ['id']
# admin.site.register(Instruction, InstructionAdmin)


# admin.site.register(Service_proc)

