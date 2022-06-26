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


class CustomerScheduleAdmin(HsscFormAdmin):
    autocomplete_fields = ["scheduled_operator", ]
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
    inlines = [CustomerScheduleDraftInline, ]
clinic_site.register(CustomerSchedulePackage, CustomerSchedulePackageAdmin)
admin.site.register(CustomerSchedulePackage, CustomerSchedulePackageAdmin)

# **********************************************************************************************************************
# Service表单Admin
# **********************************************************************************************************************

class Men_zhen_ji_lu_hui_zongAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("门诊服务记录单", {"fields": ("boolfield_zheng_zhuang", "boolfield_jian_cha_xiang_mu", "boolfield_zhen_duan", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_jian_kang_gan_yu_fu_wu", "boolfield_fei_yong_he_ji", "boolfield_men_zhen_bing_li_fu_jian", )}), ]
    autocomplete_fields = ["boolfield_zheng_zhuang", "boolfield_jian_cha_xiang_mu", "boolfield_zhen_duan", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_jian_kang_gan_yu_fu_wu", ]

admin.site.register(Men_zhen_ji_lu_hui_zong, Men_zhen_ji_lu_hui_zongAdmin)
clinic_site.register(Men_zhen_ji_lu_hui_zong, Men_zhen_ji_lu_hui_zongAdmin)

class Chong_xin_yu_yue_an_paiAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("预约单", {"fields": ("boolfield_yu_yue_shi_jian", "boolfield_jiu_zhen_wen_ti", "boolfield_jiu_zhen_ji_gou_ze_ren_ren", "boolfield_shi_yong_fu_wu_chan_pin", "boolfield_fu_jia_fu_wu_yao_qiu", )}), 
        ("接单确认表", {"fields": ("boolfield_jie_dan_que_ren", "boolfield_ju_jue_jie_dan_yuan_yin", )}), ]
    autocomplete_fields = ["boolfield_jiu_zhen_ji_gou_ze_ren_ren", ]
    radio_fields = {"boolfield_jie_dan_que_ren": admin.VERTICAL, }

admin.site.register(Chong_xin_yu_yue_an_pai, Chong_xin_yu_yue_an_paiAdmin)
clinic_site.register(Chong_xin_yu_yue_an_pai, Chong_xin_yu_yue_an_paiAdmin)

class Zhen_suo_yu_yueAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("预约单", {"fields": ("boolfield_yu_yue_shi_jian", "boolfield_jiu_zhen_wen_ti", "boolfield_jiu_zhen_ji_gou_ze_ren_ren", "boolfield_shi_yong_fu_wu_chan_pin", "boolfield_fu_jia_fu_wu_yao_qiu", )}), ]
    autocomplete_fields = ["boolfield_jiu_zhen_ji_gou_ze_ren_ren", ]

admin.site.register(Zhen_suo_yu_yue, Zhen_suo_yu_yueAdmin)
clinic_site.register(Zhen_suo_yu_yue, Zhen_suo_yu_yueAdmin)

class Li_pei_shen_qing_chong_shenAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("人身险理赔申请书", {"fields": ("boolfield_shen_qing_ren_xing_ming", "boolfield_xing_bie", "boolfield_yu_chu_xian_ren_guan_xi", "boolfield_zheng_jian_lei_xing", "boolfield_zheng_jian_hao_ma", "boolfield_zheng_jian_you_xiao_qi", "boolfield_guo_ji_di_qu", "boolfield_hang_ye", "boolfield_zhi_ye", "boolfield_lian_xi_dian_hua", "boolfield_chang_zhu_di_zhi", "boolfield_shen_qing_ren_zheng_jian_fu_jian", )}), 
        ("人身险理赔申请书审核单", {"fields": ("boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu", "boolfield_ren_shen_xian_li_pei_shen_qing_shu_tui_dan_yuan_yin", )}), 
        ("门诊服务记录单", {"fields": ("boolfield_zheng_zhuang", "boolfield_jian_cha_xiang_mu", "boolfield_zhen_duan", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_jian_kang_gan_yu_fu_wu", "boolfield_fei_yong_he_ji", "boolfield_men_zhen_bing_li_fu_jian", )}), 
        ("门诊记录单审核单", {"fields": ("boolfield_men_zhen_ji_lu_dan_tui_dan_yuan_yin", "boolfield_li_pei_men_zhen_ji_lu_qian_shu", )}), 
        ("理赔对账单", {"fields": ("boolfield_xu_hao", "boolfield_bao_dan_hao", "boolfield_bao_an_shi_jian", "boolfield_bao_an_ren", "boolfield_bao_an_ren_lian_xi_dian_hua", "boolfield_chu_xian_shi_jian", "boolfield_chu_xian_ren_xing_ming", "boolfield_chu_xian_di_dian", "boolfield_chu_xian_di_dian_sheng_ji_bie", "boolfield_chu_xian_di_dian_shi_ji_bie", "boolfield_shi_gu_gai_kuo", "boolfield_zheng_jian_lei_xing", "boolfield_bei_bao_xian_ren_zheng_jian_hao_ma", "boolfield_xing_bie", "boolfield_nian_ling", "boolfield_chu_sheng_ri_qi", "boolfield_gui_shu_cheng_shi", "boolfield_yi_yuan_xin_xi", "boolfield_ji_bing_xin_xi", "boolfield_li_pei_jin_e", "boolfield_li_pei_fang_shi", "boolfield_bei_zhu", "boolfield_bei_bao_ren_zheng_jian_fu_jian", )}), 
        ("理赔对账单审核单", {"fields": ("boolfield_li_pei_dui_zhang_dan_qian_shu", "boolfield_li_pei_dui_zhang_dan_tui_dan_yuan_yin", )}), 
        ("治疗费用汇总单", {"fields": ("boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu", "boolfield_bao_dan_nei_fu_wu_fei_yong", "boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu", "boolfield_bao_dan_wai_fu_wu_fei_yong", "boolfield_fei_yong_he_ji", "boolfield_hui_zong_fei_yong_qing_dan_fu_jian", )}), 
        ("理赔费用汇总单审核", {"fields": ("boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu", "boolfield_li_pei_fei_yong_hui_zong_dan_tui_dan_yuan_yin", )}), ]
    autocomplete_fields = ["boolfield_zheng_zhuang", "boolfield_jian_cha_xiang_mu", "boolfield_zhen_duan", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_jian_kang_gan_yu_fu_wu", ]
    radio_fields = {"boolfield_yu_chu_xian_ren_guan_xi": admin.VERTICAL, "boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu": admin.VERTICAL, "boolfield_li_pei_men_zhen_ji_lu_qian_shu": admin.VERTICAL, "boolfield_li_pei_dui_zhang_dan_qian_shu": admin.VERTICAL, "boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu": admin.VERTICAL, }

admin.site.register(Li_pei_shen_qing_chong_shen, Li_pei_shen_qing_chong_shenAdmin)
clinic_site.register(Li_pei_shen_qing_chong_shen, Li_pei_shen_qing_chong_shenAdmin)

class Yu_yue_zi_xunAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("预约单", {"fields": ("boolfield_yu_yue_shi_jian", "boolfield_jiu_zhen_wen_ti", "boolfield_jiu_zhen_ji_gou_ze_ren_ren", "boolfield_shi_yong_fu_wu_chan_pin", "boolfield_fu_jia_fu_wu_yao_qiu", )}), ]
    autocomplete_fields = ["boolfield_jiu_zhen_ji_gou_ze_ren_ren", ]

admin.site.register(Yu_yue_zi_xun, Yu_yue_zi_xunAdmin)
clinic_site.register(Yu_yue_zi_xun, Yu_yue_zi_xunAdmin)

class Ti_jiao_he_bao_zi_liaoAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("人身险理赔申请书", {"fields": ("boolfield_shen_qing_ren_xing_ming", "boolfield_xing_bie", "boolfield_yu_chu_xian_ren_guan_xi", "boolfield_zheng_jian_lei_xing", "boolfield_zheng_jian_hao_ma", "boolfield_zheng_jian_you_xiao_qi", "boolfield_guo_ji_di_qu", "boolfield_hang_ye", "boolfield_zhi_ye", "boolfield_lian_xi_dian_hua", "boolfield_chang_zhu_di_zhi", "boolfield_shen_qing_ren_zheng_jian_fu_jian", )}), 
        ("人身险理赔申请书审核单", {"fields": ("boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu", "boolfield_ren_shen_xian_li_pei_shen_qing_shu_tui_dan_yuan_yin", )}), 
        ("门诊服务记录单", {"fields": ("boolfield_zheng_zhuang", "boolfield_jian_cha_xiang_mu", "boolfield_zhen_duan", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_jian_kang_gan_yu_fu_wu", "boolfield_fei_yong_he_ji", "boolfield_men_zhen_bing_li_fu_jian", )}), 
        ("门诊记录单审核单", {"fields": ("boolfield_men_zhen_ji_lu_dan_tui_dan_yuan_yin", "boolfield_li_pei_men_zhen_ji_lu_qian_shu", )}), 
        ("理赔对账单", {"fields": ("boolfield_xu_hao", "boolfield_bao_dan_hao", "boolfield_bao_an_shi_jian", "boolfield_bao_an_ren", "boolfield_bao_an_ren_lian_xi_dian_hua", "boolfield_chu_xian_shi_jian", "boolfield_chu_xian_ren_xing_ming", "boolfield_chu_xian_di_dian", "boolfield_chu_xian_di_dian_sheng_ji_bie", "boolfield_chu_xian_di_dian_shi_ji_bie", "boolfield_shi_gu_gai_kuo", "boolfield_zheng_jian_lei_xing", "boolfield_bei_bao_xian_ren_zheng_jian_hao_ma", "boolfield_xing_bie", "boolfield_nian_ling", "boolfield_chu_sheng_ri_qi", "boolfield_gui_shu_cheng_shi", "boolfield_yi_yuan_xin_xi", "boolfield_ji_bing_xin_xi", "boolfield_li_pei_jin_e", "boolfield_li_pei_fang_shi", "boolfield_bei_zhu", "boolfield_bei_bao_ren_zheng_jian_fu_jian", )}), 
        ("理赔对账单审核单", {"fields": ("boolfield_li_pei_dui_zhang_dan_qian_shu", "boolfield_li_pei_dui_zhang_dan_tui_dan_yuan_yin", )}), 
        ("治疗费用汇总单", {"fields": ("boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu", "boolfield_bao_dan_nei_fu_wu_fei_yong", "boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu", "boolfield_bao_dan_wai_fu_wu_fei_yong", "boolfield_fei_yong_he_ji", "boolfield_hui_zong_fei_yong_qing_dan_fu_jian", )}), 
        ("理赔费用汇总单审核", {"fields": ("boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu", "boolfield_li_pei_fei_yong_hui_zong_dan_tui_dan_yuan_yin", )}), 
        ("保险审核单", {"fields": ("boolfield_shi_fou_shen_he_tong_guo", "boolfield_li_pei_shen_qing_tui_hui_yuan_yin", )}), ]
    autocomplete_fields = ["boolfield_zheng_zhuang", "boolfield_jian_cha_xiang_mu", "boolfield_zhen_duan", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_jian_kang_gan_yu_fu_wu", ]
    radio_fields = {"boolfield_yu_chu_xian_ren_guan_xi": admin.VERTICAL, "boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu": admin.VERTICAL, "boolfield_li_pei_men_zhen_ji_lu_qian_shu": admin.VERTICAL, "boolfield_li_pei_dui_zhang_dan_qian_shu": admin.VERTICAL, "boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu": admin.VERTICAL, "boolfield_shi_fou_shen_he_tong_guo": admin.VERTICAL, }

admin.site.register(Ti_jiao_he_bao_zi_liao, Ti_jiao_he_bao_zi_liaoAdmin)
clinic_site.register(Ti_jiao_he_bao_zi_liao, Ti_jiao_he_bao_zi_liaoAdmin)

class Li_pei_shen_qing_fu_wuAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("理赔对账单", {"fields": ("boolfield_xu_hao", "boolfield_bao_dan_hao", "boolfield_bao_an_shi_jian", "boolfield_bao_an_ren", "boolfield_bao_an_ren_lian_xi_dian_hua", "boolfield_chu_xian_shi_jian", "boolfield_chu_xian_ren_xing_ming", "boolfield_chu_xian_di_dian", "boolfield_chu_xian_di_dian_sheng_ji_bie", "boolfield_chu_xian_di_dian_shi_ji_bie", "boolfield_shi_gu_gai_kuo", "boolfield_zheng_jian_lei_xing", "boolfield_bei_bao_xian_ren_zheng_jian_hao_ma", "boolfield_xing_bie", "boolfield_nian_ling", "boolfield_chu_sheng_ri_qi", "boolfield_gui_shu_cheng_shi", "boolfield_yi_yuan_xin_xi", "boolfield_ji_bing_xin_xi", "boolfield_li_pei_jin_e", "boolfield_li_pei_fang_shi", "boolfield_bei_zhu", "boolfield_bei_bao_ren_zheng_jian_fu_jian", )}), 
        ("治疗费用汇总单", {"fields": ("boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu", "boolfield_bao_dan_nei_fu_wu_fei_yong", "boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu", "boolfield_bao_dan_wai_fu_wu_fei_yong", "boolfield_fei_yong_he_ji", "boolfield_hui_zong_fei_yong_qing_dan_fu_jian", )}), 
        ("门诊服务记录单", {"fields": ("boolfield_zheng_zhuang", "boolfield_jian_cha_xiang_mu", "boolfield_zhen_duan", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_jian_kang_gan_yu_fu_wu", "boolfield_fei_yong_he_ji", "boolfield_men_zhen_bing_li_fu_jian", )}), 
        ("人身险理赔申请书", {"fields": ("boolfield_shen_qing_ren_xing_ming", "boolfield_xing_bie", "boolfield_yu_chu_xian_ren_guan_xi", "boolfield_zheng_jian_lei_xing", "boolfield_zheng_jian_hao_ma", "boolfield_zheng_jian_you_xiao_qi", "boolfield_guo_ji_di_qu", "boolfield_hang_ye", "boolfield_zhi_ye", "boolfield_lian_xi_dian_hua", "boolfield_chang_zhu_di_zhi", "boolfield_shen_qing_ren_zheng_jian_fu_jian", )}), ]
    autocomplete_fields = ["boolfield_zheng_zhuang", "boolfield_jian_cha_xiang_mu", "boolfield_zhen_duan", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_jian_kang_gan_yu_fu_wu", ]
    radio_fields = {"boolfield_yu_chu_xian_ren_guan_xi": admin.VERTICAL, }

admin.site.register(Li_pei_shen_qing_fu_wu, Li_pei_shen_qing_fu_wuAdmin)
clinic_site.register(Li_pei_shen_qing_fu_wu, Li_pei_shen_qing_fu_wuAdmin)

class Li_pei_shen_qing_shu_shen_heAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("人身险理赔申请书", {"fields": ("boolfield_shen_qing_ren_xing_ming", "boolfield_xing_bie", "boolfield_yu_chu_xian_ren_guan_xi", "boolfield_zheng_jian_lei_xing", "boolfield_zheng_jian_hao_ma", "boolfield_zheng_jian_you_xiao_qi", "boolfield_guo_ji_di_qu", "boolfield_hang_ye", "boolfield_zhi_ye", "boolfield_lian_xi_dian_hua", "boolfield_chang_zhu_di_zhi", "boolfield_shen_qing_ren_zheng_jian_fu_jian", )}), 
        ("人身险理赔申请书审核单", {"fields": ("boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu", "boolfield_ren_shen_xian_li_pei_shen_qing_shu_tui_dan_yuan_yin", )}), 
        ("理赔对账单", {"fields": ("boolfield_xu_hao", "boolfield_bao_dan_hao", "boolfield_bao_an_shi_jian", "boolfield_bao_an_ren", "boolfield_bao_an_ren_lian_xi_dian_hua", "boolfield_chu_xian_shi_jian", "boolfield_chu_xian_ren_xing_ming", "boolfield_chu_xian_di_dian", "boolfield_chu_xian_di_dian_sheng_ji_bie", "boolfield_chu_xian_di_dian_shi_ji_bie", "boolfield_shi_gu_gai_kuo", "boolfield_zheng_jian_lei_xing", "boolfield_bei_bao_xian_ren_zheng_jian_hao_ma", "boolfield_xing_bie", "boolfield_nian_ling", "boolfield_chu_sheng_ri_qi", "boolfield_gui_shu_cheng_shi", "boolfield_yi_yuan_xin_xi", "boolfield_ji_bing_xin_xi", "boolfield_li_pei_jin_e", "boolfield_li_pei_fang_shi", "boolfield_bei_zhu", "boolfield_bei_bao_ren_zheng_jian_fu_jian", )}), 
        ("理赔对账单审核单", {"fields": ("boolfield_li_pei_dui_zhang_dan_qian_shu", "boolfield_li_pei_dui_zhang_dan_tui_dan_yuan_yin", )}), 
        ("门诊服务记录单", {"fields": ("boolfield_zheng_zhuang", "boolfield_jian_cha_xiang_mu", "boolfield_zhen_duan", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_jian_kang_gan_yu_fu_wu", "boolfield_fei_yong_he_ji", "boolfield_men_zhen_bing_li_fu_jian", )}), 
        ("门诊记录单审核单", {"fields": ("boolfield_men_zhen_ji_lu_dan_tui_dan_yuan_yin", "boolfield_li_pei_men_zhen_ji_lu_qian_shu", )}), 
        ("治疗费用汇总单", {"fields": ("boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu", "boolfield_bao_dan_nei_fu_wu_fei_yong", "boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu", "boolfield_bao_dan_wai_fu_wu_fei_yong", "boolfield_fei_yong_he_ji", "boolfield_hui_zong_fei_yong_qing_dan_fu_jian", )}), 
        ("理赔费用汇总单审核", {"fields": ("boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu", "boolfield_li_pei_fei_yong_hui_zong_dan_tui_dan_yuan_yin", )}), ]
    autocomplete_fields = ["boolfield_zheng_zhuang", "boolfield_jian_cha_xiang_mu", "boolfield_zhen_duan", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_jian_kang_gan_yu_fu_wu", ]
    radio_fields = {"boolfield_yu_chu_xian_ren_guan_xi": admin.VERTICAL, "boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu": admin.VERTICAL, "boolfield_li_pei_dui_zhang_dan_qian_shu": admin.VERTICAL, "boolfield_li_pei_men_zhen_ji_lu_qian_shu": admin.VERTICAL, "boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu": admin.VERTICAL, }

admin.site.register(Li_pei_shen_qing_shu_shen_he, Li_pei_shen_qing_shu_shen_heAdmin)
clinic_site.register(Li_pei_shen_qing_shu_shen_he, Li_pei_shen_qing_shu_shen_heAdmin)

class Man_yi_du_diao_chaAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("满意度调查表", {"fields": ("boolfield_yi_liao_fu_wu_ji_neng_xiang_mu_ping_fen", "boolfield_ping_tai_fu_wu_xiang_mu_ping_fen", "boolfield_fu_wu_liu_cheng_ping_fen", "boolfield_xi_wang_zeng_jia_de_fu_wu_xiang_mu", "boolfield_fu_wu_xiao_lv_ping_fen", "boolfield_you_dai_gai_jin_de_fu_wu", )}), ]
    radio_fields = {"boolfield_yi_liao_fu_wu_ji_neng_xiang_mu_ping_fen": admin.VERTICAL, "boolfield_ping_tai_fu_wu_xiang_mu_ping_fen": admin.VERTICAL, "boolfield_fu_wu_liu_cheng_ping_fen": admin.VERTICAL, "boolfield_fu_wu_xiao_lv_ping_fen": admin.VERTICAL, }

admin.site.register(Man_yi_du_diao_cha, Man_yi_du_diao_chaAdmin)
clinic_site.register(Man_yi_du_diao_cha, Man_yi_du_diao_chaAdmin)

class Zhen_hou_sui_fangAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("诊后回访单", {"fields": ("boolfield_zhi_liao_gan_shou_he_xiao_guo_ping_jia", "boolfield_deng_hou_qing_kuang", "boolfield_cun_zai_de_wen_ti", "boolfield_you_dai_gai_jin_de_fu_wu", "boolfield_nin_de_dan_xin_he_gu_lv", "boolfield_nin_hai_xu_yao_de_fu_wu", "boolfield_nin_cong_he_chu_zhi_dao_wo_men_de_fu_wu", "boolfield_nin_shi_fou_yuan_yi_xiang_ta_ren_tui_jian_wo_men", )}), ]
    radio_fields = {"boolfield_zhi_liao_gan_shou_he_xiao_guo_ping_jia": admin.VERTICAL, "boolfield_deng_hou_qing_kuang": admin.VERTICAL, "boolfield_nin_cong_he_chu_zhi_dao_wo_men_de_fu_wu": admin.VERTICAL, "boolfield_nin_shi_fou_yuan_yi_xiang_ta_ren_tui_jian_wo_men": admin.VERTICAL, }

admin.site.register(Zhen_hou_sui_fang, Zhen_hou_sui_fangAdmin)
clinic_site.register(Zhen_hou_sui_fang, Zhen_hou_sui_fangAdmin)

class Zhen_jian_sui_fangAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("诊间随访表", {"fields": ("boolfield_deng_hou_qing_kuang", "boolfield_jie_dai_fu_wu", "boolfield_zhi_liao_jian_gou_tong_qing_kuang", "boolfield_zhi_liao_gan_shou_he_xiao_guo_ping_jia", "boolfield_nin_de_dan_xin_he_gu_lv", "boolfield_cun_zai_de_wen_ti", "boolfield_nin_xiang_yao_de_bang_zhu", "boolfield_qi_ta_xu_qiu", )}), ]
    radio_fields = {"boolfield_deng_hou_qing_kuang": admin.VERTICAL, "boolfield_jie_dai_fu_wu": admin.VERTICAL, "boolfield_zhi_liao_jian_gou_tong_qing_kuang": admin.VERTICAL, "boolfield_zhi_liao_gan_shou_he_xiao_guo_ping_jia": admin.VERTICAL, }

admin.site.register(Zhen_jian_sui_fang, Zhen_jian_sui_fangAdmin)
clinic_site.register(Zhen_jian_sui_fang, Zhen_jian_sui_fangAdmin)

class Men_zhen_ji_luAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("门诊服务记录单", {"fields": ("boolfield_zheng_zhuang", "boolfield_jian_cha_xiang_mu", "boolfield_zhen_duan", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_jian_kang_gan_yu_fu_wu", "boolfield_fei_yong_he_ji", "boolfield_men_zhen_bing_li_fu_jian", )}), ]
    autocomplete_fields = ["boolfield_zheng_zhuang", "boolfield_jian_cha_xiang_mu", "boolfield_zhen_duan", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_jian_kang_gan_yu_fu_wu", ]

admin.site.register(Men_zhen_ji_lu, Men_zhen_ji_luAdmin)
clinic_site.register(Men_zhen_ji_lu, Men_zhen_ji_luAdmin)

class Yu_yue_tong_zhiAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("预约通知单", {"fields": ("boolfield_ji_gou_ming_cheng", "boolfield_yu_yue_xu_hao", "boolfield_ji_gou_lian_xi_di_zhi", "boolfield_ji_gou_lian_xi_dian_hua", "boolfield_jiu_zhen_yi_sheng", )}), 
        ("预约单", {"fields": ("boolfield_yu_yue_shi_jian", "boolfield_jiu_zhen_wen_ti", "boolfield_jiu_zhen_ji_gou_ze_ren_ren", "boolfield_shi_yong_fu_wu_chan_pin", "boolfield_fu_jia_fu_wu_yao_qiu", )}), ]
    autocomplete_fields = ["boolfield_jiu_zhen_ji_gou_ze_ren_ren", ]

admin.site.register(Yu_yue_tong_zhi, Yu_yue_tong_zhiAdmin)
clinic_site.register(Yu_yue_tong_zhi, Yu_yue_tong_zhiAdmin)

class Fen_zhen_que_renAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("到店确认表", {"fields": ("boolfield_dao_dian_shen_fen_yan_zheng", "boolfield_dao_da_que_ren", )}), 
        ("预约单", {"fields": ("boolfield_yu_yue_shi_jian", "boolfield_jiu_zhen_wen_ti", "boolfield_jiu_zhen_ji_gou_ze_ren_ren", "boolfield_shi_yong_fu_wu_chan_pin", "boolfield_fu_jia_fu_wu_yao_qiu", )}), ]
    autocomplete_fields = ["boolfield_jiu_zhen_ji_gou_ze_ren_ren", ]
    radio_fields = {"boolfield_dao_da_que_ren": admin.VERTICAL, }

admin.site.register(Fen_zhen_que_ren, Fen_zhen_que_renAdmin)
clinic_site.register(Fen_zhen_que_ren, Fen_zhen_que_renAdmin)

class Yu_yue_que_renAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("预约单", {"fields": ("boolfield_yu_yue_shi_jian", "boolfield_jiu_zhen_wen_ti", "boolfield_jiu_zhen_ji_gou_ze_ren_ren", "boolfield_shi_yong_fu_wu_chan_pin", "boolfield_fu_jia_fu_wu_yao_qiu", )}), 
        ("接单确认表", {"fields": ("boolfield_jie_dan_que_ren", "boolfield_ju_jue_jie_dan_yuan_yin", )}), ]
    autocomplete_fields = ["boolfield_jiu_zhen_ji_gou_ze_ren_ren", ]
    radio_fields = {"boolfield_jie_dan_que_ren": admin.VERTICAL, }

admin.site.register(Yu_yue_que_ren, Yu_yue_que_renAdmin)
clinic_site.register(Yu_yue_que_ren, Yu_yue_que_renAdmin)

class Yu_yue_an_paiAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("预约单", {"fields": ("boolfield_yu_yue_shi_jian", "boolfield_jiu_zhen_wen_ti", "boolfield_jiu_zhen_ji_gou_ze_ren_ren", "boolfield_shi_yong_fu_wu_chan_pin", "boolfield_fu_jia_fu_wu_yao_qiu", )}), ]
    autocomplete_fields = ["boolfield_jiu_zhen_ji_gou_ze_ren_ren", ]

admin.site.register(Yu_yue_an_pai, Yu_yue_an_paiAdmin)
clinic_site.register(Yu_yue_an_pai, Yu_yue_an_paiAdmin)

class Ji_gou_ji_ben_xin_xi_biaoAdmin(HsscFormAdmin):
    fieldssets = [
        ("机构基本信息表", {"fields": ("boolfield_ji_gou_lian_xi_di_zhi", "boolfield_ji_gou_bian_ma", "boolfield_ji_gou_ming_cheng", "boolfield_ji_gou_dai_ma", "boolfield_ji_gou_shu_xing", "boolfield_ji_gou_ceng_ji", "boolfield_suo_zai_hang_zheng_qu_hua_dai_ma", "boolfield_xing_zheng_qu_hua_gui_shu", "boolfield_fa_ding_fu_ze_ren", "boolfield_ji_gou_lian_xi_dian_hua", )}), ]
    search_fields = ["name", "pym", ]

admin.site.register(Ji_gou_ji_ben_xin_xi_biao, Ji_gou_ji_ben_xin_xi_biaoAdmin)
clinic_site.register(Ji_gou_ji_ben_xin_xi_biao, Ji_gou_ji_ben_xin_xi_biaoAdmin)

class Zhi_yuan_ji_ben_xin_xi_biaoAdmin(HsscFormAdmin):
    fieldssets = [
        ("职员基本信息表", {"fields": ("boolfield_zheng_jian_hao_ma", "boolfield_zhi_ye_zi_zhi", "boolfield_zhuan_chang", "boolfield_zhi_ye_shi_jian", "boolfield_zhi_yuan_bian_ma", "boolfield_ji_gou_lian_xi_dian_hua", "boolfield_bei_bao_ren_xing_ming", "boolfield_suo_shu_ji_gou", "boolfield_fu_wu_jue_se", )}), ]
    autocomplete_fields = ["boolfield_suo_shu_ji_gou", ]
    search_fields = ["name", "pym", ]

admin.site.register(Zhi_yuan_ji_ben_xin_xi_biao, Zhi_yuan_ji_ben_xin_xi_biaoAdmin)
clinic_site.register(Zhi_yuan_ji_ben_xin_xi_biao, Zhi_yuan_ji_ben_xin_xi_biaoAdmin)

class Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_chaAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), ]

admin.site.register(Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_cha, Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_chaAdmin)
clinic_site.register(Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_cha, Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_chaAdmin)

class She_bei_ji_ben_xin_xi_ji_luAdmin(HsscFormAdmin):
    fieldssets = [
        ("设备基本信息表", {"fields": ("boolfield_she_bei_bian_ma", "boolfield_sheng_chan_chang_jia", "boolfield_she_bei_fu_wu_dan_wei_hao_shi", "boolfield_she_bei_jian_xiu_zhou_qi", "boolfield_she_bei_shi_yong_cheng_ben", "boolfield_she_bei_ming_cheng", "boolfield_ji_gou_lian_xi_dian_hua", "boolfield_she_bei_shi_yong_fu_wu_gong_neng", )}), ]
    autocomplete_fields = ["boolfield_she_bei_shi_yong_fu_wu_gong_neng", ]
    search_fields = ["name", "pym", ]

admin.site.register(She_bei_ji_ben_xin_xi_ji_lu, She_bei_ji_ben_xin_xi_ji_luAdmin)
clinic_site.register(She_bei_ji_ben_xin_xi_ji_lu, She_bei_ji_ben_xin_xi_ji_luAdmin)

class Gong_ying_shang_ji_ben_xin_xi_diao_chaAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), ]

admin.site.register(Gong_ying_shang_ji_ben_xin_xi_diao_cha, Gong_ying_shang_ji_ben_xin_xi_diao_chaAdmin)
clinic_site.register(Gong_ying_shang_ji_ben_xin_xi_diao_cha, Gong_ying_shang_ji_ben_xin_xi_diao_chaAdmin)

class Yao_pin_ji_ben_xin_xi_biaoAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), ]

admin.site.register(Yao_pin_ji_ben_xin_xi_biao, Yao_pin_ji_ben_xin_xi_biaoAdmin)
clinic_site.register(Yao_pin_ji_ben_xin_xi_biao, Yao_pin_ji_ben_xin_xi_biaoAdmin)

class Ju_min_ji_ben_xin_xi_diao_chaAdmin(HsscFormAdmin):
    fieldssets = [
        ("个人基本信息表", {"fields": ("boolfield_xu_hao", "boolfield_bao_dan_hao", "boolfield_zheng_jian_lei_xing", "boolfield_zheng_jian_hao_ma", "boolfield_bei_bao_ren_xing_ming", "boolfield_bei_bao_ren_xing_bie", "boolfield_chu_sheng_ri_qi", "boolfield_bao_xian_ze_ren", "boolfield_bao_xian_you_xiao_qi", "boolfield_lian_xi_dian_hua", "boolfield_chang_zhu_di_zhi", )}), ]
    search_fields = ["name", "pym", ]

admin.site.register(Ju_min_ji_ben_xin_xi_diao_cha, Ju_min_ji_ben_xin_xi_diao_chaAdmin)
clinic_site.register(Ju_min_ji_ben_xin_xi_diao_cha, Ju_min_ji_ben_xin_xi_diao_chaAdmin)
