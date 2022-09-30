from django.contrib import admin
from django.shortcuts import redirect
import nested_admin

from core.admin import clinic_site
from core.signals import operand_finished
from core.business_functions import create_customer_service_log
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

        # 把服务进程状态修改为已完成
        proc = obj.pid
        if proc:
            proc.update_state('RTC')

        import copy
        form_data1 = copy.copy(form.cleaned_data)
        form_data2 = copy.copy(form.cleaned_data)

        # 把表单内容存入CustomerServiceLog
        create_customer_service_log(form_data1, obj)

        # 发送服务作业完成信号
        print('发送操作完成信号, From service.admin.HsscFormAdmin.save_model：', obj.pid)
        operand_finished.send(sender=self, pid=obj.pid, request=request, form_data=form_data2)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def response_change(self, request, obj):
        # 按照service.route_to的配置跳转
        redirect_option = obj.pid.service.route_to
        if redirect_option == 'CUSTOMER_HOMEPAGE':
            return redirect(obj.customer)
        else:
            return redirect('index')


class CustomerScheduleAdmin(admin.ModelAdmin):
    autocomplete_fields = ["scheduled_operator", ]
    list_display = ['service', 'scheduled_time', 'scheduled_operator']
    list_editable = ['scheduled_time', 'scheduled_operator']
    ordering = ('scheduled_time',)
clinic_site.register(CustomerSchedule, CustomerScheduleAdmin)
admin.site.register(CustomerSchedule, CustomerScheduleAdmin)

class CustomerScheduleInline(nested_admin.NestedTabularInline):
    model = CustomerSchedule
    extra = 0
    can_delete = False
    # verbose_name_plural = '服务日程安排'
    exclude = ["hssc_id", "label", "name", ]
    autocomplete_fields = ["scheduled_operator", ]

class CustomerScheduleDraftAdmin(HsscFormAdmin):
    autocomplete_fields = ["scheduled_operator", ]
    inlines = [CustomerScheduleInline]
clinic_site.register(CustomerScheduleDraft, CustomerScheduleDraftAdmin)
admin.site.register(CustomerScheduleDraft, CustomerScheduleDraftAdmin)

class CustomerScheduleDraftInline(nested_admin.NestedTabularInline):
    model = CustomerScheduleDraft
    inlines = [CustomerScheduleInline]
    extra = 0
    can_delete = False
    # verbose_name_plural = '服务项目安排'
    exclude = ["hssc_id", "label", "name", ]
    autocomplete_fields = ["scheduled_operator", ]

class CustomerSchedulePackageAdmin(HsscFormAdmin):
    exclude = ["hssc_id", "label", "name", "operator", "creater", "pid", "cpid", "slug", "created_time", "updated_time", "pym"]
    fieldsets = ((None, {'fields': (('customer', 'servicepackage'), )}),)
    readonly_fields = ['customer', 'servicepackage']
    inlines = [CustomerScheduleDraftInline, ]

    def save_formset(self, request, form, formset, change):
        instances = formset.save()
        if instances:
            schedule_package = instances[0].schedule_package
            customer = schedule_package.customer
            from core.business_functions import get_services_schedule
            services_schedule = get_services_schedule(instances)
            print('services_schedule:', services_schedule)
            # 创建客户服务日程
            for service_schedule in services_schedule:
                CustomerSchedule.objects.create(
                    customer=customer,
                    schedule_package=schedule_package,
                    scheduled_draft=service_schedule['scheduled_draft'],
                    service=service_schedule['service'],
                    scheduled_time=service_schedule['scheduled_time'],
                    scheduled_operator=service_schedule['scheduled_operator'],
                )
            # 重定向到修改客户服务日程页面
            return redirect('/clinic/service/customerschedule/', pk=instances[0].pk)
            # return redirect('service:customer_schedule_edit', pk=instances[0].pk)

clinic_site.register(CustomerSchedulePackage, CustomerSchedulePackageAdmin)
admin.site.register(CustomerSchedulePackage, CustomerSchedulePackageAdmin)

# **********************************************************************************************************************
# Service表单Admin
# **********************************************************************************************************************

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
        ("药品基本信息表", {"fields": ("boolfield_yao_pin_tong_yong_ming", "boolfield_yao_pin_ming_cheng", "boolfield_yong_yao_pin_ci", "boolfield_yao_pin_bian_ma", "boolfield_yao_pin_gui_ge", "boolfield_chang_yong_chu_fang_liang", "boolfield_dui_zhao_yi_bao_ming_cheng", "boolfield_dui_zhao_ji_yao_ming_cheng", "boolfield_huan_suan_gui_ze", "boolfield_yong_yao_liao_cheng", "boolfield_chu_fang_ji_liang_dan_wei", "boolfield_ru_ku_ji_liang_dan_wei", "boolfield_xiao_shou_ji_liang_dan_wei", "boolfield_yong_yao_tu_jing", "boolfield_yao_pin_fen_lei", )}), ]
    search_fields = ["name", "pym", ]

admin.site.register(Yao_pin_ji_ben_xin_xi_biao, Yao_pin_ji_ben_xin_xi_biaoAdmin)
clinic_site.register(Yao_pin_ji_ben_xin_xi_biao, Yao_pin_ji_ben_xin_xi_biaoAdmin)

class Shen_qing_kong_fu_xue_tang_jian_cha_fu_wuAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("申请服务表", {"fields": ("boolfield_dang_qian_pai_dui_ren_shu", "boolfield_yu_ji_deng_hou_shi_jian", "boolfield_ze_ren_ren", "boolfield_fu_wu_xiang_mu_ming_cheng", "boolfield_an_pai_que_ren", )}), ]
    autocomplete_fields = ["boolfield_ze_ren_ren", "boolfield_fu_wu_xiang_mu_ming_cheng", ]

admin.site.register(Shen_qing_kong_fu_xue_tang_jian_cha_fu_wu, Shen_qing_kong_fu_xue_tang_jian_cha_fu_wuAdmin)
clinic_site.register(Shen_qing_kong_fu_xue_tang_jian_cha_fu_wu, Shen_qing_kong_fu_xue_tang_jian_cha_fu_wuAdmin)

class Ju_min_ji_ben_xin_xi_diao_chaAdmin(HsscFormAdmin):
    fieldssets = [
        ("个人基本信息", {"fields": ("boolfield_shen_fen_zheng_hao_ma", "boolfield_ju_min_dang_an_hao", "boolfield_jia_ting_di_zhi", "boolfield_yi_liao_ic_ka_hao", "boolfield_lian_xi_dian_hua", "boolfield_xing_ming", "boolfield_chu_sheng_ri_qi", "boolfield_xing_bie", "boolfield_min_zu", "boolfield_hun_yin_zhuang_kuang", "boolfield_wen_hua_cheng_du", "boolfield_zhi_ye_zhuang_kuang", "boolfield_yi_liao_fei_yong_fu_dan", "boolfield_ju_zhu_lei_xing", "boolfield_xue_xing", "boolfield_qian_yue_jia_ting_yi_sheng", "boolfield_jia_ting_cheng_yuan_guan_xi", )}), ]
    autocomplete_fields = ["boolfield_qian_yue_jia_ting_yi_sheng", ]
    search_fields = ["name", "pym", ]

admin.site.register(Ju_min_ji_ben_xin_xi_diao_cha, Ju_min_ji_ben_xin_xi_diao_chaAdmin)
clinic_site.register(Ju_min_ji_ben_xin_xi_diao_cha, Ju_min_ji_ben_xin_xi_diao_chaAdmin)

class Shu_ye_zhu_sheAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("输液注射单", {"fields": ("boolfield_yong_yao_pin_ci", "boolfield_yao_pin_gui_ge", "boolfield_chang_yong_chu_fang_liang", "boolfield_zhi_xing_qian_ming", "boolfield_yong_yao_liao_cheng", "boolfield_zhu_she_ri_qi", "boolfield_yao_pin_ming", )}), ]
    autocomplete_fields = ["boolfield_yao_pin_ming", ]

admin.site.register(Shu_ye_zhu_she, Shu_ye_zhu_sheAdmin)
clinic_site.register(Shu_ye_zhu_she, Shu_ye_zhu_sheAdmin)

class Qian_yue_fu_wuAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("家庭医生签约", {"fields": ("boolfield_jia_ting_qian_yue_fu_wu_xie_yi", "boolfield_qian_yue_que_ren", "boolfield_ze_ren_ren", )}), ]
    autocomplete_fields = ["boolfield_ze_ren_ren", ]

admin.site.register(Qian_yue_fu_wu, Qian_yue_fu_wuAdmin)
clinic_site.register(Qian_yue_fu_wu, Qian_yue_fu_wuAdmin)

class T9001Admin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("非胰岛素依赖性糖尿病", {"fields": ("boolfield_ji_bing_ming_cheng", "boolfield_ke_neng_zhen_duan", "boolfield_pai_chu_zhen_duan", )}), ]
    autocomplete_fields = ["boolfield_ji_bing_ming_cheng", "boolfield_ke_neng_zhen_duan", "boolfield_pai_chu_zhen_duan", ]

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
        ("过敏史", {"fields": ("boolfield_yao_pin_ming", )}), 
        ("家族病史", {"fields": ("boolfield_jia_zu_xing_ji_bing", "boolfield_jia_zu_bing_shi_cheng_yuan", )}), 
        ("手术史", {"fields": ("boolfield_shou_shu_ri_qi", "boolfield_shou_shu_ming_cheng", )}), 
        ("疾病史", {"fields": ("boolfield_que_zhen_shi_jian", "boolfield_ge_ren_bing_shi", )}), 
        ("外伤史", {"fields": ("boolfield_wai_shang_ri_qi", "boolfield_wai_shang_xing_ji_bing", )}), 
        ("输血史", {"fields": ("boolfield_shu_xue_liang", "boolfield_shu_xue_ri_qi", )}), 
        ("个人心理综合素质调查", {"fields": ("boolfield_xing_ge_qing_xiang", "boolfield_shi_mian_qing_kuang", "boolfield_sheng_huo_gong_zuo_ya_li_qing_kuang", )}), 
        ("个人适应能力评估", {"fields": ("boolfield_mei_tian_gong_zuo_ji_gong_zuo_wang_fan_zong_shi_chang", "boolfield_dui_mu_qian_sheng_huo_he_gong_zuo_man_yi_ma", "boolfield_dui_zi_ji_de_shi_ying_neng_li_man_yi_ma", )}), 
        ("个人身体健康评估", {"fields": ("boolfield_jue_de_zi_shen_jian_kang_zhuang_kuang_ru_he", "boolfield_jiao_zhi_guo_qu_yi_nian_zhuang_tai_ru_he", "boolfield_yun_dong_pian_hao", "boolfield_yun_dong_shi_chang", "boolfield_jin_lai_you_wu_shen_ti_bu_shi_zheng_zhuang", )}), 
        ("个人健康行为调查", {"fields": ("boolfield_ping_jun_shui_mian_shi_chang", "boolfield_chi_xu_shi_mian_shi_jian", "boolfield_yin_jiu_pin_ci", "boolfield_xi_yan_pin_ci", )}), 
        ("社会环境评估", {"fields": ("boolfield_nin_dui_ju_zhu_huan_jing_man_yi_ma", "boolfield_nin_suo_zai_de_she_qu_jiao_tong_fang_bian_ma", )}), ]
    autocomplete_fields = ["boolfield_yi_chuan_xing_ji_bing", "boolfield_yao_pin_ming", "boolfield_jia_zu_xing_ji_bing", "boolfield_shou_shu_ming_cheng", "boolfield_ge_ren_bing_shi", "boolfield_wai_shang_xing_ji_bing", "boolfield_jin_lai_you_wu_shen_ti_bu_shi_zheng_zhuang", ]
    radio_fields = {"boolfield_xing_ge_qing_xiang": admin.VERTICAL, "boolfield_shi_mian_qing_kuang": admin.VERTICAL, "boolfield_sheng_huo_gong_zuo_ya_li_qing_kuang": admin.VERTICAL, "boolfield_jue_de_zi_shen_jian_kang_zhuang_kuang_ru_he": admin.VERTICAL, "boolfield_yun_dong_shi_chang": admin.VERTICAL, "boolfield_yin_jiu_pin_ci": admin.VERTICAL, "boolfield_xi_yan_pin_ci": admin.VERTICAL, }

admin.site.register(A6299, A6299Admin)
clinic_site.register(A6299, A6299Admin)

class A6220Admin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("糖尿病监测评估", {"fields": ("boolfield_kong_fu_xue_tang_ping_jun_zhi", "boolfield_can_hou_2_xiao_shi_xue_tang_ping_jun_zhi", "boolfield_xue_ya_jian_ce_ping_gu", "boolfield_tang_niao_bing_kong_zhi_xiao_guo_ping_gu", )}), ]
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
        ("糖尿病一般随访", {"fields": ("boolfield_yong_yao_pin_ci", "boolfield_yao_pin_dan_wei", "boolfield_yin_jiu_pin_ci", "boolfield_xi_yan_pin_ci", "boolfield_tang_niao_bing_zheng_zhuang", "boolfield_yao_pin_ming", )}), 
        ("足背动脉检查", {"fields": ("boolfield_zuo_jiao", "boolfield_you_jiao", )}), 
        ("眼底检查", {"fields": ("boolfield_yan_di", )}), 
        ("血压监测", {"fields": ("boolfield_shou_suo_ya", "boolfield_shu_zhang_ya", )}), 
        ("空腹血糖检查", {"fields": ("boolfield_kong_fu_xue_tang", )}), ]
    autocomplete_fields = ["boolfield_yao_pin_ming", ]
    radio_fields = {"boolfield_yin_jiu_pin_ci": admin.VERTICAL, "boolfield_xi_yan_pin_ci": admin.VERTICAL, "boolfield_zuo_jiao": admin.VERTICAL, "boolfield_you_jiao": admin.VERTICAL, }

admin.site.register(T6301, T6301Admin)
clinic_site.register(T6301, T6301Admin)

class T8901Admin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("非胰岛素依赖性糖尿病", {"fields": ("boolfield_ji_bing_ming_cheng", "boolfield_ke_neng_zhen_duan", "boolfield_pai_chu_zhen_duan", )}), ]
    autocomplete_fields = ["boolfield_ji_bing_ming_cheng", "boolfield_ke_neng_zhen_duan", "boolfield_pai_chu_zhen_duan", ]

admin.site.register(T8901, T8901Admin)
clinic_site.register(T8901, T8901Admin)

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
        ("院外咨询", {"fields": ("boolfield_bing_qing_bu_chong_miao_shu", "boolfield_zheng_zhuang", "boolfield_chang_yong_zheng_zhuang", )}), ]
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

class Tang_niao_bing_zi_wo_jian_ceAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("糖尿病自我监测", {"fields": ("boolfield_kong_fu_xue_tang", )}), ]

admin.site.register(Tang_niao_bing_zi_wo_jian_ce, Tang_niao_bing_zi_wo_jian_ceAdmin)
clinic_site.register(Tang_niao_bing_zi_wo_jian_ce, Tang_niao_bing_zi_wo_jian_ceAdmin)

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
        ("糖尿病专用问诊", {"fields": ("boolfield_bing_qing_bu_chong_miao_shu", "boolfield_zheng_zhuang", "boolfield_tang_niao_bing_zheng_zhuang", )}), ]
    autocomplete_fields = ["boolfield_zheng_zhuang", ]

admin.site.register(Tang_niao_bing_zhuan_yong_wen_zhen, Tang_niao_bing_zhuan_yong_wen_zhenAdmin)
clinic_site.register(Tang_niao_bing_zhuan_yong_wen_zhen, Tang_niao_bing_zhuan_yong_wen_zhenAdmin)

class A3101Admin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("体格检查表", {"fields": ("boolfield_you_yan_shi_li", "boolfield_zuo_yan_shi_li", "boolfield_ti_wen", "boolfield_mai_bo", "boolfield_hu_xi_pin_lv", "boolfield_shen_gao", "boolfield_ti_zhong", "boolfield_ti_zhi_zhi_shu", "boolfield_shou_suo_ya", "boolfield_shu_zhang_ya", "boolfield_yao_wei", "boolfield_yun_dong_neng_li", "boolfield_zuo_er_ting_li", "boolfield_you_er_ting_li", "boolfield_kou_chun", "boolfield_chi_lie", "boolfield_yan_bu", "boolfield_xia_zhi_shui_zhong", )}), ]
    radio_fields = {"boolfield_kou_chun": admin.VERTICAL, "boolfield_chi_lie": admin.VERTICAL, "boolfield_xia_zhi_shui_zhong": admin.VERTICAL, }

admin.site.register(A3101, A3101Admin)
clinic_site.register(A3101, A3101Admin)

class A6502Admin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("门诊分诊", {"fields": ("boolfield_yu_yue_shi_jian", "boolfield_qian_dao_que_ren", "boolfield_ze_ren_ren", )}), ]
    autocomplete_fields = ["boolfield_ze_ren_ren", ]
    radio_fields = {"boolfield_qian_dao_que_ren": admin.VERTICAL, }

admin.site.register(A6502, A6502Admin)
clinic_site.register(A6502, A6502Admin)

class A6501Admin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("代人预约挂号", {"fields": ("boolfield_yu_yue_shi_jian", "boolfield_ze_ren_ren", )}), ]
    autocomplete_fields = ["boolfield_ze_ren_ren", ]

admin.site.register(A6501, A6501Admin)
clinic_site.register(A6501, A6501Admin)

class Men_zhen_chu_fang_biaoAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("药物处方", {"fields": ("boolfield_yong_yao_pin_ci", "boolfield_chang_yong_chu_fang_liang", "boolfield_yong_yao_liao_cheng", "boolfield_yong_yao_tu_jing", "boolfield_yao_pin_ming", )}), ]
    autocomplete_fields = ["boolfield_yao_pin_ming", ]

admin.site.register(Men_zhen_chu_fang_biao, Men_zhen_chu_fang_biaoAdmin)
clinic_site.register(Men_zhen_chu_fang_biao, Men_zhen_chu_fang_biaoAdmin)
