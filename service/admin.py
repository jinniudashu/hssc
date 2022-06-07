from django.contrib import admin
from django.shortcuts import redirect

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
        base_form = 'base_form'
        extra_context['base_form'] = base_form
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # 把表单内容存入CustomerServiceLog
        import copy
        form_data = copy.copy(form.cleaned_data)
        create_customer_service_log(form_data, obj)

        # 发送服务作业完成信号
        print('发送操作完成信号, From service.admin.HsscFormAdmin.save_model：', obj.pid)
        operand_finished.send(sender=self, pid=obj.pid, request=request)

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


# **********************************************************************************************************************
# Service表单Admin
# **********************************************************************************************************************

class Bei_bao_ren_ji_ben_xin_xi_que_renAdmin(HsscFormAdmin):
    fieldssets = [
        ("绑定确认表", {"fields": ("boolfield_que_ren_ji_ben_xin_xi", "boolfield_ju_jue_bang_ding_yuan_yin", )}), 
        ("个人基本信息表", {"fields": ("characterfield_gender", "characterhssc_identification_number", "characterfield_name", "boolfield_xu_hao", "boolfield_bao_dan_hao", "boolfield_bao_xian_ze_ren", "boolfield_chang_zhu_di_zhi", "boolfield_lian_xi_dian_hua", "datetimefield_date_of_birth", "boolfield_bao_xian_you_xiao_qi", "boolfield_zheng_jian_lei_xing", )}), ]
    radio_fields = {"boolfield_que_ren_ji_ben_xin_xi": admin.VERTICAL, }
    search_fields = ["name", "pym", ]

admin.site.register(Bei_bao_ren_ji_ben_xin_xi_que_ren, Bei_bao_ren_ji_ben_xin_xi_que_renAdmin)
clinic_site.register(Bei_bao_ren_ji_ben_xin_xi_que_ren, Bei_bao_ren_ji_ben_xin_xi_que_renAdmin)

class Bao_xian_yong_hu_zhu_ceAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ),)}), 
        ("用户注册表", {"fields": ("characterfield_password_setting", "characterfield_confirm_password", "characterfield_username", )}), ]
    readonly_fields = ["characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ]

admin.site.register(Bao_xian_yong_hu_zhu_ce, Bao_xian_yong_hu_zhu_ceAdmin)
clinic_site.register(Bao_xian_yong_hu_zhu_ce, Bao_xian_yong_hu_zhu_ceAdmin)

class Chong_xin_yu_yue_an_paiAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ),)}), 
        ("接单确认表", {"fields": ("boolfield_qian_dao_que_ren", )}), 
        ("预约单", {"fields": ("boolfield_jiu_zhen_wen_ti", "boolfield_fu_jia_fu_wu_yao_qiu", "datetimefield_ri_qi_shi_jian", "boolfield_shi_yong_bao_xian_chan_pin", "boolfield_jiu_zhen_ji_gou_ze_ren_ren", )}), ]
    autocomplete_fields = ["boolfield_jiu_zhen_ji_gou_ze_ren_ren", ]
    radio_fields = {"boolfield_qian_dao_que_ren": admin.VERTICAL, }
    readonly_fields = ["characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ]

admin.site.register(Chong_xin_yu_yue_an_pai, Chong_xin_yu_yue_an_paiAdmin)
clinic_site.register(Chong_xin_yu_yue_an_pai, Chong_xin_yu_yue_an_paiAdmin)

class Zhen_suo_yu_yueAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ),)}), 
        ("预约单", {"fields": ("boolfield_jiu_zhen_wen_ti", "boolfield_fu_jia_fu_wu_yao_qiu", "datetimefield_ri_qi_shi_jian", "boolfield_shi_yong_bao_xian_chan_pin", "boolfield_jiu_zhen_ji_gou_ze_ren_ren", )}), ]
    autocomplete_fields = ["boolfield_jiu_zhen_ji_gou_ze_ren_ren", ]
    readonly_fields = ["characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ]

admin.site.register(Zhen_suo_yu_yue, Zhen_suo_yu_yueAdmin)
clinic_site.register(Zhen_suo_yu_yue, Zhen_suo_yu_yueAdmin)

class Li_pei_shen_qing_chong_shenAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ),)}), 
        ("人身险理赔申请书", {"fields": ("characterhssc_identification_number", "boolfield_shen_qing_ren_xing_ming", "boolfield_zheng_jian_you_xiao_qi", "boolfield_hang_ye", "boolfield_zhi_ye", "boolfield_chang_zhu_di_zhi", "boolfield_lian_xi_dian_hua", "boolfield_guo_ji_di_qu", "relatedfield_gender", "boolfield_zheng_jian_lei_xing", "boolfield_yu_chu_xian_ren_guan_xi", )}), 
        ("人身险理赔申请书审核单", {"fields": ("boolfield_tui_dan_yuan_yin", "boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu", )}), 
        ("门诊服务记录单", {"fields": ("boolfield_fei_yong_he_ji", "relatedfield_symptom_list", "boolfield_zhen_duan", "boolfield_jian_cha_xiang_mu", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_fu_wu_xiang_mu", "boolfield_men_zhen_bing_li_fu_jian", )}), 
        ("门诊记录单审核单", {"fields": ("boolfield_men_zhen_ji_lu_dan_tui_dan_yuan_yin", "boolfield_li_pei_men_zhen_ji_lu_qian_shu", )}), 
        ("理赔对账单", {"fields": ("characterfield_age", "boolfield_xu_hao", "boolfield_bao_dan_hao", "boolfield_bao_an_ren_lian_xi_dian_hua", "boolfield_chu_xian_ren_xing_ming", "boolfield_chu_xian_di_dian", "boolfield_shi_gu_gai_kuo", "boolfield_bei_bao_xian_ren_zheng_jian_hao_ma", "boolfield_gui_shu_cheng_shi", "boolfield_yi_yuan_xin_xi", "boolfield_ji_bing_xin_xi", "boolfield_li_pei_fang_shi", "boolfield_bei_zhu", "boolfield_bao_an_ren", "boolfield_li_pei_jin_e_bao_xiao_jian_mian_jin_e", "boolfield_chu_xian_di_dian_shi_ji_bie", "boolfield_chu_xian_di_dian_sheng_ji_bie", "datetimefield_date_of_birth", "boolfield_bao_an_shi_jian", "boolfield_chu_xian_shi_jian", "relatedfield_gender", "boolfield_zheng_jian_lei_xing", )}), 
        ("理赔对账单审核单", {"fields": ("boolfield_li_pei_dui_zhang_dan_tui_dan_yuan_yin", "boolfield_qian_shu_que_ren", )}), 
        ("治疗费用汇总单", {"fields": ("boolfield_fei_yong_he_ji", "boolfield_fei_yong", "boolfield_bao_dan_wai_fu_wu_fei_yong", "boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu", "boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu", "boolfield_fei_yong_qing_dan_fu_jian", )}), 
        ("理赔费用汇总单审核", {"fields": ("boolfield_li_pei_fei_yong_hui_zong_dan_tui_dan_yuan_yin", "boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu", )}), ]
    autocomplete_fields = ["relatedfield_symptom_list", "boolfield_zhen_duan", "boolfield_jian_cha_xiang_mu", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_fu_wu_xiang_mu", ]
    radio_fields = {"boolfield_yu_chu_xian_ren_guan_xi": admin.VERTICAL, "boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu": admin.VERTICAL, "boolfield_li_pei_men_zhen_ji_lu_qian_shu": admin.VERTICAL, "boolfield_qian_shu_que_ren": admin.VERTICAL, "boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu": admin.VERTICAL, }
    readonly_fields = ["characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ]

admin.site.register(Li_pei_shen_qing_chong_shen, Li_pei_shen_qing_chong_shenAdmin)
clinic_site.register(Li_pei_shen_qing_chong_shen, Li_pei_shen_qing_chong_shenAdmin)

class Yu_yue_zi_xunAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ),)}), 
        ("预约单", {"fields": ("boolfield_jiu_zhen_wen_ti", "boolfield_fu_jia_fu_wu_yao_qiu", "datetimefield_ri_qi_shi_jian", "boolfield_shi_yong_bao_xian_chan_pin", "boolfield_jiu_zhen_ji_gou_ze_ren_ren", )}), ]
    autocomplete_fields = ["boolfield_jiu_zhen_ji_gou_ze_ren_ren", ]
    readonly_fields = ["characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ]

admin.site.register(Yu_yue_zi_xun, Yu_yue_zi_xunAdmin)
clinic_site.register(Yu_yue_zi_xun, Yu_yue_zi_xunAdmin)

class Ti_jiao_he_bao_zi_liaoAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ),)}), 
        ("人身险理赔申请书", {"fields": ("characterhssc_identification_number", "boolfield_shen_qing_ren_xing_ming", "boolfield_zheng_jian_you_xiao_qi", "boolfield_hang_ye", "boolfield_zhi_ye", "boolfield_chang_zhu_di_zhi", "boolfield_lian_xi_dian_hua", "boolfield_guo_ji_di_qu", "relatedfield_gender", "boolfield_zheng_jian_lei_xing", "boolfield_yu_chu_xian_ren_guan_xi", )}), 
        ("人身险理赔申请书审核单", {"fields": ("boolfield_tui_dan_yuan_yin", "boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu", )}), 
        ("门诊服务记录单", {"fields": ("boolfield_fei_yong_he_ji", "relatedfield_symptom_list", "boolfield_zhen_duan", "boolfield_jian_cha_xiang_mu", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_fu_wu_xiang_mu", "boolfield_men_zhen_bing_li_fu_jian", )}), 
        ("门诊记录单审核单", {"fields": ("boolfield_men_zhen_ji_lu_dan_tui_dan_yuan_yin", "boolfield_li_pei_men_zhen_ji_lu_qian_shu", )}), 
        ("理赔对账单", {"fields": ("characterfield_age", "boolfield_xu_hao", "boolfield_bao_dan_hao", "boolfield_bao_an_ren_lian_xi_dian_hua", "boolfield_chu_xian_ren_xing_ming", "boolfield_chu_xian_di_dian", "boolfield_shi_gu_gai_kuo", "boolfield_bei_bao_xian_ren_zheng_jian_hao_ma", "boolfield_gui_shu_cheng_shi", "boolfield_yi_yuan_xin_xi", "boolfield_ji_bing_xin_xi", "boolfield_li_pei_fang_shi", "boolfield_bei_zhu", "boolfield_bao_an_ren", "boolfield_li_pei_jin_e_bao_xiao_jian_mian_jin_e", "boolfield_chu_xian_di_dian_shi_ji_bie", "boolfield_chu_xian_di_dian_sheng_ji_bie", "datetimefield_date_of_birth", "boolfield_bao_an_shi_jian", "boolfield_chu_xian_shi_jian", "relatedfield_gender", "boolfield_zheng_jian_lei_xing", )}), 
        ("理赔对账单审核单", {"fields": ("boolfield_li_pei_dui_zhang_dan_tui_dan_yuan_yin", "boolfield_qian_shu_que_ren", )}), 
        ("治疗费用汇总单", {"fields": ("boolfield_fei_yong_he_ji", "boolfield_fei_yong", "boolfield_bao_dan_wai_fu_wu_fei_yong", "boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu", "boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu", "boolfield_fei_yong_qing_dan_fu_jian", )}), 
        ("理赔费用汇总单审核", {"fields": ("boolfield_li_pei_fei_yong_hui_zong_dan_tui_dan_yuan_yin", "boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu", )}), 
        ("核保单", {"fields": ("boolfield_li_pei_shen_qing_tui_hui_yuan_yin", "boolfield_shi_fou_tong_guo_he_bao", )}), ]
    autocomplete_fields = ["relatedfield_symptom_list", "boolfield_zhen_duan", "boolfield_jian_cha_xiang_mu", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_fu_wu_xiang_mu", ]
    radio_fields = {"boolfield_yu_chu_xian_ren_guan_xi": admin.VERTICAL, "boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu": admin.VERTICAL, "boolfield_li_pei_men_zhen_ji_lu_qian_shu": admin.VERTICAL, "boolfield_qian_shu_que_ren": admin.VERTICAL, "boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu": admin.VERTICAL, "boolfield_shi_fou_tong_guo_he_bao": admin.VERTICAL, }
    readonly_fields = ["characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ]

admin.site.register(Ti_jiao_he_bao_zi_liao, Ti_jiao_he_bao_zi_liaoAdmin)
clinic_site.register(Ti_jiao_he_bao_zi_liao, Ti_jiao_he_bao_zi_liaoAdmin)

class Li_pei_shen_qing_fu_wuAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ),)}), 
        ("门诊服务记录单", {"fields": ("boolfield_fei_yong_he_ji", "relatedfield_symptom_list", "boolfield_zhen_duan", "boolfield_jian_cha_xiang_mu", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_fu_wu_xiang_mu", "boolfield_men_zhen_bing_li_fu_jian", )}), 
        ("治疗费用汇总单", {"fields": ("boolfield_fei_yong_he_ji", "boolfield_fei_yong", "boolfield_bao_dan_wai_fu_wu_fei_yong", "boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu", "boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu", "boolfield_fei_yong_qing_dan_fu_jian", )}), 
        ("理赔对账单", {"fields": ("characterfield_age", "boolfield_xu_hao", "boolfield_bao_dan_hao", "boolfield_bao_an_ren_lian_xi_dian_hua", "boolfield_chu_xian_ren_xing_ming", "boolfield_chu_xian_di_dian", "boolfield_shi_gu_gai_kuo", "boolfield_bei_bao_xian_ren_zheng_jian_hao_ma", "boolfield_gui_shu_cheng_shi", "boolfield_yi_yuan_xin_xi", "boolfield_ji_bing_xin_xi", "boolfield_li_pei_fang_shi", "boolfield_bei_zhu", "boolfield_bao_an_ren", "boolfield_li_pei_jin_e_bao_xiao_jian_mian_jin_e", "boolfield_chu_xian_di_dian_shi_ji_bie", "boolfield_chu_xian_di_dian_sheng_ji_bie", "datetimefield_date_of_birth", "boolfield_bao_an_shi_jian", "boolfield_chu_xian_shi_jian", "relatedfield_gender", "boolfield_zheng_jian_lei_xing", )}), 
        ("人身险理赔申请书", {"fields": ("characterhssc_identification_number", "boolfield_shen_qing_ren_xing_ming", "boolfield_zheng_jian_you_xiao_qi", "boolfield_hang_ye", "boolfield_zhi_ye", "boolfield_chang_zhu_di_zhi", "boolfield_lian_xi_dian_hua", "boolfield_guo_ji_di_qu", "relatedfield_gender", "boolfield_zheng_jian_lei_xing", "boolfield_yu_chu_xian_ren_guan_xi", )}), ]
    autocomplete_fields = ["relatedfield_symptom_list", "boolfield_zhen_duan", "boolfield_jian_cha_xiang_mu", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_fu_wu_xiang_mu", ]
    radio_fields = {"boolfield_yu_chu_xian_ren_guan_xi": admin.VERTICAL, }
    readonly_fields = ["characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ]

admin.site.register(Li_pei_shen_qing_fu_wu, Li_pei_shen_qing_fu_wuAdmin)
clinic_site.register(Li_pei_shen_qing_fu_wu, Li_pei_shen_qing_fu_wuAdmin)

class Li_pei_shen_qing_shu_shen_heAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ),)}), 
        ("人身险理赔申请书", {"fields": ("characterhssc_identification_number", "boolfield_shen_qing_ren_xing_ming", "boolfield_zheng_jian_you_xiao_qi", "boolfield_hang_ye", "boolfield_zhi_ye", "boolfield_chang_zhu_di_zhi", "boolfield_lian_xi_dian_hua", "boolfield_guo_ji_di_qu", "relatedfield_gender", "boolfield_zheng_jian_lei_xing", "boolfield_yu_chu_xian_ren_guan_xi", )}), 
        ("人身险理赔申请书审核单", {"fields": ("boolfield_tui_dan_yuan_yin", "boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu", )}), 
        ("理赔对账单", {"fields": ("characterfield_age", "boolfield_xu_hao", "boolfield_bao_dan_hao", "boolfield_bao_an_ren_lian_xi_dian_hua", "boolfield_chu_xian_ren_xing_ming", "boolfield_chu_xian_di_dian", "boolfield_shi_gu_gai_kuo", "boolfield_bei_bao_xian_ren_zheng_jian_hao_ma", "boolfield_gui_shu_cheng_shi", "boolfield_yi_yuan_xin_xi", "boolfield_ji_bing_xin_xi", "boolfield_li_pei_fang_shi", "boolfield_bei_zhu", "boolfield_bao_an_ren", "boolfield_li_pei_jin_e_bao_xiao_jian_mian_jin_e", "boolfield_chu_xian_di_dian_shi_ji_bie", "boolfield_chu_xian_di_dian_sheng_ji_bie", "datetimefield_date_of_birth", "boolfield_bao_an_shi_jian", "boolfield_chu_xian_shi_jian", "relatedfield_gender", "boolfield_zheng_jian_lei_xing", )}), 
        ("理赔对账单审核单", {"fields": ("boolfield_li_pei_dui_zhang_dan_tui_dan_yuan_yin", "boolfield_qian_shu_que_ren", )}), 
        ("门诊服务记录单", {"fields": ("boolfield_fei_yong_he_ji", "relatedfield_symptom_list", "boolfield_zhen_duan", "boolfield_jian_cha_xiang_mu", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_fu_wu_xiang_mu", "boolfield_men_zhen_bing_li_fu_jian", )}), 
        ("门诊记录单审核单", {"fields": ("boolfield_men_zhen_ji_lu_dan_tui_dan_yuan_yin", "boolfield_li_pei_men_zhen_ji_lu_qian_shu", )}), 
        ("治疗费用汇总单", {"fields": ("boolfield_fei_yong_he_ji", "boolfield_fei_yong", "boolfield_bao_dan_wai_fu_wu_fei_yong", "boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu", "boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu", "boolfield_fei_yong_qing_dan_fu_jian", )}), 
        ("理赔费用汇总单审核", {"fields": ("boolfield_li_pei_fei_yong_hui_zong_dan_tui_dan_yuan_yin", "boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu", )}), ]
    autocomplete_fields = ["relatedfield_symptom_list", "boolfield_zhen_duan", "boolfield_jian_cha_xiang_mu", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_fu_wu_xiang_mu", ]
    radio_fields = {"boolfield_yu_chu_xian_ren_guan_xi": admin.VERTICAL, "boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu": admin.VERTICAL, "boolfield_qian_shu_que_ren": admin.VERTICAL, "boolfield_li_pei_men_zhen_ji_lu_qian_shu": admin.VERTICAL, "boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu": admin.VERTICAL, }
    readonly_fields = ["characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ]

admin.site.register(Li_pei_shen_qing_shu_shen_he, Li_pei_shen_qing_shu_shen_heAdmin)
clinic_site.register(Li_pei_shen_qing_shu_shen_he, Li_pei_shen_qing_shu_shen_heAdmin)

class Man_yi_du_diao_chaAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ),)}), 
        ("满意度调查表", {"fields": ("boolfield_you_dai_gai_jin_de_fu_wu", "boolfield_xi_wang_zeng_jia_de_fu_wu_xiang_mu", "boolfield_fu_wu_xiao_lv_ping_fen", "boolfield_yi_liao_fu_wu_ji_neng_xiang_mu_ping_fen", "boolfield_ping_tai_fu_wu_xiang_mu_ping_fen", "boolfield_fu_wu_liu_cheng_ping_fen", )}), ]
    radio_fields = {"boolfield_fu_wu_xiao_lv_ping_fen": admin.VERTICAL, "boolfield_yi_liao_fu_wu_ji_neng_xiang_mu_ping_fen": admin.VERTICAL, "boolfield_ping_tai_fu_wu_xiang_mu_ping_fen": admin.VERTICAL, "boolfield_fu_wu_liu_cheng_ping_fen": admin.VERTICAL, }
    readonly_fields = ["characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ]

admin.site.register(Man_yi_du_diao_cha, Man_yi_du_diao_chaAdmin)
clinic_site.register(Man_yi_du_diao_cha, Man_yi_du_diao_chaAdmin)

class Zhen_hou_sui_fangAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ),)}), 
        ("诊后回访单", {"fields": ("boolfield_cun_zai_de_wen_ti", "boolfield_nin_de_dan_xin_he_gu_lv", "boolfield_you_dai_gai_jin_de_fu_wu", "boolfield_nin_hai_xu_yao_de_fu_wu", "boolfield_deng_hou_qing_kuang", "boolfield_fu_wu_xiao_guo_ping_jia", )}), ]
    radio_fields = {"boolfield_deng_hou_qing_kuang": admin.VERTICAL, "boolfield_fu_wu_xiao_guo_ping_jia": admin.VERTICAL, }
    readonly_fields = ["characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ]

admin.site.register(Zhen_hou_sui_fang, Zhen_hou_sui_fangAdmin)
clinic_site.register(Zhen_hou_sui_fang, Zhen_hou_sui_fangAdmin)

class Zhen_jian_sui_fangAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ),)}), 
        ("诊间随访表", {"fields": ("boolfield_cun_zai_de_wen_ti", "boolfield_qi_ta_xu_qiu", "boolfield_nin_de_dan_xin_he_gu_lv", "boolfield_nin_xiang_yao_de_bang_zhu", "boolfield_zhi_liao_jian_gou_tong_qing_kuang", "boolfield_jie_dai_fu_wu", "boolfield_deng_hou_qing_kuang", "boolfield_fu_wu_xiao_guo_ping_jia", )}), ]
    radio_fields = {"boolfield_zhi_liao_jian_gou_tong_qing_kuang": admin.VERTICAL, "boolfield_jie_dai_fu_wu": admin.VERTICAL, "boolfield_deng_hou_qing_kuang": admin.VERTICAL, "boolfield_fu_wu_xiao_guo_ping_jia": admin.VERTICAL, }
    readonly_fields = ["characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ]

admin.site.register(Zhen_jian_sui_fang, Zhen_jian_sui_fangAdmin)
clinic_site.register(Zhen_jian_sui_fang, Zhen_jian_sui_fangAdmin)

class Men_zhen_ji_luAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": ((),)}), 
        ("门诊服务记录单", {"fields": ("boolfield_fei_yong_he_ji", "relatedfield_symptom_list", "boolfield_zhen_duan", "boolfield_jian_cha_xiang_mu", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_fu_wu_xiang_mu", "boolfield_men_zhen_bing_li_fu_jian", )}), 
        ("个人基本信息表", {"fields": ("characterfield_gender", "characterhssc_identification_number", "characterfield_name", "boolfield_xu_hao", "boolfield_bao_dan_hao", "boolfield_bao_xian_ze_ren", "boolfield_chang_zhu_di_zhi", "boolfield_lian_xi_dian_hua", "datetimefield_date_of_birth", "boolfield_bao_xian_you_xiao_qi", "boolfield_zheng_jian_lei_xing", )}), ]
    autocomplete_fields = ["relatedfield_symptom_list", "boolfield_zhen_duan", "boolfield_jian_cha_xiang_mu", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_fu_wu_xiang_mu", ]

admin.site.register(Men_zhen_ji_lu, Men_zhen_ji_luAdmin)
clinic_site.register(Men_zhen_ji_lu, Men_zhen_ji_luAdmin)

class Yu_yue_tong_zhiAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ),)}), 
        ("预约通知单", {"fields": ("boolfield_ji_gou_ming_cheng", "characterfield_contact_number", "characterfield_contact_address", "boolfield_jiu_zhen_yi_sheng", "boolfield_yu_yue_xu_hao", "datetimefield_ri_qi_shi_jian", "boolfield_jiu_zhen_ji_gou_ze_ren_ren", )}), ]
    autocomplete_fields = ["boolfield_jiu_zhen_ji_gou_ze_ren_ren", ]
    readonly_fields = ["characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ]

admin.site.register(Yu_yue_tong_zhi, Yu_yue_tong_zhiAdmin)
clinic_site.register(Yu_yue_tong_zhi, Yu_yue_tong_zhiAdmin)

class Fen_zhen_que_renAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ),)}), 
        ("到店确认表", {"fields": ("boolfield_fen_zhen_que_ren", "boolfield_shen_fen_zheng_jian_fu_jian", )}), 
        ("预约单", {"fields": ("boolfield_jiu_zhen_wen_ti", "boolfield_fu_jia_fu_wu_yao_qiu", "datetimefield_ri_qi_shi_jian", "boolfield_shi_yong_bao_xian_chan_pin", "boolfield_jiu_zhen_ji_gou_ze_ren_ren", )}), ]
    autocomplete_fields = ["boolfield_jiu_zhen_ji_gou_ze_ren_ren", ]
    radio_fields = {"boolfield_fen_zhen_que_ren": admin.VERTICAL, }
    readonly_fields = ["characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ]

admin.site.register(Fen_zhen_que_ren, Fen_zhen_que_renAdmin)
clinic_site.register(Fen_zhen_que_ren, Fen_zhen_que_renAdmin)

class Yu_yue_que_renAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ),)}), 
        ("接单确认表", {"fields": ("boolfield_qian_dao_que_ren", )}), 
        ("预约单", {"fields": ("boolfield_jiu_zhen_wen_ti", "boolfield_fu_jia_fu_wu_yao_qiu", "datetimefield_ri_qi_shi_jian", "boolfield_shi_yong_bao_xian_chan_pin", "boolfield_jiu_zhen_ji_gou_ze_ren_ren", )}), ]
    autocomplete_fields = ["boolfield_jiu_zhen_ji_gou_ze_ren_ren", ]
    radio_fields = {"boolfield_qian_dao_que_ren": admin.VERTICAL, }
    readonly_fields = ["characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ]

admin.site.register(Yu_yue_que_ren, Yu_yue_que_renAdmin)
clinic_site.register(Yu_yue_que_ren, Yu_yue_que_renAdmin)

class Yu_yue_an_paiAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ),)}), 
        ("预约单", {"fields": ("boolfield_jiu_zhen_wen_ti", "boolfield_fu_jia_fu_wu_yao_qiu", "datetimefield_ri_qi_shi_jian", "boolfield_shi_yong_bao_xian_chan_pin", "boolfield_jiu_zhen_ji_gou_ze_ren_ren", )}), ]
    autocomplete_fields = ["boolfield_jiu_zhen_ji_gou_ze_ren_ren", ]
    readonly_fields = ["characterfield_gender", "characterfield_name", "boolfield_chang_zhu_di_zhi", "datetimefield_date_of_birth", ]

admin.site.register(Yu_yue_an_pai, Yu_yue_an_paiAdmin)
clinic_site.register(Yu_yue_an_pai, Yu_yue_an_paiAdmin)

class Ji_gou_ji_ben_xin_xi_biaoAdmin(HsscFormAdmin):
    fieldssets = [
        ("机构基本信息表", {"fields": ("boolfield_ji_gou_bian_ma", "boolfield_ji_gou_ming_cheng", "boolfield_ji_gou_dai_ma", "boolfield_ji_gou_shu_xing", "boolfield_ji_gou_ceng_ji", "boolfield_suo_zai_hang_zheng_qu_hua_dai_ma", "boolfield_xing_zheng_qu_hua_gui_shu", "boolfield_fa_ding_fu_ze_ren", "characterfield_contact_number", "characterfield_contact_address", )}), ]
    search_fields = ["name", "pym", ]

admin.site.register(Ji_gou_ji_ben_xin_xi_biao, Ji_gou_ji_ben_xin_xi_biaoAdmin)
clinic_site.register(Ji_gou_ji_ben_xin_xi_biao, Ji_gou_ji_ben_xin_xi_biaoAdmin)

class Zhi_yuan_ji_ben_xin_xi_biaoAdmin(HsscFormAdmin):
    fieldssets = [
        ("职员基本信息表", {"fields": ("characterfield_practice_qualification", "characterfield_expertise", "characterfield_practice_time", "boolfield_zhi_yuan_bian_ma", "characterfield_contact_number", "characterhssc_identification_number", "characterfield_name", "relatedfield_affiliation", "relatedfield_service_role", )}), ]
    autocomplete_fields = ["relatedfield_affiliation", ]
    search_fields = ["name", "pym", ]

admin.site.register(Zhi_yuan_ji_ben_xin_xi_biao, Zhi_yuan_ji_ben_xin_xi_biaoAdmin)
clinic_site.register(Zhi_yuan_ji_ben_xin_xi_biao, Zhi_yuan_ji_ben_xin_xi_biaoAdmin)

class Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_chaAdmin(HsscFormAdmin):
    search_fields = ["name", "pym", ]

admin.site.register(Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_cha, Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_chaAdmin)
clinic_site.register(Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_cha, Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_diao_chaAdmin)

class She_bei_ji_ben_xin_xi_ji_luAdmin(HsscFormAdmin):
    fieldssets = [
        ("设备基本信息表", {"fields": ("boolfield_she_bei_bian_ma", "boolfield_sheng_chan_chang_jia", "boolfield_she_bei_fu_wu_dan_wei_hao_shi", "boolfield_she_bei_jian_xiu_zhou_qi", "boolfield_she_bei_shi_yong_cheng_ben", "boolfield_she_bei_ming_cheng", "characterfield_contact_number", "boolfield_she_bei_shi_yong_fu_wu_gong_neng", )}), ]
    autocomplete_fields = ["boolfield_she_bei_shi_yong_fu_wu_gong_neng", ]
    search_fields = ["name", "pym", ]

admin.site.register(She_bei_ji_ben_xin_xi_ji_lu, She_bei_ji_ben_xin_xi_ji_luAdmin)
clinic_site.register(She_bei_ji_ben_xin_xi_ji_lu, She_bei_ji_ben_xin_xi_ji_luAdmin)

class Gong_ying_shang_ji_ben_xin_xi_diao_chaAdmin(HsscFormAdmin):
    search_fields = ["name", "pym", ]

admin.site.register(Gong_ying_shang_ji_ben_xin_xi_diao_cha, Gong_ying_shang_ji_ben_xin_xi_diao_chaAdmin)
clinic_site.register(Gong_ying_shang_ji_ben_xin_xi_diao_cha, Gong_ying_shang_ji_ben_xin_xi_diao_chaAdmin)

class Yao_pin_ji_ben_xin_xi_biaoAdmin(HsscFormAdmin):
    search_fields = ["name", "pym", ]

admin.site.register(Yao_pin_ji_ben_xin_xi_biao, Yao_pin_ji_ben_xin_xi_biaoAdmin)
clinic_site.register(Yao_pin_ji_ben_xin_xi_biao, Yao_pin_ji_ben_xin_xi_biaoAdmin)

class Ju_min_ji_ben_xin_xi_diao_chaAdmin(HsscFormAdmin):
    fieldssets = [
        ("个人基本信息表", {"fields": ("characterfield_gender", "characterhssc_identification_number", "characterfield_name", "boolfield_xu_hao", "boolfield_bao_dan_hao", "boolfield_bao_xian_ze_ren", "boolfield_chang_zhu_di_zhi", "boolfield_lian_xi_dian_hua", "datetimefield_date_of_birth", "boolfield_bao_xian_you_xiao_qi", "boolfield_zheng_jian_lei_xing", )}), ]
    search_fields = ["name", "pym", ]

admin.site.register(Ju_min_ji_ben_xin_xi_diao_cha, Ju_min_ji_ben_xin_xi_diao_chaAdmin)
clinic_site.register(Ju_min_ji_ben_xin_xi_diao_cha, Ju_min_ji_ben_xin_xi_diao_chaAdmin)
