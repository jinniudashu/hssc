from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q
from django.conf import settings
from django.forms import ModelForm, modelformset_factory

from core.models import *


class ClinicSite(admin.AdminSite):
    site_header = '智益诊所管理系统'
    site_title = 'Hssc Clinic'
    index_title = '诊所工作台'
    enable_nav_sidebar = False
    index_template = 'admin/index_clinic.html'
    site_url = None

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('manage_task/', self.manage_task),
            path('customer_service/<int:customer_id>/', self.customer_service),
            path('search_customers/', self.search_customers),
        	path('search_services/<int:customer_id>/', self.search_services, name='search_services'),
            path('new_service/<int:customer_id>/<int:service_id>/<int:recommended_service_id>/', self.new_service, name='new_service'),
            path('new_service_schedule/<int:customer_id>/<int:service_id>/', self.new_service_schedule, name='new_service_schedule'),
            path('update_customer_schedules/<int:customer_schedule_package_id>/', self.update_customer_schedules, name='update_customer_schedules'),
        ]
        return my_urls + urls

    # 职员登录后的首页
    def index(self, request, extra_context=None):
        # extra_context = extra_context or {}
        # user = User.objects.get(username=request.user).customer
        return super().index(request, extra_context=extra_context)

    # 管理任务状态
    def manage_task(self, request, **kwargs):
        operator = User.objects.get(username=request.user).customer
        proc_id = request.GET.get('proc_id', None)
        proc = OperationProc.objects.get(id = proc_id)
        op_code = request.GET.get('op_code', None)

        # op_code: RECEIVE, ROLLBACK, SUSPEND_OR_RESUME, CANCEL, SHIFT
        if op_code == 'RECEIVE':
            proc.receive_task(operator)
        elif op_code == 'ROLLBACK':
            proc.rollback_task()
        elif op_code == 'SUSPEND_OR_RESUME':
            proc.suspend_or_resume_task()
        elif op_code == 'CANCEL':
            proc.cancel_task(operator)
        elif op_code == 'SHIFT':
            operator_id = request.GET.get('operator_id', None)
            shift_operator = Customer.objects.get(id = operator_id)
            proc.shift_task(shift_operator)
        return redirect('/clinic/')
    
    # 客户服务首页
    def customer_service(self, request, **kwargs):
        context = {}
        customer = Customer.objects.get(id = kwargs['customer_id'])
        operator = User.objects.get(username=request.user).customer
        
        # 病例首页
        from core.business_functions import get_customer_profile
        context['profile'] = get_customer_profile(customer)

        # 生成响应对象
        response = render(request, 'customer_service.html', context)

        # 向sessionStorage写入customer_id
        response.set_cookie('customer_id', kwargs['customer_id'])
        response.set_cookie('operator_id', operator.id)
        response.set_cookie('environment', settings.DJANGO_ENV)
        
        # # 获取操作员有操作权限的服务id列表, 写入cookie
        permitted_services_id = [
            service.id
            for service in Service.objects.filter(service_type__in=[1,2]) 
            if set(service.role.all()).intersection(set(operator.staff.role.all()))
        ]
        response.set_cookie('permitted_services_id', permitted_services_id)

        return response

    # 搜索客户，返回客户列表
    def search_customers(self, request):
        from core.business_functions import search_customer_profile_list
        # 从request.POST获取search
        search_text = request.POST.get('search')
        context = {}
        if search_text is None or search_text == '':
            context['customer_profiles'] = None
        else:
            # 获取客户基本信息
            customer_profiles, customer_profile_fields_header = search_customer_profile_list(search_text)
            context['customer_profiles'] = customer_profiles
            context['customer_profile_fields_header'] = customer_profile_fields_header
        return render(request, 'customers_list.html', context)

    # 搜索服务，返回服务列表
    def search_services(self, request, **kwargs):
        # 从request.POST获取search
        search_text = request.POST.get('search')

        context = {}
        context['services'] = [
            {
                'id': service.id, 
                'label': service.label,
                'type': service.service_type,
                'enable_queue_counter': service.enable_queue_counter,
                'queue_count': OperationProc.objects.get_service_queue_count(service)
            } for service in Service.objects.filter(Q(service_type__in=[1,2]) & (Q(label__icontains=search_text) | Q(pym__icontains=search_text))) if service.label != '安排服务'
        ]
        context['customer_id'] = kwargs['customer_id']

        return render(request, 'services_list.html', context)

    # 创建服务
    def new_service(self, request, **kwargs):
        '''
        人工创建新服务：作业进程+表单进程
        从kwargs获取参数：customer_id, service_id
        '''
        from core.business_functions import create_service_proc, dispatch_operator, eval_scheduled_time
        # 从request获取参数：customer, service, operator
        customer = Customer.objects.get(id=kwargs['customer_id'])
        current_operator = User.objects.get(username=request.user).customer
        service = Service.objects.get(id=kwargs['service_id'])
        service_operator = dispatch_operator(customer, service, current_operator, timezone.now(), None)

        # 区分服务类型是"1 管理调度服务"还是"2 诊疗服务"，获取ContentType
        if service.service_type == 1:
            content_type = ContentType.objects.get(app_label='service', model='customerschedulepackage')
        else:
            content_type = ContentType.objects.get(app_label='service', model=service.name.lower())

        # 准备新的服务作业进程参数
        proc_params = {}
        proc_params['service'] = service
        proc_params['customer'] = customer
        proc_params['creater'] = current_operator
        proc_params['operator'] = service_operator
        proc_params['priority_operator'] = None
        proc_params['state'] = 0  # or 0 根据服务作业权限判断

        # 如果当前操作员即是服务作业员，计划执行时间为当前时间，否则估算计划执行时间
        if current_operator == service_operator:
            proc_params['scheduled_time'] = timezone.now()
        else:
            proc_params['scheduled_time'] = eval_scheduled_time(service, service_operator)

        proc_params['contract_service_proc'] = None
        proc_params['content_type'] = content_type
        proc_params['form_data'] = None
        proc_params['apply_to_group'] = False
        proc_params['coroutine_result'] = None
        
        # 如果是推荐服务，解析parent_proc和passing_data
        if kwargs['recommended_service_id']:
            recommended_service = RecommendedService.objects.get(id=kwargs['recommended_service_id'])
            proc_params['parent_proc'] = recommended_service.pid
            proc_params['passing_data'] = recommended_service.passing_data

            # 获取父进程的表单数据
            field_names = [field.name for field in recommended_service.pid.content_object._meta.get_fields()][12:]
            form_data = {}
            for field_name in field_names:
                field_value = getattr(recommended_service.pid.content_object, field_name)
                # 如果字段是多对多字段，则获取QuerySet
                if isinstance(field_value, models.Manager):
                    field_value = field_value.all()
                form_data[field_name] = field_value                
            proc_params['form_data'] = form_data

        else:
            # 人工创建服务，没有父进程
            proc_params['parent_proc'] = None
            # 人工创建服务，没有传递数据
            proc_params['passing_data'] = 0

        # 创建新的OperationProc服务作业进程实例
        new_proc = create_service_proc(**proc_params)

        # *************************************************
        # 管理可选服务队列
        # *************************************************
        # 如果请求来自一个可选服务条目，从可选服务队列中删除该条目
        if kwargs['recommended_service_id']:
            RecommendedService.objects.get(id=kwargs['recommended_service_id']).delete()

        # 如果开单给作业员本人，进入修改界面
        if service_operator == current_operator:
            # 重定向到/clinic/service/model/id/change
            return redirect(new_proc.entry)
        else:  # 否则显示提示消息：开单成功
            from django.contrib import messages
            messages.add_message(request, messages.INFO, f'{service.label}已开单')
            return redirect(customer)

    # 安排服务/创建新的服务日程
    def new_service_schedule(self, request, **kwargs):
        from core.business_functions import eval_scheduled_time, create_customer_schedule
        # 1. 创建"安排服务计划"服务进程
        customer_id = kwargs['customer_id']
        customer = Customer.objects.get(id=customer_id)
        current_operator = User.objects.get(username=request.user).customer
        service = Service.objects.get(name='CustomerSchedule')
        content_type = ContentType.objects.get(app_label='service', model='customerschedule')
        # 创建一个状态为“运行”的“安排服务计划”作业进程
        new_proc=OperationProc.objects.create(
            service=service,  # 服务
            customer=customer,  # 客户
            operator=current_operator,  # 作业人员
            creater=current_operator,  # 创建者
            scheduled_time=timezone.now(),  # 计划执行时间
            state=2,  # 进程状态：运行
            content_type=content_type,  # 内容类型
            overtime=service.overtime,  # 超时时间
            working_hours=service.working_hours,  # 工作时间
        )

        # 2. 创建服务计划安排: CustomerSchedule
        params = {
            'customer': customer,
            'operator': current_operator,
            'creater': current_operator,
            'service': Service.objects.get(id=kwargs['service_id']),  # 服务
            'scheduled_time': eval_scheduled_time(service, None),
            'pid': new_proc,
        }
        customer_schedule = create_customer_schedule(**params)  # 创建服务计划安排

        # 3. 更新OperationProc服务进程的form实例信息
        new_proc.object_id = customer_schedule.id
        new_proc.entry = f'/clinic/service/customerschedule/{customer_schedule.id}/change'
        new_proc.save()

        return redirect(new_proc.entry)

    # 更新客户服务日程
    def update_customer_schedules(self, request, **kwargs):
        from service.models import CustomerSchedulePackage, CustomerSchedule
        class CustomerSchedulePackageForm(ModelForm):
            class Meta:
                model = CustomerSchedulePackage
                fields = ('customer', 'servicepackage', 'start_time')

        CustomerScheduleFormset = modelformset_factory(CustomerSchedule, fields=('service', 'scheduled_time', 'scheduled_operator',), extra=0, can_delete=False)
        customerschedulepackage = CustomerSchedulePackage.objects.get(id=kwargs['customer_schedule_package_id'])
        customer_form = CustomerSchedulePackageForm(instance=customerschedulepackage)
        queryset = CustomerSchedule.objects.filter(schedule_package=customerschedulepackage).order_by('scheduled_time')
        if request.method == 'POST':
            customer_schedules_formset = CustomerScheduleFormset(request.POST)
            if customer_schedules_formset.is_valid():
                customer_schedules_formset.save()        
            return redirect(customerschedulepackage.customer)
        else:
            customer_schedules_formset = CustomerScheduleFormset(queryset=queryset)
            context = {
                'customer_form': customer_form,
                'formset': customer_schedules_formset,
            }
            return render(request, 'customerschedule_update.html', context)

clinic_site = ClinicSite(name = 'ClinicSite')


# **********************************************************************************************************************
# Service 配置 Admin
# **********************************************************************************************************************
@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    search_fields = ('name', 'pym')
clinic_site.register(Medicine, MedicineAdmin)


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
            'fields': (('label', 'name_icpc'), 'description', ('api_fields', 'name', 'hssc_id'), )
        }),
    )
    search_fields = ['name', 'label', 'pym']
    readonly_fields = ['api_fields', 'name', 'hssc_id']
    autocomplete_fields = ['name_icpc',]
clinic_site.register(BuessinessForm, BuessinessFormAdmin)


@admin.register(ManagedEntity)
class ManagedEntityAdmin(admin.ModelAdmin):
    readonly_fields = ['hssc_id', 'pym', 'name', 'model_name', 'header_fields_json']


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
            'fields': (('label', 'name_icpc'), ('managed_entity', 'priority', 'service_type'), 'role', 'history_services_display', 'enable_queue_counter', 'route_to', ('working_hours' ,'overtime'), ('name', 'hssc_id'))
        }),
        ('管理调度', {
            'fields': ('arrange_service_package', 'arrange_service')
        }),
        ('质控管理', {
            'fields': ('follow_up_required', 'follow_up_interval', 'follow_up_service')
        }),
        ('作业管理', {
            'fields': ('suppliers', 'not_suitable', 'cost', 'load_feedback')
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
clinic_site.register(Service, ServiceAdmin)

@admin.register(L1Service)
class L1ServiceAdmin(admin.ModelAdmin):
    list_display = ['label', 'name', 'id']
    list_display_links = ['label', 'name',]
    search_fields=['label', 'pym']
    ordering = ['id']
    readonly_fields = ['hssc_id']
    filter_horizontal = ("role",)
    autocomplete_fields = ["start_service", "end_service", ]
clinic_site.register(L1Service, L1ServiceAdmin)

@admin.register(CycleUnit)
class CycleUnitAdmin(admin.ModelAdmin):
    list_display = ['cycle_unit', 'days',]
    list_display_links = ['cycle_unit', 'days',]
    readonly_fields = ['hssc_id', 'name', 'pym']


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
            'fields': (('label', 'name_icpc'), ('name', 'hssc_id'))
        }),
    )
    search_fields=['label', 'pym']
    readonly_fields = ['name', 'hssc_id']
    inlines = [ServicePackageDetailInline]
    ordering = ['id']


admin.site.register(SystemOperand)


@admin.register(EventRule)
class EventRuleAdmin(admin.ModelAdmin):
    list_display = ('label', 'description', 'expression', 'detection_scope', 'event_type')
    list_display_links = ['label', 'description']
    search_fields=['label', 'name', 'pym']
    readonly_fields = ['hssc_id']
    ordering = ('id',)


@admin.register(ServiceRule)
class ServiceRuleAdmin(admin.ModelAdmin):
    list_display = ['label', 'service', 'event_rule', 'system_operand', 'next_service', 'passing_data', 'apply_to_group','complete_feedback', 'is_active']
    list_editable = ['service', 'event_rule', 'system_operand', 'next_service', 'passing_data', 'apply_to_group','complete_feedback', 'is_active']
    list_display_links = ['label', ]
    readonly_fields = ['name', 'hssc_id']
    autocomplete_fields = ['service', 'next_service', 'event_rule']
    ordering = ['id']
    search_fields = ['label', 'service__name__icontains', 'next_service__name__icontains', 'event_rule__name__icontains']

admin.site.register(ContractService)


# **********************************************************************************************************************
# Service 进程管理 Admin
# **********************************************************************************************************************
admin.site.register(ContractServiceProc)
clinic_site.register(ContractServiceProc)

@admin.register(OperationProc)
class OperationProcAdmin(admin.ModelAdmin):
    list_display = ['id', 'task_proc', 'service', 'operator', 'customer', 'state', 'scheduled_time', 'coroutine', 'entry', 'parent_proc']
    list_display_links = ['service', 'operator', 'customer', 'state', 'entry', 'parent_proc']
    ordering = ['id']


class CustomOperationProcForm(ModelForm):
    class Meta:
        model = OperationProc
        fields = ['service', 'operator', 'scheduled_time']

    # def __init__(self, *args, **kwargs):
    #     print('****trace****')
    #     super().__init__(*args, **kwargs)
    #     # 如果这个表单的实例已经有一个选择的service
    #     print(self.instance)
    #     print(self.instance.service)
    #     if self.instance and self.instance.service:
    #         from core.models import Staff
    #         # 获取所有该service关联的roles
    #         roles = self.instance.service.role.all()
    #         # 过滤选择Staff.role在roles里的员工
    #         print(roles)
    #         self.fields['operator'].queryset = Staff.objects.filter(role__in=roles).distinct()

    # def get_form(self, request, obj=None, **kwargs):
    #     # 使用你的自定义表单类
    #     return CustomOperationProcForm

class AssignOperatorAdmin(OperationProcAdmin):

    form = CustomOperationProcForm
    list_display = ['service', 'operator', 'scheduled_time']
    list_editable = ('operator', 'scheduled_time')
    list_display_links = None
    actions = None

    # 隐藏"Add"按钮
    def has_add_permission(self, request):
        return False
    
    def get_queryset(self, request):
        # 获取原始的 QuerySet
        queryset = super().get_queryset(request)
        queryset = queryset.filter(operator__isnull=True)
        return queryset
    
    def response_change(self, request, obj):
        # 按照service.route_to的配置跳转
        if obj.service.route_to == 'CUSTOMER_HOMEPAGE':
            return redirect(obj.customer)
        else:
            return redirect('index')


    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     from core.models import Staff
    #     if db_field.name == "operator":
    #         # 获取所有该service关联的roles
    #         print('*****trace******')
    #         print(request)
    #         print(request.GET.get('service'))
    #         print('formfield_for_foreignkey',self)
            # roles = self.instance.service.role.all()
            # # 过滤选择Staff.role在roles里的员工
            # print(roles)
            # kwargs["queryset"] = Staff.objects.filter(role__in=roles).distinct()
            # self.fields['operator'].queryset = Staff.objects.filter(role__in=roles).distinct()

        # return super().formfield_for_foreignkey(db_field, request, **kwargs)

clinic_site.register(OperationProc, AssignOperatorAdmin)

@admin.register(TaskProc)
class TaskProcAdmin(admin.ModelAdmin):
    list_display = ['id', 'l1_service', 'state', 'operator', 'customer', 'parent_proc', 'created_time', 'completed_time',]
    list_display_links = ['l1_service', 'state', 'operator', 'customer', 'parent_proc', 'created_time', 'completed_time',]
    ordering = ['id']
clinic_site.register(TaskProc, TaskProcAdmin)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['name', 'phone']
clinic_site.register(Customer, CustomerAdmin)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    search_fields = ['name', 'hssc_id']
clinic_site.register(Staff, StaffAdmin)

@admin.register(Workgroup)
class WorkgroupAdmin(admin.ModelAdmin):
    list_display = ('label', 'leader')
    readonly_fields = ['name', 'hssc_id']
    search_fields = ['label', 'leader']

clinic_site.register(Workgroup, WorkgroupAdmin)

@admin.register(VirtualStaff)
class VirtualStaffAdmin(admin.ModelAdmin):
    list_display = ('label', 'workgroup', 'staff')
    readonly_fields = ['name', 'hssc_id']
    search_fields = ['label', 'staff', 'workgroup']
    autocomplete_fields = ['staff', 'workgroup']
clinic_site.register(VirtualStaff, VirtualStaffAdmin)

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    search_fields = ['name', 'hssc_id']
clinic_site.register(Institution, InstitutionAdmin)

admin.site.register(CustomerServiceLog)
clinic_site.register(CustomerServiceLog)

@admin.register(RecommendedService)
class RecommendedServiceAdmin(admin.ModelAdmin):
    list_display = ('customer', 'service', 'pid', 'age')
    list_display_links = ('customer', 'service', 'pid', 'age')
clinic_site.register(RecommendedService)

admin.site.register(Message)
clinic_site.register(Message)

admin.site.register(ExternalServiceMapping)
clinic_site.register(ExternalServiceMapping)


# 承保人员清单可导入
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class ChengBaoRenYuanQingDanResource(resources.ModelResource):
    class Meta:
        model = ChengBaoRenYuanQingDan
        # exclude = ['LastCycleDate']

class ChengBaoRenYuanQingDanAdmin(ImportExportModelAdmin):
    resource_class = ChengBaoRenYuanQingDanResource
admin.site.register(ChengBaoRenYuanQingDan, ChengBaoRenYuanQingDanAdmin)



# **********************************************************************************************************************
# 业务数据备份
# **********************************************************************************************************************

from django.http import HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
import json
from time import time

# core中每个需要备份的model都需要在这里添加
# 不备份在其他表新增内容时自动插入内容的表，Component, RelateFieldModel
Backup_core_models = [
    Customer,
    ContractServiceProc,
    OperationProc,
    Institution,
    Staff,
    Workgroup,
    VirtualStaff,
    CustomerServiceLog,
    RecommendedService,
    Message,
    Medicine,
    ChengBaoRenYuanQingDan,
]

@admin.register(BackupData)
class BackupDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_time')
    # 增加一个自定义按钮“备份设计数据”
    change_list_template = 'backup_data_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('backup_data/', self.backup_data),
        ]
        return my_urls + urls

    # 备份设计数据
    def backup_data(self, request):
        backup_data = {}
        for model in Backup_core_models:
            _model = model.__name__.lower()
            backup_data[_model]=model.objects.backup_data()
            json.dumps(backup_data[_model], indent=4, ensure_ascii=False, cls=DjangoJSONEncoder)
        
        backup_name = str(int(time()))
        # 写入数据库
        result = BackupData.objects.create(
            name = backup_name,
            code = json.dumps(backup_data, indent=4, ensure_ascii=False, cls=DjangoJSONEncoder),
        )
        print(f'设计数据备份成功, id: {result}')

        # 写入json文件
        print('开始写入json文件...')
        with open(f'./core/backup/data_{backup_name}.json', 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=4, ensure_ascii=False, cls=DjangoJSONEncoder)
            print(f'ICPC写入成功, id: {backup_name}')

        return HttpResponseRedirect("../")
 