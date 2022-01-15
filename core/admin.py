from django.contrib import admin
from .models import Staff, Customer, Service, Operation, Event, Instruction, Event_instructions
from .models import Service_proc, Operation_proc

admin.site.register(Staff)
admin.site.register(Customer)

class EventInline(admin.TabularInline):
    model = Event
    extra = 0


class OperationAdmin(admin.ModelAdmin):
    list_display = ['label', 'name', 'icpc', 'id']
    list_display_links = ['label', 'name', 'icpc']
    readonly_fields = ['forms']
    fieldsets = (
        (None, {
            'fields': (('label', 'name', 'icpc'), 'priority', 'group',)
        }),
        ('作业管理', {
            'fields': ('not_suitable', 'time_limits', 'working_hours', 'cost', 'load_feedback')
        }),
        ('资源配置', {
            'fields': ('resource_materials','resource_devices','resource_knowledge')
        }),
        ('元数据', {
            'fields': ('forms', )
        })
    )
    autocomplete_fields = ['icpc']
    search_fields = ['name', 'icpc', 'label']
    inlines = [EventInline]
    ordering = ['id']
admin.site.register(Operation, OperationAdmin)


class EventAdmin(admin.ModelAdmin):
#     change_form_template = "core/templates/change_form.html"
    list_display = ['label', 'name', 'operation', 'id']
    list_display_links = ['label', 'name', 'operation',]
    search_fields = ['name', 'label']
    readonly_fields = ['parameters']
    ordering = ['id']
admin.site.register(Event, EventAdmin)


class Operation_procAdmin(admin.ModelAdmin):
    list_display = ['id', 'operation', 'operator', 'customer', 'state', 'entry', 'ppid', 'service_proc']
    list_display_links = ['operation', 'operator', 'customer', 'state', 'entry', 'ppid', 'service_proc']
    ordering = ['id']
admin.site.register(Operation_proc, Operation_procAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'icpc', 'id']
    list_display_links = ['name', 'icpc']
    autocomplete_fields = ['icpc']
    search_fields = ['name', 'icpc']
    ordering = ['id']
admin.site.register(Service, ServiceAdmin)


class Event_instructionsAdmin(admin.ModelAdmin):
    list_display = ['event', 'instruction', 'order', 'params', 'id']
    list_display_links = ['event', 'instruction', 'order', 'params']
    search_fields = ['event']
    ordering = ['id']
admin.site.register(Event_instructions, Event_instructionsAdmin)


class InstructionAdmin(admin.ModelAdmin):
    list_display = ['label', 'name', 'code', 'func', 'description', 'id']
    list_display_links = ['label', 'name', 'code', 'func']
    search_fields = ['name']
    ordering = ['id']
admin.site.register(Instruction, InstructionAdmin)


# admin.site.register(Service_proc)

