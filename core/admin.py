from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.contrib.auth.models import User

from core.models import *


class ClinicSite(admin.AdminSite):
    site_header = '智益诊所管理系统'
    site_title = 'Hssc Clinic'
    index_title = '诊所工作台'
    enable_nav_sidebar = False
    index_template = 'admin/index_clinic.html'
    enable_nav_sidebar = False
    site_url = None

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('receive_task/<int:proc_id>', self.receive_task),
            path('customer_service/<int:customer_id>', self.customer_service),
        ]
        return my_urls + urls

    # 职员登录后的首页
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        user = User.objects.get(username=request.user).customer
        # 可申领的服务作业
        extra_context['unassigned_procs'] = OperationProc.objects.get_unassigned_proc(user)
        # 今日服务安排,紧要服务安排,本周服务安排
        items = []
        items.append({'title': '今日服务安排', 'todos': StaffTodo.objects.today_todos(user)})
        items.append({'title': '紧要服务安排', 'todos': StaffTodo.objects.urgent_todos(user)})
        items.append({'title': '本周服务安排', 'todos': StaffTodo.objects.week_todos(user)})
        extra_context['items'] = items

        return super().index(request, extra_context=extra_context)

    # 接受任务：把任务放入当前用户的待办列表中
    def receive_task(self, request, **kwargs):
        operation_proc = OperationProc.objects.get(id = kwargs['proc_id'])
        operation_proc.operator = User.objects.get(username=request.user).customer
        operation_proc.state = 1
        operation_proc.save()
        return redirect('/clinic/')
        

    # 客户服务首页
    def customer_service(self, request, **kwargs):
        context = {}
        customer = Customer.objects.get(id = kwargs['customer_id'])
        operator = User.objects.get(username=request.user).customer
        
        # 病例首页
        context['profile'] = customer.get_profile()

        # 已安排服务
        # context['scheduled_services'] = customer.get_scheduled_services()
        context['scheduled_services'] = [
            {
                'entry': proc.entry,
                'service': proc.service,
                'permission': bool(set(proc.service.role.all()).intersection(set(operator.staff.role.all()))),
            } for proc in customer.get_scheduled_services()]

        # 推荐服务
        context['recommanded_services'] = [
            {
                'id': recommend_service.id, 
                'service': recommend_service.service,
                'enable_queue_counter': recommend_service.service.enable_queue_counter,
                'queue_count': OperationProc.objects.get_service_queue_count(recommend_service.service)
            } for recommend_service in customer.get_recommended_services()
        ]

        # 历史服务
        context['history_services'] = customer.get_history_services()

        return render(request, 'customer_service.html', context)

clinic_site = ClinicSite(name = 'ClinicSite')


# **********************************************************************************************************************
# Service 配置 Admin
# **********************************************************************************************************************
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    search_fields = ('name', 'pym')
clinic_site.register(Role, RoleAdmin)


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
    readonly_fields = ['name', 'hssc_id']
    autocomplete_fields = ['name_icpc',]


@admin.register(ManagedEntity)
class ManagedEntityAdmin(admin.ModelAdmin):
    readonly_fields = ['hssc_id', 'pym', 'name', 'model_name']


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
            'fields': (('label', 'name_icpc'), ('managed_entity', 'priority', 'is_system_service'), 'role', 'history_services_display', 'enable_queue_counter', 'route_to', ('name', 'hssc_id'))
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


admin.site.register(SystemOperand)

@admin.register(EventRule)
class EventRuleAdmin(admin.ModelAdmin):
    list_display = ('label', 'description', 'expression', 'detection_scope', 'weight')
    list_display_links = ['label', 'description']
    search_fields=['label', 'name', 'pym']
    readonly_fields = ['hssc_id']
    ordering = ('id',)

admin.site.register(ServiceSpec)

@admin.register(ServiceRule)
class ServiceRuleAdmin(admin.ModelAdmin):
    list_display = ['label', 'service', 'event_rule', 'system_operand', 'next_service', 'passing_data', 'complete_feedback', 'is_active']
    list_editable = ['service', 'event_rule', 'system_operand', 'next_service', 'passing_data', 'complete_feedback', 'is_active']
    list_display_links = ['label', ]
    readonly_fields = ['name', 'hssc_id']
    autocomplete_fields = ['service', 'next_service', 'event_rule']
    ordering = ['id']


admin.site.register(ContractService)


# **********************************************************************************************************************
# Service 进程管理 Admin
# **********************************************************************************************************************
admin.site.register(ContractServiceProc)
clinic_site.register(ContractServiceProc)

@admin.register(OperationProc)
class OperationProcAdmin(admin.ModelAdmin):
    list_display = ['id', 'service', 'operator', 'customer', 'state', 'entry', 'parent_proc', 'contract_service_proc']
    list_display_links = ['service', 'operator', 'customer', 'state', 'entry', 'parent_proc', 'contract_service_proc']
    ordering = ['id']
clinic_site.register(OperationProc, OperationProcAdmin)


admin.site.register(StaffTodo)
clinic_site.register(StaffTodo)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['name', 'phone']
clinic_site.register(Customer, CustomerAdmin)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    search_fields = ['name']
clinic_site.register(Staff, StaffAdmin)

@admin.register(Workgroup)
class WorkgroupAdmin(admin.ModelAdmin):
    list_display = ('label', 'leader')
    readonly_fields = ['name']
clinic_site.register(Workgroup, WorkgroupAdmin)

admin.site.register(CustomerServiceLog)
clinic_site.register(CustomerServiceLog)

admin.site.register(RecommendedService)
clinic_site.register(RecommendedService)

admin.site.register(Message)
clinic_site.register(Message)
