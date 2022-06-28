from urllib import response
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
    site_url = None

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('receive_task/<int:proc_id>', self.receive_task),
            path('customer_service/<int:customer_id>', self.customer_service),
            path('search_customers/', self.search_customers),
        	path('search_services/<int:customer_id>/', self.search_services, name='search_services'),
            path('new_service/<int:customer_id>/<int:service_id>/<int:recommended_service_id>/', self.new_service, name='new_service'),
            path('new_service_schedule/<int:customer_id>/<int:service_id>', self.new_service_schedule, name='new_service_schedule'),
            path('new_service_package_schedule/<int:customer_id>/<int:service_package_id>', self.new_service_package_schedule, name='new_service_package_schedule'),
            path('update_customer_schedules/<int:customer_schedule_package_id>', self.update_customer_schedules, name='update_customer_schedules'),
        ]
        return my_urls + urls

    # 职员登录后的首页
    def index(self, request, extra_context=None):
        # extra_context = extra_context or {}
        # user = User.objects.get(username=request.user).customer

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
        from core.business_functions import get_customer_profile
        context['profile'] = get_customer_profile(customer)

        # 生成响应对象
        response = render(request, 'customer_service.html', context)

        # 向sessionStorage写入customer_id
        response.set_cookie('customer_id', kwargs['customer_id'])
        
        # 获取操作员有操作权限的服务id列表, 写入cookie
        from core.business_functions import get_operator_permitted_services
        permitted_services_id = get_operator_permitted_services(operator)
        response.set_cookie('permitted_services_id', permitted_services_id)

        return response

    # 搜索客户，返回客户列表
    def search_customers(self, request):
        from django.db.models import Q
        # 从request.POST获取search
        print('request.POST:', request.POST)
        search_text = request.POST.get('search')
        context = {}
        if search_text is None or search_text == '':
            context['customers'] = None
        else:
            context['customers'] = Customer.objects.filter(name__icontains=search_text)
        return render(request, 'customers_list.html', context)

    # 搜索服务，返回服务/服务包列表
    def search_services(self, request, **kwargs):
        # 从request.POST获取search
        print('request.POST:', request.POST)
        search_text = request.POST.get('search')
        context = {}
        # if search_text is None or search_text == '':
        #     context['services'] = None
        # else:
        context['services'] = [
            {
                'id': service.id, 
                'label': service.label,
                'enable_queue_counter': service.enable_queue_counter,
                'queue_count': OperationProc.objects.get_service_queue_count(service)
            } for service in Service.objects.filter(Q(is_system_service=False) & (Q(label__icontains=search_text) | Q(pym__icontains=search_text)))
        ]
        
        context['service_packages'] = [
            {
                'id': service_package.id, 
                'label': service_package.label,
            } for service_package in ServicePackage.objects.filter(Q(label__icontains=search_text) | Q(pym__icontains=search_text))
        ]

        context['customer_id'] = kwargs['customer_id']

        return render(request, 'services_list.html', context)

    # 创建服务
    def new_service(self, request, **kwargs):
        '''
        人工创建新服务：作业进程+表单进程
        从kwargs获取参数：customer_id, service_id
        '''
        from core.business_functions import create_service_proc, dispatch_operator
        # 从request获取参数：customer, service, operator
        customer = Customer.objects.get(id=kwargs['customer_id'])
        current_operator = User.objects.get(username=request.user).customer
        service = Service.objects.get(id=kwargs['service_id'])
        service_operator = dispatch_operator(customer, service, current_operator)
        content_type = ContentType.objects.get(app_label='service', model=service.name.lower())

        # 准备新的服务作业进程参数
        proc_params = {}
        proc_params['service'] = service
        proc_params['customer'] = customer
        proc_params['creater'] = current_operator
        proc_params['operator'] = service_operator
        proc_params['state'] = 0  # or 0 根据服务作业权限判断
        proc_params['scheduled_time'] = timezone.now() # or None 根据服务作业权限判断
        proc_params['contract_service_proc'] = None
        proc_params['content_type'] = content_type
        proc_params['form_data'] = None

        # 如果是推荐服务，解析parent_proc和passing_data
        if kwargs['recommended_service_id']:
            recommended_service = RecommendedService.objects.get(id=kwargs['recommended_service_id'])
            proc_params['parent_proc'] = recommended_service.pid
            proc_params['passing_data'] = recommended_service.passing_data
        else:
            # 人工创建服务，没有父进程
            proc_params['parent_proc'] = None
            # 人工创建服务，没有传递数据
            proc_params['passing_data'] = 0

        # 创建新的OperationProc服务作业进程实例
        new_proc = create_service_proc(**proc_params)

        # 如果请求来自可选服务，从可选服务队列中删除服务
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

    # 创建新的服务日程
    def new_service_schedule(self, request, **kwargs):
        customer_id = kwargs['customer_id']
        service_id = kwargs['service_id']
        print('customer_id:', customer_id)
        print('service_id:', service_id)
        context = {}
        return redirect('/clinic/service/customerschedule/add/')

    # 创建新的服务包计划
    def new_service_package_schedule(self, request, **kwargs):
        # 1. 创建"安排服务计划"服务进程
        customer_id = kwargs['customer_id']
        customer = Customer.objects.get(id=customer_id)
        current_operator = User.objects.get(username=request.user).customer
        service = Service.objects.get(name='CustomerSchedulePackage')
        content_type = ContentType.objects.get(app_label='service', model='customerschedulepackage')
        # 创建一个状态为“运行”的“安排服务计划”作业进程
        new_proc=OperationProc.objects.create(
            service=service,  # 服务
            customer=customer,  # 客户
            operator=current_operator,  # 作业人员
            creater=current_operator,  # 创建者
            state=2,  # 进程状态：运行
            content_type=content_type,  # 内容类型
        )

        # 2. 创建客户服务包和服务项目安排: CustomerSchedulePackage, CustomerScheduleDraft
        # 获取服务包信息: ServicePackage, ServicePackageDetail
        service_package_id = kwargs['service_package_id']
        servicepackage = ServicePackage.objects.get(id=service_package_id)
        servicepackagedetails = ServicePackageDetail.objects.filter(servicepackage=servicepackage)
        # 创建客户服务包
        from service.models import CustomerSchedulePackage, CustomerScheduleDraft
        customerschedulepackage = CustomerSchedulePackage.objects.create(
            customer=customer,  # 客户
            operator=current_operator,  # 作业人员
            creater=current_operator,  # 创建者
            pid=new_proc,  # 服务作业进程
            cpid=None,
            servicepackage=servicepackage,  # 服务包
        )
        # 创建服务项目安排
        for servicepackagedetail in servicepackagedetails:
            print('servicepackagedetail:', servicepackagedetail.cycle_frequency, type(servicepackagedetail.cycle_frequency), servicepackagedetail.cycle_times, type(servicepackagedetail.cycle_times))
            CustomerScheduleDraft.objects.create(
                schedule_package=customerschedulepackage,  # 客户服务包
                service=servicepackagedetail.service,  # 服务项目
                cycle_unit=servicepackagedetail.cycle_unit,  # 周期单位
                cycle_frequency=servicepackagedetail.cycle_frequency,  # 每周期频次
                cycle_times=servicepackagedetail.cycle_times,  # 周期总数/天数
                default_beginning_time=servicepackagedetail.default_beginning_time,  # 执行时间基准
                base_interval=servicepackagedetail.base_interval,  # 基准间隔
            )

        # 3. 更新OperationProc服务进程的form实例信息
        new_proc.object_id = customerschedulepackage.id
        new_proc.entry = f'/clinic/service/customerschedulepackage/{customerschedulepackage.id}/change'
        new_proc.save()

        return redirect(new_proc.entry)

    # 更新客户服务日程
    def update_customer_schedules(self, request, **kwargs):
        from django.forms import ModelForm, modelformset_factory, TextInput
        from service.models import CustomerSchedulePackage, CustomerSchedule
        class CustomerSchedulePackageForm(ModelForm):
            class Meta:
                model = CustomerSchedulePackage
                fields = ('customer', 'servicepackage', )

        CustomerScheduleFormset = modelformset_factory(CustomerSchedule, fields=('service', 'scheduled_time', 'scheduled_operator',), extra=0, can_delete=False)

        customerschedulepackage = CustomerSchedulePackage.objects.get(id=kwargs['customer_schedule_package_id'])
        customer_form = CustomerSchedulePackageForm(instance=customerschedulepackage)
        queryset = CustomerSchedule.objects.filter(schedule_package=customerschedulepackage)
        if request.method == 'POST':
            # customer_schedules_formset = CustomerScheduleFormset(request.POST, queryset=queryset)
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
            'fields': (('label', 'name_icpc'), ('managed_entity', 'priority', 'is_system_service'), 'role', 'history_services_display', 'enable_queue_counter', 'route_to', ('working_hours' ,'overtime'), ('name', 'hssc_id'))
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
            'fields': (('label', 'name_icpc'), 'overtime', ('name', 'hssc_id'))
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

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    search_fields = ['name']
clinic_site.register(Institution, InstitutionAdmin)

admin.site.register(CustomerServiceLog)
clinic_site.register(CustomerServiceLog)

admin.site.register(RecommendedService)
clinic_site.register(RecommendedService)

admin.site.register(Message)
clinic_site.register(Message)

admin.site.register(ExternalServiceMapping)
clinic_site.register(ExternalServiceMapping)