from django.contrib import admin
from core.admin import clinic_site
from .models import *



@admin.register(An_pai_que_ren)
class An_pai_que_renAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(An_pai_que_ren, An_pai_que_renAdmin)


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Character, CharacterAdmin)


@admin.register(Satisfaction)
class SatisfactionAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Satisfaction, SatisfactionAdmin)


@admin.register(Frequency)
class FrequencyAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Frequency, FrequencyAdmin)


@admin.register(State_degree)
class State_degreeAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(State_degree, State_degreeAdmin)


@admin.register(Comparative_expression)
class Comparative_expressionAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Comparative_expression, Comparative_expressionAdmin)


@admin.register(Sports_preference)
class Sports_preferenceAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Sports_preference, Sports_preferenceAdmin)


@admin.register(Exercise_time)
class Exercise_timeAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Exercise_time, Exercise_timeAdmin)


@admin.register(Convenience)
class ConvenienceAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Convenience, ConvenienceAdmin)


@admin.register(Family_relationship)
class Family_relationshipAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Family_relationship, Family_relationshipAdmin)


@admin.register(Normality)
class NormalityAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Normality, NormalityAdmin)


@admin.register(Dorsal_artery_pulsation)
class Dorsal_artery_pulsationAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Dorsal_artery_pulsation, Dorsal_artery_pulsationAdmin)


@admin.register(Pharynx)
class PharynxAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Pharynx, PharynxAdmin)


@admin.register(Edema)
class EdemaAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Edema, EdemaAdmin)


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Gender, GenderAdmin)


@admin.register(Nationality)
class NationalityAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Nationality, NationalityAdmin)


@admin.register(Marital_status)
class Marital_statusAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Marital_status, Marital_statusAdmin)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Education, EducationAdmin)


@admin.register(Occupational_status)
class Occupational_statusAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Occupational_status, Occupational_statusAdmin)


@admin.register(Medical_expenses_burden)
class Medical_expenses_burdenAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Medical_expenses_burden, Medical_expenses_burdenAdmin)


@admin.register(Type_of_residence)
class Type_of_residenceAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Type_of_residence, Type_of_residenceAdmin)


@admin.register(Blood_type)
class Blood_typeAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Blood_type, Blood_typeAdmin)


@admin.register(Chang_yong_zheng_zhuang)
class Chang_yong_zheng_zhuangAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Chang_yong_zheng_zhuang, Chang_yong_zheng_zhuangAdmin)


@admin.register(Tang_niao_bing_zheng_zhuang)
class Tang_niao_bing_zheng_zhuangAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Tang_niao_bing_zheng_zhuang, Tang_niao_bing_zheng_zhuangAdmin)


@admin.register(Qian_dao_que_ren)
class Qian_dao_que_renAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Qian_dao_que_ren, Qian_dao_que_renAdmin)


@admin.register(Shi_mian_qing_kuang)
class Shi_mian_qing_kuangAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Shi_mian_qing_kuang, Shi_mian_qing_kuangAdmin)


@admin.register(Ya_li_qing_kuang)
class Ya_li_qing_kuangAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Ya_li_qing_kuang, Ya_li_qing_kuangAdmin)


@admin.register(Ji_xu_shi_yong_qing_kuang)
class Ji_xu_shi_yong_qing_kuangAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Ji_xu_shi_yong_qing_kuang, Ji_xu_shi_yong_qing_kuangAdmin)


@admin.register(Qian_yue_que_ren)
class Qian_yue_que_renAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Qian_yue_que_ren, Qian_yue_que_renAdmin)


@admin.register(Sui_fang_ping_gu)
class Sui_fang_ping_guAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Sui_fang_ping_gu, Sui_fang_ping_guAdmin)


@admin.register(Tong_ti)
class Tong_tiAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Tong_ti, Tong_tiAdmin)


@admin.register(Niao_tang)
class Niao_tangAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Niao_tang, Niao_tangAdmin)


@admin.register(Dan_bai_zhi)
class Dan_bai_zhiAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Dan_bai_zhi, Dan_bai_zhiAdmin)


@admin.register(Yong_yao_tu_jing)
class Yong_yao_tu_jingAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Yong_yao_tu_jing, Yong_yao_tu_jingAdmin)


@admin.register(Xin_yu_ping_ji)
class Xin_yu_ping_jiAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Xin_yu_ping_ji, Xin_yu_ping_jiAdmin)


@admin.register(Yao_pin_dan_wei)
class Yao_pin_dan_weiAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Yao_pin_dan_wei, Yao_pin_dan_weiAdmin)


@admin.register(Yao_pin_fen_lei)
class Yao_pin_fen_leiAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Yao_pin_fen_lei, Yao_pin_fen_leiAdmin)


@admin.register(Fu_wu_jue_se)
class Fu_wu_jue_seAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Fu_wu_jue_se, Fu_wu_jue_seAdmin)


@admin.register(Qin_shu_guan_xi)
class Qin_shu_guan_xiAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Qin_shu_guan_xi, Qin_shu_guan_xiAdmin)


@admin.register(Tang_niao_bing_kong_zhi_xiao_guo_ping_gu)
class Tang_niao_bing_kong_zhi_xiao_guo_ping_guAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Tang_niao_bing_kong_zhi_xiao_guo_ping_gu, Tang_niao_bing_kong_zhi_xiao_guo_ping_guAdmin)


@admin.register(Deng_hou_shi_jian)
class Deng_hou_shi_jianAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Deng_hou_shi_jian, Deng_hou_shi_jianAdmin)


@admin.register(Fu_wu_xiao_guo_ping_jia)
class Fu_wu_xiao_guo_ping_jiaAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Fu_wu_xiao_guo_ping_jia, Fu_wu_xiao_guo_ping_jiaAdmin)


@admin.register(Ping_fen)
class Ping_fenAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Ping_fen, Ping_fenAdmin)


@admin.register(Nin_cong_he_chu_zhi_dao_wo_men)
class Nin_cong_he_chu_zhi_dao_wo_menAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Nin_cong_he_chu_zhi_dao_wo_men, Nin_cong_he_chu_zhi_dao_wo_menAdmin)


@admin.register(Shi_fou_yuan_yi_xiang_jia_ren_peng_you_tui_jian_wo_men_de_fu_wu)
class Shi_fou_yuan_yi_xiang_jia_ren_peng_you_tui_jian_wo_men_de_fu_wuAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]

clinic_site.register(Shi_fou_yuan_yi_xiang_jia_ren_peng_you_tui_jian_wo_men_de_fu_wu, Shi_fou_yuan_yi_xiang_jia_ren_peng_you_tui_jian_wo_men_de_fu_wuAdmin)
