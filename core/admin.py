from django.contrib import admin
from hssc.site import clinic_site
from core.models import *


admin.site.register(StaffTodo)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    search_fields = ('name', 'pym')
clinic_site.register(Role, RoleAdmin)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['name', 'phone']
clinic_site.register(Customer, CustomerAdmin)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    search_fields = ['name']
clinic_site.register(Staff, StaffAdmin)


class WorkgroupAdmin(admin.ModelAdmin):
    list_display = ('label', 'leader')
    readonly_fields = ['name']
admin.site.register(Workgroup, WorkgroupAdmin)
clinic_site.register(Workgroup, WorkgroupAdmin)


class OperationProcAdmin(admin.ModelAdmin):
    list_display = ['id', 'service', 'operator', 'customer', 'state', 'entry', 'parent_proc', 'contract_service_proc']
    list_display_links = ['service', 'operator', 'customer', 'state', 'entry', 'parent_proc', 'contract_service_proc']
    ordering = ['id']
admin.site.register(OperationProc, OperationProcAdmin)


@admin.register(BuessinessForm)
class BuessinessFormAdmin(admin.ModelAdmin):
    list_display = ['name_icpc', 'label', 'name', 'id']
    list_display_links = ['label', 'name',]
    fieldsets = (
        (None, {
            'fields': (('label', 'name_icpc'), 'description', ('name', 'hssc_id'), )
        }),
    )
    search_fields = ['name', 'label', 'pym']
    readonly_fields = ['name', 'hssc_id', 'meta_data']
    autocomplete_fields = ['name_icpc',]


class BuessinessFormsSettingInline(admin.TabularInline):
    model = BuessinessFormsSetting
    exclude = ['name', 'label', 'hssc_id']
    autocomplete_fields = ['buessiness_form']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name_icpc', 'label', 'name', 'id']
    list_display_links = ['label', 'name',]
    fieldsets = (
        ('基本信息', {
            'fields': (('label', 'name_icpc'), ('managed_entity', 'priority'), 'role', ('history_services_display', 'enable_queue_counter'), ('name', 'hssc_id'))
        }),
        ('作业管理', {
            'fields': ('suppliers', 'not_suitable', ('awaiting_time_frame' ,'execution_time_frame'), 'working_hours', 'cost', 'load_feedback')
        }),
        ('资源配置', {
            'fields': ('resource_materials','resource_devices','resource_knowledge')
        }),
    )
    search_fields=['label', 'pym']
    ordering = ['id']
    readonly_fields = ['name', 'hssc_id']
    inlines = [BuessinessFormsSettingInline]
    filter_horizontal = ("role",)
    autocomplete_fields = ["name_icpc"]


class ServicePackageDetailInline(admin.TabularInline):
    model = ServicePackageDetail
    exclude = ['name', 'label', 'hssc_id', 'pym']
    autocomplete_fields = ['service']

@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ['name_icpc', 'label', 'id']
    list_display_links = ['label', ]
    fieldsets = (
        (None, {
            'fields': (('label', 'name_icpc'), ('begin_time_setting', 'duration', 'awaiting_time_frame' ,'execution_time_frame'), ('name', 'hssc_id'))
        }),
    )
    search_fields=['label', 'pym']
    readonly_fields = ['name', 'hssc_id']
    inlines = [ServicePackageDetailInline]
    ordering = ['id']


@admin.register(ServiceRule)
class ServiceRuleAdmin(admin.ModelAdmin):
    list_display = ['label', 'service', 'event_rule', 'system_operand', 'next_service', 'passing_data', 'complete_feedback', 'is_active']
    list_editable = ['service', 'event_rule', 'system_operand', 'next_service', 'passing_data', 'complete_feedback', 'is_active']
    list_display_links = ['label', ]
    readonly_fields = ['name', 'hssc_id']
    autocomplete_fields = ['service', 'next_service', 'event_rule']
    ordering = ['id']


@admin.register(ManagedEntity)
class ManagedEntityAdmin(admin.ModelAdmin):
    readonly_fields = ['hssc_id', 'pym', 'name', 'model_name']


@admin.register(EventRule)
class EventRuleAdmin(admin.ModelAdmin):
    list_display = ('label', 'description', 'detection_scope', 'weight')
    list_display_links = ['label', 'description']
    search_fields=['label', 'name', 'pym']
    readonly_fields = ['hssc_id']
    ordering = ('id',)


admin.site.register(ContractServiceProc)
admin.site.register(SystemOperand)
admin.site.register(ServiceSpec)
admin.site.register(ContractService)
admin.site.register(RecommendedService)
admin.site.register(Message)

