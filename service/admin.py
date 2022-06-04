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
        # 把表单内容存入CustomerServiceLog
        _post_data = request.POST.copy()
        log = create_customer_service_log(_post_data, obj)
        print('把表单内容存入CustomerServiceLog, From service.admin.HsscFormAdmin.save_model, Added log:', log.__dict__)

        # 发送服务作业完成信号
        pid = obj.pid
        print('发送操作完成信号, From service.admin.HsscFormAdmin.save_model：', pid)
        operand_finished.send(sender=self, pid=pid, request=request)
        super().save_model(request, obj, form, change)

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

class Li_pei_shen_qing_shu_shen_heAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "datetimefield_date_of_birth", "boolfield_chang_zhu_di_zhi", ),)}), 
        ("人身险理赔申请书", {"fields": ("characterhssc_identification_number", "relatedfield_gender", "boolfield_zheng_jian_lei_xing", "boolfield_shen_qing_ren_xing_ming", "boolfield_yu_chu_xian_ren_guan_xi", "boolfield_zheng_jian_you_xiao_qi", "boolfield_guo_ji_di_qu", "boolfield_hang_ye", "boolfield_zhi_ye", "boolfield_chang_zhu_di_zhi", "boolfield_lian_xi_dian_hua", )}), 
        ("签署确认单", {"fields": ("boolfield_qian_shu_que_ren", "boolfield_tui_dan_yuan_yin", )}), ]
    radio_fields = {"boolfield_yu_chu_xian_ren_guan_xi": admin.VERTICAL, "boolfield_qian_shu_que_ren": admin.VERTICAL, }
    readonly_fields = ["characterfield_name", "characterfield_gender", "datetimefield_date_of_birth", "boolfield_chang_zhu_di_zhi", ]

admin.site.register(Li_pei_shen_qing_shu_shen_he, Li_pei_shen_qing_shu_shen_heAdmin)
clinic_site.register(Li_pei_shen_qing_shu_shen_he, Li_pei_shen_qing_shu_shen_heAdmin)

class Li_pei_dui_zhang_dan_shen_heAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "datetimefield_date_of_birth", "boolfield_chang_zhu_di_zhi", ),)}), 
        ("签署确认单", {"fields": ("boolfield_qian_shu_que_ren", "boolfield_tui_dan_yuan_yin", )}), 
        ("理赔对账单", {"fields": ("characterfield_age", "datetimefield_date_of_birth", "relatedfield_gender", "boolfield_zheng_jian_lei_xing", "boolfield_xu_hao", "boolfield_bao_dan_hao", "boolfield_bao_an_shi_jian", "boolfield_chu_xian_shi_jian", "boolfield_bao_an_ren_lian_xi_dian_hua", "boolfield_chu_xian_ren_xing_ming", "boolfield_chu_xian_di_dian", "boolfield_chu_xian_di_dian_sheng_ji_bie", "boolfield_chu_xian_di_dian_shi_ji_bie", "boolfield_shi_gu_gai_kuo", "boolfield_bei_bao_xian_ren_zheng_jian_hao_ma", "boolfield_gui_shu_cheng_shi", "boolfield_yi_yuan_xin_xi", "boolfield_ji_bing_xin_xi", "boolfield_li_pei_jin_e_bao_xiao_jian_mian_jin_e", "boolfield_li_pei_fang_shi", "boolfield_bei_zhu", "boolfield_bao_an_ren", )}), ]
    radio_fields = {"boolfield_qian_shu_que_ren": admin.VERTICAL, }
    readonly_fields = ["characterfield_name", "characterfield_gender", "datetimefield_date_of_birth", "boolfield_chang_zhu_di_zhi", ]

admin.site.register(Li_pei_dui_zhang_dan_shen_he, Li_pei_dui_zhang_dan_shen_heAdmin)
clinic_site.register(Li_pei_dui_zhang_dan_shen_he, Li_pei_dui_zhang_dan_shen_heAdmin)

class Li_pei_men_zhen_ji_lu_shen_heAdmin(HsscFormAdmin):
    fieldssets = [
        ("设备基本信息表", {"fields": ("boolfield_she_bei_bian_ma", "boolfield_sheng_chan_chang_jia", "boolfield_she_bei_fu_wu_dan_wei_hao_shi", "boolfield_she_bei_jian_xiu_zhou_qi", "boolfield_she_bei_shi_yong_cheng_ben", "boolfield_she_bei_ming_cheng", "characterfield_contact_number", "boolfield_she_bei_shi_yong_fu_wu_gong_neng", )}), 
        ("门诊服务记录单", {"fields": ("relatedfield_symptom_list", "boolfield_zhen_duan", "boolfield_jian_cha_xiang_mu", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_fu_wu_xiang_mu", "boolfield_fei_yong_he_ji", "boolfield_men_zhen_bing_li_fu_jian", )}), ]
    autocomplete_fields = ["boolfield_she_bei_shi_yong_fu_wu_gong_neng", "relatedfield_symptom_list", "boolfield_zhen_duan", "boolfield_jian_cha_xiang_mu", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_fu_wu_xiang_mu", ]
    search_fields = ["name", "pym", ]

admin.site.register(Li_pei_men_zhen_ji_lu_shen_he, Li_pei_men_zhen_ji_lu_shen_heAdmin)
clinic_site.register(Li_pei_men_zhen_ji_lu_shen_he, Li_pei_men_zhen_ji_lu_shen_heAdmin)

class Li_pei_fei_yong_hui_zong_dan_shen_heAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "datetimefield_date_of_birth", "boolfield_chang_zhu_di_zhi", ),)}), 
        ("治疗费用汇总单", {"fields": ("boolfield_fei_yong_he_ji", "boolfield_bao_dan_nei_fu_wu_shou_fei_xiang_mu", "boolfield_bao_dan_wai_fu_wu_shou_fei_xiang_mu", "boolfield_fei_yong", "boolfield_bao_dan_wai_fu_wu_fei_yong", "boolfield_fei_yong_qing_dan_fu_jian", )}), 
        ("签署确认单", {"fields": ("boolfield_qian_shu_que_ren", "boolfield_tui_dan_yuan_yin", )}), ]
    radio_fields = {"boolfield_qian_shu_que_ren": admin.VERTICAL, }
    readonly_fields = ["characterfield_name", "characterfield_gender", "datetimefield_date_of_birth", "boolfield_chang_zhu_di_zhi", ]

admin.site.register(Li_pei_fei_yong_hui_zong_dan_shen_he, Li_pei_fei_yong_hui_zong_dan_shen_heAdmin)
clinic_site.register(Li_pei_fei_yong_hui_zong_dan_shen_he, Li_pei_fei_yong_hui_zong_dan_shen_heAdmin)

class Man_yi_du_diao_chaAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "datetimefield_date_of_birth", "boolfield_chang_zhu_di_zhi", ),)}), 
        ("满意度调查表", {"fields": ("boolfield_you_dai_gai_jin_de_fu_wu", "boolfield_yi_liao_fu_wu_ji_neng_xiang_mu_ping_fen", "boolfield_ping_tai_fu_wu_xiang_mu_ping_fen", "boolfield_xi_wang_zeng_jia_de_fu_wu_xiang_mu", "boolfield_fu_wu_xiao_lv_ping_fen", "boolfield_fu_wu_liu_cheng_ping_fen", )}), ]
    radio_fields = {"boolfield_yi_liao_fu_wu_ji_neng_xiang_mu_ping_fen": admin.VERTICAL, "boolfield_ping_tai_fu_wu_xiang_mu_ping_fen": admin.VERTICAL, "boolfield_fu_wu_xiao_lv_ping_fen": admin.VERTICAL, "boolfield_fu_wu_liu_cheng_ping_fen": admin.VERTICAL, }
    readonly_fields = ["characterfield_name", "characterfield_gender", "datetimefield_date_of_birth", "boolfield_chang_zhu_di_zhi", ]

admin.site.register(Man_yi_du_diao_cha, Man_yi_du_diao_chaAdmin)
clinic_site.register(Man_yi_du_diao_cha, Man_yi_du_diao_chaAdmin)

class Zhen_hou_sui_fangAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "datetimefield_date_of_birth", "boolfield_chang_zhu_di_zhi", ),)}), 
        ("诊后回访单", {"fields": ("boolfield_deng_hou_qing_kuang", "boolfield_cun_zai_de_wen_ti", "boolfield_nin_de_dan_xin_he_gu_lv", "boolfield_fu_wu_xiao_guo_ping_jia", "boolfield_you_dai_gai_jin_de_fu_wu", "boolfield_nin_hai_xu_yao_de_fu_wu", )}), ]
    radio_fields = {"boolfield_deng_hou_qing_kuang": admin.VERTICAL, "boolfield_fu_wu_xiao_guo_ping_jia": admin.VERTICAL, }
    readonly_fields = ["characterfield_name", "characterfield_gender", "datetimefield_date_of_birth", "boolfield_chang_zhu_di_zhi", ]

admin.site.register(Zhen_hou_sui_fang, Zhen_hou_sui_fangAdmin)
clinic_site.register(Zhen_hou_sui_fang, Zhen_hou_sui_fangAdmin)

class Zhen_jian_sui_fangAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "datetimefield_date_of_birth", "boolfield_chang_zhu_di_zhi", ),)}), 
        ("诊间随访表", {"fields": ("boolfield_zhi_liao_jian_gou_tong_qing_kuang", "boolfield_deng_hou_qing_kuang", "boolfield_jie_dai_fu_wu", "boolfield_cun_zai_de_wen_ti", "boolfield_qi_ta_xu_qiu", "boolfield_nin_de_dan_xin_he_gu_lv", "boolfield_nin_xiang_yao_de_bang_zhu", "boolfield_fu_wu_xiao_guo_ping_jia", )}), ]
    radio_fields = {"boolfield_zhi_liao_jian_gou_tong_qing_kuang": admin.VERTICAL, "boolfield_deng_hou_qing_kuang": admin.VERTICAL, "boolfield_jie_dai_fu_wu": admin.VERTICAL, "boolfield_fu_wu_xiao_guo_ping_jia": admin.VERTICAL, }
    readonly_fields = ["characterfield_name", "characterfield_gender", "datetimefield_date_of_birth", "boolfield_chang_zhu_di_zhi", ]

admin.site.register(Zhen_jian_sui_fang, Zhen_jian_sui_fangAdmin)
clinic_site.register(Zhen_jian_sui_fang, Zhen_jian_sui_fangAdmin)

class Men_zhen_ji_luAdmin(HsscFormAdmin):
    fieldssets = [
        ("门诊服务记录单", {"fields": ("relatedfield_symptom_list", "boolfield_zhen_duan", "boolfield_jian_cha_xiang_mu", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_fu_wu_xiang_mu", "boolfield_fei_yong_he_ji", "boolfield_men_zhen_bing_li_fu_jian", )}), 
        ("被保个人基本信息表", {"fields": ("characterhssc_identification_number", "characterfield_name", "characterfield_gender", "datetimefield_date_of_birth", "boolfield_bao_xian_you_xiao_qi", "boolfield_zheng_jian_lei_xing", "boolfield_xu_hao", "boolfield_bao_dan_hao", "boolfield_bao_xian_ze_ren", "boolfield_chang_zhu_di_zhi", "boolfield_lian_xi_dian_hua", )}), ]
    autocomplete_fields = ["relatedfield_symptom_list", "boolfield_zhen_duan", "boolfield_jian_cha_xiang_mu", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_fu_wu_xiang_mu", ]
    search_fields = ["name", "pym", ]

admin.site.register(Men_zhen_ji_lu, Men_zhen_ji_luAdmin)
clinic_site.register(Men_zhen_ji_lu, Men_zhen_ji_luAdmin)

class Yu_yue_tong_zhiAdmin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "datetimefield_date_of_birth", "boolfield_chang_zhu_di_zhi", ),)}), 
        ("预约通知单", {"fields": ("characterfield_contact_address", "characterfield_contact_number", "datetimefield_ri_qi_shi_jian", "boolfield_ze_ren_ren", "boolfield_jiu_zhen_yi_sheng", "boolfield_yu_yue_xu_hao", )}), ]
    autocomplete_fields = ["boolfield_ze_ren_ren", ]
    readonly_fields = ["characterfield_name", "characterfield_gender", "datetimefield_date_of_birth", "boolfield_chang_zhu_di_zhi", ]

admin.site.register(Yu_yue_tong_zhi, Yu_yue_tong_zhiAdmin)
clinic_site.register(Yu_yue_tong_zhi, Yu_yue_tong_zhiAdmin)

class Fen_zhen_que_renAdmin(HsscFormAdmin):
    fieldssets = [
        ("预约申请单", {"fields": ("datetimefield_ri_qi_shi_jian", "boolfield_ze_ren_ren", "boolfield_jiu_zhen_wen_ti", "boolfield_shi_yong_bao_xian_chan_pin", "boolfield_fu_jia_fu_wu_yao_qiu", )}), 
        ("被保个人基本信息表", {"fields": ("characterhssc_identification_number", "characterfield_name", "characterfield_gender", "datetimefield_date_of_birth", "boolfield_bao_xian_you_xiao_qi", "boolfield_zheng_jian_lei_xing", "boolfield_xu_hao", "boolfield_bao_dan_hao", "boolfield_bao_xian_ze_ren", "boolfield_chang_zhu_di_zhi", "boolfield_lian_xi_dian_hua", )}), 
        ("到店确认表", {"fields": ("boolfield_fen_zhen_que_ren", "boolfield_shen_fen_zheng_jian_fu_jian", )}), ]
    autocomplete_fields = ["boolfield_ze_ren_ren", ]
    radio_fields = {"boolfield_fen_zhen_que_ren": admin.VERTICAL, }
    search_fields = ["name", "pym", ]

admin.site.register(Fen_zhen_que_ren, Fen_zhen_que_renAdmin)
clinic_site.register(Fen_zhen_que_ren, Fen_zhen_que_renAdmin)

class Yu_yue_que_renAdmin(HsscFormAdmin):
    fieldssets = [
        ("接单确认表", {"fields": ("boolfield_qian_dao_que_ren", )}), 
        ("预约申请单", {"fields": ("datetimefield_ri_qi_shi_jian", "boolfield_ze_ren_ren", "boolfield_jiu_zhen_wen_ti", "boolfield_shi_yong_bao_xian_chan_pin", "boolfield_fu_jia_fu_wu_yao_qiu", )}), 
        ("被保个人基本信息表", {"fields": ("characterhssc_identification_number", "characterfield_name", "characterfield_gender", "datetimefield_date_of_birth", "boolfield_bao_xian_you_xiao_qi", "boolfield_zheng_jian_lei_xing", "boolfield_xu_hao", "boolfield_bao_dan_hao", "boolfield_bao_xian_ze_ren", "boolfield_chang_zhu_di_zhi", "boolfield_lian_xi_dian_hua", )}), ]
    autocomplete_fields = ["boolfield_ze_ren_ren", ]
    radio_fields = {"boolfield_qian_dao_que_ren": admin.VERTICAL, }
    search_fields = ["name", "pym", ]

admin.site.register(Yu_yue_que_ren, Yu_yue_que_renAdmin)
clinic_site.register(Yu_yue_que_ren, Yu_yue_que_renAdmin)

class Yu_yue_an_paiAdmin(HsscFormAdmin):
    fieldssets = [
        ("预约申请单", {"fields": ("datetimefield_ri_qi_shi_jian", "boolfield_ze_ren_ren", "boolfield_jiu_zhen_wen_ti", "boolfield_shi_yong_bao_xian_chan_pin", "boolfield_fu_jia_fu_wu_yao_qiu", )}), 
        ("被保个人基本信息表", {"fields": ("characterhssc_identification_number", "characterfield_name", "characterfield_gender", "datetimefield_date_of_birth", "boolfield_bao_xian_you_xiao_qi", "boolfield_zheng_jian_lei_xing", "boolfield_xu_hao", "boolfield_bao_dan_hao", "boolfield_bao_xian_ze_ren", "boolfield_chang_zhu_di_zhi", "boolfield_lian_xi_dian_hua", )}), ]
    autocomplete_fields = ["boolfield_ze_ren_ren", ]
    search_fields = ["name", "pym", ]

admin.site.register(Yu_yue_an_pai, Yu_yue_an_paiAdmin)
clinic_site.register(Yu_yue_an_pai, Yu_yue_an_paiAdmin)

class Ji_gou_ji_ben_xin_xi_biaoAdmin(HsscFormAdmin):
    fieldssets = [
        ("机构基本信息表", {"fields": ("characterfield_contact_address", "boolfield_ji_gou_bian_ma", "boolfield_ji_gou_ming_cheng", "boolfield_ji_gou_dai_ma", "boolfield_ji_gou_shu_xing", "boolfield_ji_gou_ceng_ji", "boolfield_suo_zai_hang_zheng_qu_hua_dai_ma", "boolfield_xing_zheng_qu_hua_gui_shu", "boolfield_fa_ding_fu_ze_ren", "characterfield_contact_number", )}), ]
    search_fields = ["name", "pym", ]

admin.site.register(Ji_gou_ji_ben_xin_xi_biao, Ji_gou_ji_ben_xin_xi_biaoAdmin)
clinic_site.register(Ji_gou_ji_ben_xin_xi_biao, Ji_gou_ji_ben_xin_xi_biaoAdmin)

class Zhi_yuan_ji_ben_xin_xi_biaoAdmin(HsscFormAdmin):
    fieldssets = [
        ("职员基本信息表", {"fields": ("characterhssc_identification_number", "characterfield_practice_qualification", "characterfield_expertise", "characterfield_practice_time", "boolfield_zhi_yuan_bian_ma", "characterfield_contact_number", "characterfield_name", "relatedfield_affiliation", "relatedfield_service_role", )}), ]
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
        ("被保个人基本信息表", {"fields": ("characterhssc_identification_number", "characterfield_name", "characterfield_gender", "datetimefield_date_of_birth", "boolfield_bao_xian_you_xiao_qi", "boolfield_zheng_jian_lei_xing", "boolfield_xu_hao", "boolfield_bao_dan_hao", "boolfield_bao_xian_ze_ren", "boolfield_chang_zhu_di_zhi", "boolfield_lian_xi_dian_hua", )}), ]
    search_fields = ["name", "pym", ]

admin.site.register(Ju_min_ji_ben_xin_xi_diao_cha, Ju_min_ji_ben_xin_xi_diao_chaAdmin)
clinic_site.register(Ju_min_ji_ben_xin_xi_diao_cha, Ju_min_ji_ben_xin_xi_diao_chaAdmin)

class A6401Admin(HsscFormAdmin):
    fieldssets = [
        ("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "datetimefield_date_of_birth", "boolfield_chang_zhu_di_zhi", ),)}), 
        ("预约申请单", {"fields": ("datetimefield_ri_qi_shi_jian", "boolfield_ze_ren_ren", "boolfield_jiu_zhen_wen_ti", "boolfield_shi_yong_bao_xian_chan_pin", "boolfield_fu_jia_fu_wu_yao_qiu", )}), ]
    autocomplete_fields = ["boolfield_ze_ren_ren", ]
    readonly_fields = ["characterfield_name", "characterfield_gender", "datetimefield_date_of_birth", "boolfield_chang_zhu_di_zhi", ]

admin.site.register(A6401, A6401Admin)
clinic_site.register(A6401, A6401Admin)
