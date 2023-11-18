from django.contrib import admin
from django.shortcuts import redirect
from django.forms import ModelForm

from core.admin import clinic_site
from core.signals import operand_finished
from core.business_functions import get_services_schedule, create_customer_service_log
from service.models import *

class HsscFormAdmin(admin.ModelAdmin):
    list_fields = ['name', 'id']
    exclude = ["hssc_id", "label", "name", "customer", "operator", "creater", "pid", "cpid", "slug", "created_time", "updated_time", "pym"]
    view_on_site = False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        # base_form = 'base_form'
        # extra_context['base_form'] = base_form
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if any(key.endswith('-TOTAL_FORMS') for key in request.POST):
            # 表单数据包含InlineModelAdmin 实例, 由save_formset发送服务作业完成信号
            # 保存obj到request for later retrieval in save_formset
            request._saved_obj = obj                
        else: # 表单数据不包含InlineModelAdmin 实例, 由save_model发送服务作业完成信号
            # 把表单内容存入CustomerServiceLog
            log = create_customer_service_log(form.cleaned_data, None, obj)

            print('操作完成(save_model)：', obj.pid)
            operand_finished.send(sender=self, pid=obj.pid, request=request, form_data=form.cleaned_data, formset_data=None)

    def save_formset(self, request, form, formset, change):
        super().save_formset(request, form, formset, change)

        # Retrieve obj from the request
        obj = getattr(request, '_saved_obj', None)

        form_data = form.cleaned_data
        formset_data = formset.cleaned_data

        # 把表单明细内容存入CustomerServiceLog
        log = create_customer_service_log(form_data, formset_data, obj)

        print('操作完成(save_formset)：', obj.pid)
        operand_finished.send(sender=self, pid=obj.pid, request=request, form_data=form_data, formset_data=formset_data)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def response_change(self, request, obj):
        # # 如果是创建服务包计划，保存后跳转到修改服务计划列表的页面
        # if obj.__class__.__name__ == 'CustomerSchedulePackage':
        #     schedule_list = CustomerScheduleList.objects.get(schedule_package=obj)
        #     print('Change CustomerSchedulePackage', obj, 'to', schedule_list)
        #     return redirect(f'/clinic/service/customerschedulelist/{schedule_list.id}/change/')

        # 查找以obj.pid为父进程的所有子进程
        children_procs = obj.pid.children()
        # 过滤出proc.operator为None的进程,构造列表
        none_operator_procs = [proc for proc in children_procs if proc.operator == None]
        # 进入人工指派操作员页面
        if none_operator_procs:
            return redirect('/clinic/assign_operator/' + str(obj.pid.id) + '/')
        
        # 按照service.route_to的配置跳转
        if obj.pid.service.route_to == 'CUSTOMER_HOMEPAGE':
            return redirect(obj.customer)
        else:
            return redirect('index')


class CustomerScheduleAdmin(HsscFormAdmin):
    exclude = ["hssc_id", "label", "name", "operator", "creater", "pid", "cpid", "slug", "created_time", "updated_time", "pym", 'customer_schedule_list', 'schedule_package', ]
    autocomplete_fields = ["scheduled_operator", ]
    list_display = ['customer', 'service', 'scheduled_time', 'scheduled_operator', 'priority_operator', 'pid', 'overtime', 'is_assigned', 'operator', 'creater', ]
    list_editable = ['scheduled_time', 'scheduled_operator', 'overtime', 'is_assigned']
    readonly_fields = ['customer', 'service']
    filter_horizontal = ('reference_operation',)
    ordering = ('customer_schedule_list', 'created_time', 'scheduled_time',)

clinic_site.register(CustomerSchedule, CustomerScheduleAdmin)
admin.site.register(CustomerSchedule, CustomerScheduleAdmin)

class CustomerScheduleInline(admin.TabularInline):
    model = CustomerSchedule
    extra = 0
    can_delete = False
    exclude = ["hssc_id", "label", "name", "operator", "creater", "pid", "cpid", "slug", 'customer', 'schedule_package', 'is_assigned']
    autocomplete_fields = ["scheduled_operator", ]


class CustomerScheduleListAdmin(admin.ModelAdmin):
    exclude = ["hssc_id", "label", "name", "operator", "creater", "pid", "cpid", "slug", "created_time", "updated_time", "pym"]
    fieldsets = ((None, {'fields': (('customer', 'plan_serial_number', ), )}),)
    readonly_fields = ['customer', 'plan_serial_number', ]
    inlines = [CustomerScheduleInline, ]

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def response_change(self, request, obj):
        return redirect(obj.customer)

clinic_site.register(CustomerScheduleList, CustomerScheduleListAdmin)
admin.site.register(CustomerScheduleList, CustomerScheduleListAdmin)


class CustomerScheduleDraftAdmin(admin.ModelAdmin):
    autocomplete_fields = ["scheduled_operator", ]
clinic_site.register(CustomerScheduleDraft, CustomerScheduleDraftAdmin)
admin.site.register(CustomerScheduleDraft, CustomerScheduleDraftAdmin)

from django.forms import ModelForm
class CustomCustomerScheduleDraftForm(ModelForm):
    class Meta:
        model = CustomerScheduleDraft
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 如果这个表单的实例已经有一个选择的service
        if self.instance and self.instance.service:
            from core.models import Staff
            # 获取所有该service关联的roles
            roles = self.instance.service.role.all()
            # 过滤选择Staff.role在roles里的员工
            self.fields['scheduled_operator'].queryset = Staff.objects.filter(role__in=roles).distinct()

class CustomerScheduleDraftInline(admin.TabularInline):
    model = CustomerScheduleDraft
    form = CustomCustomerScheduleDraftForm
    extra = 0
    can_delete = False
    # verbose_name_plural = '服务项目安排'
    exclude = ["hssc_id", "label", "name", ]
    # autocomplete_fields = ["scheduled_operator", ]

    def get_queryset(self, request):
        # 重写get_queryset方法，设置缺省overtime为服务的overtime
        qs = super().get_queryset(request)
        for item in qs:
            item.overtime = item.service.overtime
            item.save()
        return qs

class CustomerSchedulePackageAdmin(HsscFormAdmin):
    exclude = ["hssc_id", "label", "name", "operator", "creater", "pid", "cpid", "slug", "created_time", "updated_time", "pym"]
    fieldsets = ((None, {'fields': (('customer', 'servicepackage'), 'start_time' )}),)
    readonly_fields = ['customer', 'servicepackage']
    inlines = [CustomerScheduleDraftInline, ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        request._saved_obj = obj                

    def save_formset(self, request, form, formset, change):
        # Retrieve obj from the request
        schedule_package = getattr(request, '_saved_obj', None)
        formset.save()
        instances = formset.queryset

        if instances:
            schedules = get_services_schedule(instances, schedule_package.start_time)
            
            # 生成CustomerScheduleList记录
            schedule_list = CustomerScheduleList.objects.create(
                customer = schedule_package.customer,
                operator = schedule_package.operator,
                creater = schedule_package.creater,
                plan_serial_number = schedule_package.servicepackage.label + '--' + schedule_package.created_time.strftime('%Y-%m-%d') + '--' + schedule_package.operator.name,
                schedule_package = schedule_package,
                is_ready = False
            )

            # 创建客户服务日程
            for schedule in schedules:
                CustomerSchedule.objects.create(
                    customer_schedule_list = schedule_list,
                    customer=schedule_package.customer,
                    operator=schedule_package.operator,
                    creater=schedule_package.creater,
                    schedule_package=schedule_package,
                    service=schedule['service'],
                    scheduled_time=schedule['scheduled_time'],
                    scheduled_operator=schedule['scheduled_operator'],
                    priority_operator=schedule['priority_operator'],
                    overtime=schedule['overtime'],
                    pid=schedule_package.pid
                )

            # 更新服务进程entry为'customerschedulelist/id/change/'
            schedule_list.schedule_package.pid.entry = f'/clinic/service/customerschedulelist/{schedule_list.id}/change'
            schedule_list.schedule_package.pid.save()

            schedule_list.is_ready = True  # 完成一次创建服务包计划安排事务
            schedule_list.save()

            # 把服务进程状态修改为已完成
            proc = schedule_package.pid
            if proc:
                proc.update_state('RTC')
            
clinic_site.register(CustomerSchedulePackage, CustomerSchedulePackageAdmin)
admin.site.register(CustomerSchedulePackage, CustomerSchedulePackageAdmin)

# **********************************************************************************************************************
# Service表单Admin
# **********************************************************************************************************************

class Shuang_xiang_zhuan_zhen_zhuan_chuAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("双向转诊表转出", {"fields": ("boolfield_zhuan_zhen_ji_gou_ming_cheng", "boolfield_zhuan_zhen_shuo_ming", "boolfield_chu_bu_yin_xiang", "boolfield_zhu_yao_xian_bing_shi", "boolfield_zhu_yao_ji_wang_shi", "boolfield_zhuan_zhen_yi_sheng_qian_zi", "boolfield_ji_gou_ming_cheng", "boolfield_lian_xi_dian_hua", "boolfield_zhuan_zhen_ri_qi", )}), ]
    autocomplete_fields = ["boolfield_zhu_yao_xian_bing_shi", "boolfield_zhu_yao_ji_wang_shi", ]

admin.site.register(Shuang_xiang_zhuan_zhen_zhuan_chu, Shuang_xiang_zhuan_zhen_zhuan_chuAdmin)
clinic_site.register(Shuang_xiang_zhuan_zhen_zhuan_chu, Shuang_xiang_zhuan_zhen_zhuan_chuAdmin)

class Hui_zhen_zhen_duan_fu_wu_listInline(admin.TabularInline):
    model = Hui_zhen_zhen_duan_fu_wu_list
    extra = 1
    autocomplete_fields = ["boolfield_hui_zhen_jian_yi", "boolfield_hui_zhen_ze_ren_ren", ]

    def get_formset(self, request, obj=None, **kwargs):
        # 获取数据库记录数
        record_count = self.model.objects.filter(hui_zhen_zhen_duan_fu_wu=obj).count() if obj else 0
        # 根据记录数设置extra的值
        self.extra = 1 if record_count == 0 else 0
        
        from service.forms import Hui_zhen_zhen_duan_fu_wu_listForm
        FormWithUser = type(
            "FormWithUser",
            (Hui_zhen_zhen_duan_fu_wu_listForm,),
            {"__init__": lambda self, *args, **kwargs: Hui_zhen_zhen_duan_fu_wu_listForm.__init__(self, user=request.user, *args, **kwargs)}
        )
        kwargs["form"] = FormWithUser
            
        return super().get_formset(request, obj, **kwargs)

class Hui_zhen_zhen_duan_fu_wuAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("会诊诊断表", {"fields": ("boolfield_zheng_zhuang", "boolfield_hui_zhen_zhen_duan_jie_guo", )}), ]
    autocomplete_fields = ["boolfield_zheng_zhuang", "boolfield_hui_zhen_zhen_duan_jie_guo", ]
    inlines = [Hui_zhen_zhen_duan_fu_wu_listInline, ]

admin.site.register(Hui_zhen_zhen_duan_fu_wu, Hui_zhen_zhen_duan_fu_wuAdmin)
clinic_site.register(Hui_zhen_zhen_duan_fu_wu, Hui_zhen_zhen_duan_fu_wuAdmin)

class Hui_zhen_jian_yi_fu_wu_listInline(admin.TabularInline):
    model = Hui_zhen_jian_yi_fu_wu_list
    extra = 1
    autocomplete_fields = ["boolfield_hui_zhen_jian_yi", ]

    def get_formset(self, request, obj=None, **kwargs):
        # 获取数据库记录数
        record_count = self.model.objects.filter(hui_zhen_jian_yi_fu_wu=obj).count() if obj else 0
        # 根据记录数设置extra的值
        self.extra = 1 if record_count == 0 else 0
        
        return super().get_formset(request, obj, **kwargs)

class Hui_zhen_jian_yi_fu_wuAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("会诊建议表", {"fields": ("boolfield_zheng_zhuang", "boolfield_hui_zhen_ze_ren_ren", )}), ]
    autocomplete_fields = ["boolfield_zheng_zhuang", "boolfield_hui_zhen_ze_ren_ren", ]

    def get_form(self, request, obj=None, **kwargs):
        from service.forms import Hui_zhen_jian_yi_fu_wuForm
        FormWithUser = type(
            "FormWithUser",
            (Hui_zhen_jian_yi_fu_wuForm,),
            {"__init__": lambda self, *args, **kwargs: Hui_zhen_jian_yi_fu_wuForm.__init__(self, user=request.user, *args, **kwargs)}
        )
        kwargs["form"] = FormWithUser
        return super().get_form(request, obj, **kwargs)
            
    inlines = [Hui_zhen_jian_yi_fu_wu_listInline, ]

admin.site.register(Hui_zhen_jian_yi_fu_wu, Hui_zhen_jian_yi_fu_wuAdmin)
clinic_site.register(Hui_zhen_jian_yi_fu_wu, Hui_zhen_jian_yi_fu_wuAdmin)

class Hui_zhen_shen_qing_fu_wuAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("会诊申请表", {"fields": ("boolfield_zheng_zhuang", "boolfield_hui_zhen_ren", )}), ]
    autocomplete_fields = ["boolfield_zheng_zhuang", "boolfield_hui_zhen_ren", ]

admin.site.register(Hui_zhen_shen_qing_fu_wu, Hui_zhen_shen_qing_fu_wuAdmin)
clinic_site.register(Hui_zhen_shen_qing_fu_wu, Hui_zhen_shen_qing_fu_wuAdmin)

class Yong_yao_hui_fang_fu_wuAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), ]

admin.site.register(Yong_yao_hui_fang_fu_wu, Yong_yao_hui_fang_fu_wuAdmin)
clinic_site.register(Yong_yao_hui_fang_fu_wu, Yong_yao_hui_fang_fu_wuAdmin)

class Tang_niao_bing_jian_kang_jiao_yu_fu_wuAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("糖尿病健康教育处方", {"fields": ("boolfield_jian_kang_jiao_yu_chu_fang", )}), ]

admin.site.register(Tang_niao_bing_jian_kang_jiao_yu_fu_wu, Tang_niao_bing_jian_kang_jiao_yu_fu_wuAdmin)
clinic_site.register(Tang_niao_bing_jian_kang_jiao_yu_fu_wu, Tang_niao_bing_jian_kang_jiao_yu_fu_wuAdmin)

class Yi_xing_tang_niao_bing_zhen_duanAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("胰岛素依赖性糖尿病诊断表", {"fields": ("boolfield_ji_bing_ming_cheng", "boolfield_shi_fou_hui_zhen", "boolfield_shi_fou_zhuan_zhen", )}), ]
    autocomplete_fields = ["boolfield_ji_bing_ming_cheng", ]
    radio_fields = {"boolfield_shi_fou_hui_zhen": admin.VERTICAL, "boolfield_shi_fou_zhuan_zhen": admin.VERTICAL, }
    change_form_template = "yi_xing_tang_niao_bing_zhen_duan_change_form.html"

admin.site.register(Yi_xing_tang_niao_bing_zhen_duan, Yi_xing_tang_niao_bing_zhen_duanAdmin)
clinic_site.register(Yi_xing_tang_niao_bing_zhen_duan, Yi_xing_tang_niao_bing_zhen_duanAdmin)

class Zhu_she_fu_wu_listInline(admin.TabularInline):
    model = Zhu_she_fu_wu_list
    extra = 1
    autocomplete_fields = ["boolfield_yao_pin_ming", ]

    def get_formset(self, request, obj=None, **kwargs):
        # 获取数据库记录数
        record_count = self.model.objects.filter(zhu_she_fu_wu=obj).count() if obj else 0
        # 根据记录数设置extra的值
        self.extra = 1 if record_count == 0 else 0
        
        return super().get_formset(request, obj, **kwargs)

class Zhu_she_fu_wuAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("输液注射单", {"fields": ("boolfield_zhi_xing_qian_ming", "boolfield_yong_yao_liao_cheng", "boolfield_zhu_she_ri_qi", )}), ]
    inlines = [Zhu_she_fu_wu_listInline, ]

admin.site.register(Zhu_she_fu_wu, Zhu_she_fu_wuAdmin)
clinic_site.register(Zhu_she_fu_wu, Zhu_she_fu_wuAdmin)

class Yun_dong_chu_fangAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("运动处方", {"fields": ("boolfield_ji_bing_ming_cheng", "boolfield_yun_dong_gan_yu", )}), ]
    autocomplete_fields = ["boolfield_ji_bing_ming_cheng", "boolfield_yun_dong_gan_yu", ]

admin.site.register(Yun_dong_chu_fang, Yun_dong_chu_fangAdmin)
clinic_site.register(Yun_dong_chu_fang, Yun_dong_chu_fangAdmin)

class Ying_yang_chu_fangAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("营养处方", {"fields": ("boolfield_ji_bing_ming_cheng", "boolfield_ying_yang_gan_yu", )}), ]
    autocomplete_fields = ["boolfield_ji_bing_ming_cheng", "boolfield_ying_yang_gan_yu", ]

admin.site.register(Ying_yang_chu_fang, Ying_yang_chu_fangAdmin)
clinic_site.register(Ying_yang_chu_fang, Ying_yang_chu_fangAdmin)

class Yuan_wai_jian_ce_can_hou_2_xiao_shi_xue_tangAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("餐后2小时血糖", {"fields": ("boolfield_can_hou_2_xiao_shi_xue_tang", )}), ]

admin.site.register(Yuan_wai_jian_ce_can_hou_2_xiao_shi_xue_tang, Yuan_wai_jian_ce_can_hou_2_xiao_shi_xue_tangAdmin)
clinic_site.register(Yuan_wai_jian_ce_can_hou_2_xiao_shi_xue_tang, Yuan_wai_jian_ce_can_hou_2_xiao_shi_xue_tangAdmin)

class Yuan_wai_jian_ce_kong_fu_xue_tangAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("空腹血糖检查", {"fields": ("boolfield_kong_fu_xue_tang", )}), ]

admin.site.register(Yuan_wai_jian_ce_kong_fu_xue_tang, Yuan_wai_jian_ce_kong_fu_xue_tangAdmin)
clinic_site.register(Yuan_wai_jian_ce_kong_fu_xue_tang, Yuan_wai_jian_ce_kong_fu_xue_tangAdmin)

class Man_yi_du_diao_chaAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("满意度调查表", {"fields": ("boolfield_yi_liao_fu_wu_ji_neng_xiang_mu_ping_fen", "boolfield_ping_tai_fu_wu_xiang_mu_ping_fen", "boolfield_fu_wu_liu_cheng_ping_fen", "boolfield_fu_wu_xiao_lv_ping_fen", "boolfield_xi_wang_zeng_jia_de_fu_wu_xiang_mu", "boolfield_you_dai_gai_jin_de_fu_wu", )}), 
        ("满意度调查表", {"fields": ("boolfield_yi_liao_fu_wu_ji_neng_xiang_mu_ping_fen", "boolfield_ping_tai_fu_wu_xiang_mu_ping_fen", "boolfield_fu_wu_liu_cheng_ping_fen", "boolfield_fu_wu_xiao_lv_ping_fen", "boolfield_xi_wang_zeng_jia_de_fu_wu_xiang_mu", "boolfield_you_dai_gai_jin_de_fu_wu", )}), ]
    radio_fields = {"boolfield_yi_liao_fu_wu_ji_neng_xiang_mu_ping_fen": admin.VERTICAL, "boolfield_ping_tai_fu_wu_xiang_mu_ping_fen": admin.VERTICAL, "boolfield_fu_wu_liu_cheng_ping_fen": admin.VERTICAL, "boolfield_fu_wu_xiao_lv_ping_fen": admin.VERTICAL, "boolfield_yi_liao_fu_wu_ji_neng_xiang_mu_ping_fen": admin.VERTICAL, "boolfield_ping_tai_fu_wu_xiang_mu_ping_fen": admin.VERTICAL, "boolfield_fu_wu_liu_cheng_ping_fen": admin.VERTICAL, "boolfield_fu_wu_xiao_lv_ping_fen": admin.VERTICAL, }

admin.site.register(Man_yi_du_diao_cha, Man_yi_du_diao_chaAdmin)
clinic_site.register(Man_yi_du_diao_cha, Man_yi_du_diao_chaAdmin)

class Zhen_hou_sui_fangAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("诊后回访单", {"fields": ("boolfield_zhi_liao_gan_shou_he_xiao_guo_ping_jia", "boolfield_deng_hou_qing_kuang", "boolfield_cun_zai_de_wen_ti", "boolfield_you_dai_gai_jin_de_fu_wu", "boolfield_nin_de_dan_xin_he_gu_lv", "boolfield_nin_hai_xu_yao_de_fu_wu", "boolfield_nin_cong_he_chu_zhi_dao_wo_men_de_fu_wu", "boolfield_nin_shi_fou_yuan_yi_xiang_ta_ren_tui_jian_wo_men", )}), 
        ("诊后回访单", {"fields": ("boolfield_zhi_liao_gan_shou_he_xiao_guo_ping_jia", "boolfield_deng_hou_qing_kuang", "boolfield_cun_zai_de_wen_ti", "boolfield_you_dai_gai_jin_de_fu_wu", "boolfield_nin_de_dan_xin_he_gu_lv", "boolfield_nin_hai_xu_yao_de_fu_wu", "boolfield_nin_cong_he_chu_zhi_dao_wo_men_de_fu_wu", "boolfield_nin_shi_fou_yuan_yi_xiang_ta_ren_tui_jian_wo_men", )}), ]
    radio_fields = {"boolfield_zhi_liao_gan_shou_he_xiao_guo_ping_jia": admin.VERTICAL, "boolfield_deng_hou_qing_kuang": admin.VERTICAL, "boolfield_nin_cong_he_chu_zhi_dao_wo_men_de_fu_wu": admin.VERTICAL, "boolfield_nin_shi_fou_yuan_yi_xiang_ta_ren_tui_jian_wo_men": admin.VERTICAL, "boolfield_zhi_liao_gan_shou_he_xiao_guo_ping_jia": admin.VERTICAL, "boolfield_deng_hou_qing_kuang": admin.VERTICAL, "boolfield_nin_cong_he_chu_zhi_dao_wo_men_de_fu_wu": admin.VERTICAL, "boolfield_nin_shi_fou_yuan_yi_xiang_ta_ren_tui_jian_wo_men": admin.VERTICAL, }

admin.site.register(Zhen_hou_sui_fang, Zhen_hou_sui_fangAdmin)
clinic_site.register(Zhen_hou_sui_fang, Zhen_hou_sui_fangAdmin)

class Xue_ya_jian_ce_ping_guAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("血压监测评估", {"fields": ("boolfield_xue_ya_jian_ce_ping_gu", )}), ]

admin.site.register(Xue_ya_jian_ce_ping_gu, Xue_ya_jian_ce_ping_guAdmin)
clinic_site.register(Xue_ya_jian_ce_ping_gu, Xue_ya_jian_ce_ping_guAdmin)

class Can_hou_2_xiao_shi_xue_tangAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("餐后2小时血糖", {"fields": ("boolfield_can_hou_2_xiao_shi_xue_tang", )}), ]

admin.site.register(Can_hou_2_xiao_shi_xue_tang, Can_hou_2_xiao_shi_xue_tangAdmin)
clinic_site.register(Can_hou_2_xiao_shi_xue_tang, Can_hou_2_xiao_shi_xue_tangAdmin)

class Ji_gou_ji_ben_xin_xi_biaoAdmin(HsscFormAdmin):
    fieldssets = [
        ("机构基本信息表", {"fields": ("boolfield_lian_xi_di_zhi", "boolfield_ji_gou_bian_ma", "boolfield_ji_gou_ming_cheng", "boolfield_ji_gou_dai_ma", "boolfield_ji_gou_shu_xing", "boolfield_ji_gou_ceng_ji", "boolfield_suo_zai_hang_zheng_qu_hua_dai_ma", "boolfield_xing_zheng_qu_hua_gui_shu", "boolfield_fa_ding_fu_ze_ren", "boolfield_lian_xi_dian_hua", )}), ]
    search_fields = ["name", "pym", ]

admin.site.register(Ji_gou_ji_ben_xin_xi_biao, Ji_gou_ji_ben_xin_xi_biaoAdmin)
clinic_site.register(Ji_gou_ji_ben_xin_xi_biao, Ji_gou_ji_ben_xin_xi_biaoAdmin)

class Zhi_yuan_ji_ben_xin_xi_biaoAdmin(HsscFormAdmin):
    fieldssets = [
        ("职员基本信息表", {"fields": ("boolfield_shen_fen_zheng_hao_ma", "boolfield_zhi_ye_zi_zhi", "boolfield_zhuan_chang", "boolfield_zhi_ye_shi_jian", "boolfield_zhi_yuan_bian_ma", "boolfield_lian_xi_dian_hua", "boolfield_xing_ming", "boolfield_suo_shu_ji_gou", "boolfield_fu_wu_jue_se", )}), ]
    autocomplete_fields = ["boolfield_suo_shu_ji_gou", ]
    search_fields = ["name", "pym", ]

admin.site.register(Zhi_yuan_ji_ben_xin_xi_biao, Zhi_yuan_ji_ben_xin_xi_biaoAdmin)
clinic_site.register(Zhi_yuan_ji_ben_xin_xi_biao, Zhi_yuan_ji_ben_xin_xi_biaoAdmin)

class Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_chaAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("服务分供机构基本信息表", {"fields": ("boolfield_lian_xi_di_zhi", "boolfield_ji_gou_dai_ma", "boolfield_ji_gou_shu_xing", "boolfield_gong_ying_shang_bian_ma", "boolfield_zhuan_ye_fu_wu", "boolfield_gong_ying_shang_ming_cheng", "boolfield_lian_xi_dian_hua", "boolfield_xin_yu_ping_ji", )}), ]

admin.site.register(Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_cha, Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_chaAdmin)
clinic_site.register(Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_cha, Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_chaAdmin)

class She_bei_ji_ben_xin_xi_ji_luAdmin(HsscFormAdmin):
    fieldssets = [
        ("设备基本信息表", {"fields": ("boolfield_she_bei_bian_ma", "boolfield_sheng_chan_chang_jia", "boolfield_she_bei_fu_wu_dan_wei_hao_shi", "boolfield_she_bei_jian_xiu_zhou_qi", "boolfield_she_bei_shi_yong_cheng_ben", "boolfield_she_bei_ming_cheng", "boolfield_lian_xi_dian_hua", "boolfield_she_bei_shi_yong_fu_wu_gong_neng", )}), ]
    autocomplete_fields = ["boolfield_she_bei_shi_yong_fu_wu_gong_neng", ]
    search_fields = ["name", "pym", ]

admin.site.register(She_bei_ji_ben_xin_xi_ji_lu, She_bei_ji_ben_xin_xi_ji_luAdmin)
clinic_site.register(She_bei_ji_ben_xin_xi_ji_lu, She_bei_ji_ben_xin_xi_ji_luAdmin)

class Gong_ying_shang_ji_ben_xin_xi_diao_chaAdmin(HsscFormAdmin):
    fieldssets = [
        ("物料供应商基本信息表", {"fields": ("boolfield_lian_xi_di_zhi", "boolfield_gong_ying_shang_bian_ma", "boolfield_zhu_yao_gong_ying_chan_pin", "boolfield_gong_huo_zhou_qi", "boolfield_gong_ying_shang_ming_cheng", "boolfield_lian_xi_dian_hua", "boolfield_xin_yu_ping_ji", )}), ]
    search_fields = ["name", "pym", ]

admin.site.register(Gong_ying_shang_ji_ben_xin_xi_diao_cha, Gong_ying_shang_ji_ben_xin_xi_diao_chaAdmin)
clinic_site.register(Gong_ying_shang_ji_ben_xin_xi_diao_cha, Gong_ying_shang_ji_ben_xin_xi_diao_chaAdmin)

class Yao_pin_ji_ben_xin_xi_biaoAdmin(HsscFormAdmin):
    fieldssets = [
        ("药品基本信息表", {"fields": ("boolfield_yao_pin_bian_ma", "boolfield_pin_yin_ma", "boolfield_yao_pin_ming_cheng", "boolfield_gui_ge", "boolfield_chu_fang_ji_liang_dan_wei", "boolfield_chang_yong_ji_liang", "boolfield_yong_yao_tu_jing", "boolfield_yong_yao_pin_ci", "boolfield_yong_yao_bei_zhu", "boolfield_yao_ji_lei_xing", "boolfield_yao_pin_fen_lei", "boolfield_yao_pin_guan_li_shu_xing", "boolfield_yao_pin_tong_yong_ming_cheng", "boolfield_guo_jia_ji_ben_yao_pin_mu_lu_ming_cheng", "boolfield_yi_bao_yao_pin_mu_lu_dui_ying_yao_pin_bian_ma", "boolfield_yi_bao_bao_xiao_lei_bie", "boolfield_shi_ying_zheng", "boolfield_bu_shi_ying_zheng", "boolfield_bu_liang_fan_ying", )}), ]
    autocomplete_fields = ["boolfield_shi_ying_zheng", "boolfield_bu_shi_ying_zheng", ]
    radio_fields = {"boolfield_yi_bao_bao_xiao_lei_bie": admin.VERTICAL, }
    search_fields = ["name", "pym", ]

admin.site.register(Yao_pin_ji_ben_xin_xi_biao, Yao_pin_ji_ben_xin_xi_biaoAdmin)
clinic_site.register(Yao_pin_ji_ben_xin_xi_biao, Yao_pin_ji_ben_xin_xi_biaoAdmin)

class Shen_qing_kong_fu_xue_tang_jian_cha_fu_wuAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("申请服务表", {"fields": ("boolfield_dang_qian_pai_dui_ren_shu", "boolfield_yu_ji_deng_hou_shi_jian", "boolfield_fu_wu_xiang_mu_ming_cheng", "boolfield_an_pai_que_ren", )}), ]
    autocomplete_fields = ["boolfield_fu_wu_xiang_mu_ming_cheng", ]

admin.site.register(Shen_qing_kong_fu_xue_tang_jian_cha_fu_wu, Shen_qing_kong_fu_xue_tang_jian_cha_fu_wuAdmin)
clinic_site.register(Shen_qing_kong_fu_xue_tang_jian_cha_fu_wu, Shen_qing_kong_fu_xue_tang_jian_cha_fu_wuAdmin)

class Ju_min_ji_ben_xin_xi_diao_chaAdmin(HsscFormAdmin):
    fieldssets = [
        ("个人基本信息", {"fields": ("boolfield_xing_ming", "boolfield_chu_sheng_ri_qi", "boolfield_xing_bie", "boolfield_jia_ting_di_zhi", "boolfield_lian_xi_dian_hua", "boolfield_shen_fen_zheng_hao_ma", "boolfield_ju_min_dang_an_hao", "boolfield_yi_liao_ic_ka_hao", "boolfield_min_zu", "boolfield_hun_yin_zhuang_kuang", "boolfield_wen_hua_cheng_du", "boolfield_zhi_ye_zhuang_kuang", "boolfield_yi_liao_fei_yong_fu_dan", "boolfield_ju_zhu_lei_xing", "boolfield_xue_xing", "boolfield_qian_yue_jia_ting_yi_sheng", "boolfield_jia_ting_cheng_yuan_guan_xi", )}), ]
    autocomplete_fields = ["boolfield_qian_yue_jia_ting_yi_sheng", ]
    search_fields = ["name", "pym", ]

admin.site.register(Ju_min_ji_ben_xin_xi_diao_cha, Ju_min_ji_ben_xin_xi_diao_chaAdmin)
clinic_site.register(Ju_min_ji_ben_xin_xi_diao_cha, Ju_min_ji_ben_xin_xi_diao_chaAdmin)

class Shu_ye_zhu_she_listInline(admin.TabularInline):
    model = Shu_ye_zhu_she_list
    extra = 1
    autocomplete_fields = ["boolfield_yao_pin_ming", ]

    def get_formset(self, request, obj=None, **kwargs):
        # 获取数据库记录数
        record_count = self.model.objects.filter(shu_ye_zhu_she=obj).count() if obj else 0
        # 根据记录数设置extra的值
        self.extra = 1 if record_count == 0 else 0
        
        return super().get_formset(request, obj, **kwargs)

class Shu_ye_zhu_sheAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("输液注射单", {"fields": ("boolfield_zhi_xing_qian_ming", "boolfield_yong_yao_liao_cheng", "boolfield_zhu_she_ri_qi", )}), 
        ("上门服务", {"fields": ("boolfield_shang_men_fu_wu_xiang_mu", "boolfield_jia_ting_di_zhi", "boolfield_shang_men_fu_wu_shi_jian", )}), ]
    autocomplete_fields = ["boolfield_shang_men_fu_wu_xiang_mu", ]
    inlines = [Shu_ye_zhu_she_listInline, ]

admin.site.register(Shu_ye_zhu_she, Shu_ye_zhu_sheAdmin)
clinic_site.register(Shu_ye_zhu_she, Shu_ye_zhu_sheAdmin)

class Qian_yue_fu_wuAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("家庭医生签约", {"fields": ("boolfield_jia_ting_qian_yue_fu_wu_xie_yi", "boolfield_qian_yue_que_ren", )}), ]

admin.site.register(Qian_yue_fu_wu, Qian_yue_fu_wuAdmin)
clinic_site.register(Qian_yue_fu_wu, Qian_yue_fu_wuAdmin)

class T9001Admin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("非胰岛素依赖性糖尿病诊断表", {"fields": ("boolfield_ji_bing_ming_cheng", "boolfield_shi_fou_hui_zhen", "boolfield_shi_fou_zhuan_zhen", )}), ]
    autocomplete_fields = ["boolfield_ji_bing_ming_cheng", ]
    radio_fields = {"boolfield_shi_fou_hui_zhen": admin.VERTICAL, "boolfield_shi_fou_zhuan_zhen": admin.VERTICAL, }
    change_form_template = "t9001_change_form.html"

admin.site.register(T9001, T9001Admin)
clinic_site.register(T9001, T9001Admin)

class Tang_hua_xue_hong_dan_bai_jian_cha_biaoAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("糖化血红蛋白检查", {"fields": ("boolfield_tang_hua_xue_hong_dan_bai", )}), ]

admin.site.register(Tang_hua_xue_hong_dan_bai_jian_cha_biao, Tang_hua_xue_hong_dan_bai_jian_cha_biaoAdmin)
clinic_site.register(Tang_hua_xue_hong_dan_bai_jian_cha_biao, Tang_hua_xue_hong_dan_bai_jian_cha_biaoAdmin)

class Kong_fu_xue_tang_jian_chaAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("空腹血糖检查", {"fields": ("boolfield_kong_fu_xue_tang", )}), ]

admin.site.register(Kong_fu_xue_tang_jian_cha, Kong_fu_xue_tang_jian_chaAdmin)
clinic_site.register(Kong_fu_xue_tang_jian_cha, Kong_fu_xue_tang_jian_chaAdmin)

class Xue_ya_jian_ceAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("血压监测", {"fields": ("boolfield_shou_suo_ya", "boolfield_shu_zhang_ya", )}), ]

admin.site.register(Xue_ya_jian_ce, Xue_ya_jian_ceAdmin)
clinic_site.register(Xue_ya_jian_ce, Xue_ya_jian_ceAdmin)

class Tang_niao_bing_cha_tiAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("眼底检查", {"fields": ("boolfield_yan_di", )}), 
        ("足背动脉检查", {"fields": ("boolfield_zuo_jiao", "boolfield_you_jiao", )}), ]
    radio_fields = {"boolfield_zuo_jiao": admin.VERTICAL, "boolfield_you_jiao": admin.VERTICAL, }

admin.site.register(Tang_niao_bing_cha_ti, Tang_niao_bing_cha_tiAdmin)
clinic_site.register(Tang_niao_bing_cha_ti, Tang_niao_bing_cha_tiAdmin)

class A3502Admin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("尿常规检查", {"fields": ("boolfield_niao_tang", "boolfield_dan_bai_zhi", "boolfield_niao_tong_ti", )}), ]

admin.site.register(A3502, A3502Admin)
clinic_site.register(A3502, A3502Admin)

class A6299Admin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("遗传病史", {"fields": ("boolfield_yi_chuan_xing_ji_bing", "boolfield_yi_chuan_bing_shi_cheng_yuan", )}), 
        ("过敏史", {"fields": ("boolfield_guo_min_yao_wu", )}), 
        ("家族病史", {"fields": ("boolfield_jia_zu_xing_ji_bing", "boolfield_jia_zu_bing_shi_cheng_yuan", )}), 
        ("手术史", {"fields": ("boolfield_shou_shu_ming_cheng", "boolfield_shou_shu_ri_qi", )}), 
        ("疾病史", {"fields": ("boolfield_ge_ren_bing_shi", "boolfield_que_zhen_shi_jian", )}), 
        ("外伤史", {"fields": ("boolfield_wai_shang_xing_ji_bing", "boolfield_wai_shang_ri_qi", )}), 
        ("输血史", {"fields": ("boolfield_shu_xue_liang", "boolfield_shu_xue_ri_qi", )}), 
        ("个人心理综合素质调查", {"fields": ("boolfield_xing_ge_qing_xiang", "boolfield_shi_mian_qing_kuang", "boolfield_sheng_huo_gong_zuo_ya_li_qing_kuang", )}), 
        ("个人适应能力评估", {"fields": ("boolfield_mei_tian_gong_zuo_ji_gong_zuo_wang_fan_zong_shi_chang", "boolfield_dui_mu_qian_sheng_huo_he_gong_zuo_man_yi_ma", "boolfield_dui_zi_ji_de_shi_ying_neng_li_man_yi_ma", )}), 
        ("个人身体健康评估", {"fields": ("boolfield_jue_de_zi_shen_jian_kang_zhuang_kuang_ru_he", "boolfield_jiao_zhi_guo_qu_yi_nian_zhuang_tai_ru_he", "boolfield_yun_dong_pian_hao", "boolfield_yun_dong_shi_chang", "boolfield_jin_lai_you_wu_shen_ti_bu_shi_zheng_zhuang", )}), 
        ("个人健康行为调查", {"fields": ("boolfield_ping_jun_shui_mian_shi_chang", "boolfield_chi_xu_shi_mian_shi_jian", "boolfield_yin_jiu_pin_ci", "boolfield_xi_yan_pin_ci", )}), 
        ("社会环境评估", {"fields": ("boolfield_nin_dui_ju_zhu_huan_jing_man_yi_ma", "boolfield_nin_suo_zai_de_she_qu_jiao_tong_fang_bian_ma", )}), ]
    autocomplete_fields = ["boolfield_yi_chuan_xing_ji_bing", "boolfield_guo_min_yao_wu", "boolfield_jia_zu_xing_ji_bing", "boolfield_shou_shu_ming_cheng", "boolfield_ge_ren_bing_shi", "boolfield_wai_shang_xing_ji_bing", "boolfield_jin_lai_you_wu_shen_ti_bu_shi_zheng_zhuang", ]
    radio_fields = {"boolfield_xing_ge_qing_xiang": admin.VERTICAL, "boolfield_shi_mian_qing_kuang": admin.VERTICAL, "boolfield_sheng_huo_gong_zuo_ya_li_qing_kuang": admin.VERTICAL, "boolfield_jue_de_zi_shen_jian_kang_zhuang_kuang_ru_he": admin.VERTICAL, "boolfield_yun_dong_shi_chang": admin.VERTICAL, "boolfield_yin_jiu_pin_ci": admin.VERTICAL, "boolfield_xi_yan_pin_ci": admin.VERTICAL, }

admin.site.register(A6299, A6299Admin)
clinic_site.register(A6299, A6299Admin)

class A6220Admin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("糖尿病监测评估", {"fields": ("boolfield_kong_fu_xue_tang_ping_jun_zhi", "boolfield_can_hou_2_xiao_shi_xue_tang_ping_jun_zhi", "boolfield_tang_niao_bing_kong_zhi_xiao_guo_ping_gu", "boolfield_xue_ya_jian_ce_ping_gu", )}), ]
    radio_fields = {"boolfield_tang_niao_bing_kong_zhi_xiao_guo_ping_gu": admin.VERTICAL, }

admin.site.register(A6220, A6220Admin)
clinic_site.register(A6220, A6220Admin)

class A6202Admin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("院外辅助问诊", {"fields": ("boolfield_bing_qing_bu_chong_miao_shu", "boolfield_zheng_zhuang", )}), ]
    autocomplete_fields = ["boolfield_zheng_zhuang", ]

admin.site.register(A6202, A6202Admin)
clinic_site.register(A6202, A6202Admin)

class T6301Admin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("糖尿病一般随访", {"fields": ("boolfield_yong_yao_pin_ci", "boolfield_yin_jiu_pin_ci", "boolfield_xi_yan_pin_ci", "boolfield_tang_niao_bing_zheng_zhuang", "boolfield_yao_pin_ming", )}), 
        ("足背动脉检查", {"fields": ("boolfield_zuo_jiao", "boolfield_you_jiao", )}), 
        ("眼底检查", {"fields": ("boolfield_yan_di", )}), 
        ("血压监测", {"fields": ("boolfield_shou_suo_ya", "boolfield_shu_zhang_ya", )}), 
        ("空腹血糖检查", {"fields": ("boolfield_kong_fu_xue_tang", )}), ]
    autocomplete_fields = ["boolfield_yao_pin_ming", ]
    radio_fields = {"boolfield_yin_jiu_pin_ci": admin.VERTICAL, "boolfield_xi_yan_pin_ci": admin.VERTICAL, "boolfield_zuo_jiao": admin.VERTICAL, "boolfield_you_jiao": admin.VERTICAL, }

admin.site.register(T6301, T6301Admin)
clinic_site.register(T6301, T6301Admin)

class A6218Admin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("门诊医生问诊", {"fields": ("boolfield_bing_qing_bu_chong_miao_shu", "boolfield_zheng_zhuang", )}), ]
    autocomplete_fields = ["boolfield_zheng_zhuang", ]

admin.site.register(A6218, A6218Admin)
clinic_site.register(A6218, A6218Admin)

class A6201Admin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("院外咨询", {"fields": ("boolfield_bing_qing_bu_chong_miao_shu", "boolfield_zheng_zhuang", )}), ]
    autocomplete_fields = ["boolfield_zheng_zhuang", ]

admin.site.register(A6201, A6201Admin)
clinic_site.register(A6201, A6201Admin)

class A6217Admin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("院内辅助问诊", {"fields": ("boolfield_bing_qing_bu_chong_miao_shu", "boolfield_zheng_zhuang", )}), ]
    autocomplete_fields = ["boolfield_zheng_zhuang", ]

admin.site.register(A6217, A6217Admin)
clinic_site.register(A6217, A6217Admin)

class Yao_shi_fu_wuAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("药事服务", {"fields": ("boolfield_ji_bing_ming_cheng", "boolfield_shi_fou_ji_xu_shi_yong", "boolfield_yao_pin_ming", )}), ]
    autocomplete_fields = ["boolfield_ji_bing_ming_cheng", "boolfield_yao_pin_ming", ]
    radio_fields = {"boolfield_shi_fou_ji_xu_shi_yong": admin.VERTICAL, }

admin.site.register(Yao_shi_fu_wu, Yao_shi_fu_wuAdmin)
clinic_site.register(Yao_shi_fu_wu, Yao_shi_fu_wuAdmin)

class Tang_niao_bing_zhuan_yong_wen_zhenAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("糖尿病专用问诊", {"fields": ("boolfield_bing_qing_bu_chong_miao_shu", "boolfield_tang_niao_bing_zheng_zhuang", )}), ]

admin.site.register(Tang_niao_bing_zhuan_yong_wen_zhen, Tang_niao_bing_zhuan_yong_wen_zhenAdmin)
clinic_site.register(Tang_niao_bing_zhuan_yong_wen_zhen, Tang_niao_bing_zhuan_yong_wen_zhenAdmin)

class A3101Admin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("诊前检查表", {"fields": ("boolfield_ti_wen", "boolfield_mai_bo", "boolfield_hu_xi_pin_lv", "boolfield_shen_gao", "boolfield_ti_zhong", "boolfield_ti_zhi_zhi_shu", "boolfield_shou_suo_ya", "boolfield_shu_zhang_ya", "boolfield_yao_wei", "boolfield_yan_bu", "boolfield_xia_zhi_shui_zhong", "boolfield_zheng_zhuang", )}), ]
    autocomplete_fields = ["boolfield_zheng_zhuang", ]
    radio_fields = {"boolfield_xia_zhi_shui_zhong": admin.VERTICAL, }
    change_form_template = "a3101_change_form.html"

admin.site.register(A3101, A3101Admin)
clinic_site.register(A3101, A3101Admin)

class A6502Admin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("门诊分诊", {"fields": ("boolfield_qian_dao_que_ren", "boolfield_yu_yue_shi_jian", "boolfield_zheng_zhuang", )}), ]
    autocomplete_fields = ["boolfield_zheng_zhuang", ]
    radio_fields = {"boolfield_qian_dao_que_ren": admin.VERTICAL, }

admin.site.register(A6502, A6502Admin)
clinic_site.register(A6502, A6502Admin)

class A6501Admin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("代人预约挂号", {"fields": ("boolfield_yu_yue_shi_jian", "boolfield_ze_ren_ren", "boolfield_zheng_zhuang", )}), ]
    autocomplete_fields = ["boolfield_ze_ren_ren", "boolfield_zheng_zhuang", ]

admin.site.register(A6501, A6501Admin)
clinic_site.register(A6501, A6501Admin)

class Men_zhen_chu_fang_biao_listInline(admin.TabularInline):
    model = Men_zhen_chu_fang_biao_list
    extra = 1
    autocomplete_fields = ["boolfield_yao_pin_ming", ]

    def get_formset(self, request, obj=None, **kwargs):
        # 获取数据库记录数
        record_count = self.model.objects.filter(men_zhen_chu_fang_biao=obj).count() if obj else 0
        # 根据记录数设置extra的值
        self.extra = 1 if record_count == 0 else 0
        
        return super().get_formset(request, obj, **kwargs)

class Men_zhen_chu_fang_biaoAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("药物处方", {"fields": ("boolfield_ji_bing_ming_cheng", "boolfield_yong_yao_liao_cheng", )}), ]
    autocomplete_fields = ["boolfield_ji_bing_ming_cheng", ]
    change_form_template = "men_zhen_chu_fang_biao_change_form.html"
    inlines = [Men_zhen_chu_fang_biao_listInline, ]

admin.site.register(Men_zhen_chu_fang_biao, Men_zhen_chu_fang_biaoAdmin)
clinic_site.register(Men_zhen_chu_fang_biao, Men_zhen_chu_fang_biaoAdmin)
