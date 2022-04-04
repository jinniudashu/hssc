from django.contrib import admin
from .models import *


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Satisfaction)
class SatisfactionAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Frequency)
class FrequencyAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(State_degree)
class State_degreeAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Comparative_expression)
class Comparative_expressionAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Sports_preference)
class Sports_preferenceAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Exercise_time)
class Exercise_timeAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Convenience)
class ConvenienceAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Family_relationship)
class Family_relationshipAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Normality)
class NormalityAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Dorsal_artery_pulsation)
class Dorsal_artery_pulsationAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Hearing)
class HearingAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Lips)
class LipsAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Dentition)
class DentitionAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Pharynx)
class PharynxAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Life_event)
class Life_eventAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Edema)
class EdemaAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Nationality)
class NationalityAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Marital_status)
class Marital_statusAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Occupational_status)
class Occupational_statusAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Medical_expenses_burden)
class Medical_expenses_burdenAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Type_of_residence)
class Type_of_residenceAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Blood_type)
class Blood_typeAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Chang_yong_zheng_zhuang)
class Chang_yong_zheng_zhuangAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Tang_niao_bing_zheng_zhuang)
class Tang_niao_bing_zheng_zhuangAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Xi_yan_qing_kuang)
class Xi_yan_qing_kuangAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Yin_jiu_qing_kuang)
class Yin_jiu_qing_kuangAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Qian_dao_que_ren)
class Qian_dao_que_renAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Shi_mian_qing_kuang)
class Shi_mian_qing_kuangAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Da_bian_qing_kuang)
class Da_bian_qing_kuangAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Ya_li_qing_kuang)
class Ya_li_qing_kuangAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Kong_qi_wu_ran_qing_kuang)
class Kong_qi_wu_ran_qing_kuangAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Zao_sheng_wu_ran_qing_kuang)
class Zao_sheng_wu_ran_qing_kuangAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Shi_pin_he_yin_shui_an_quan_qing_kuang)
class Shi_pin_he_yin_shui_an_quan_qing_kuangAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Yin_shi_gui_lv_qing_kuang)
class Yin_shi_gui_lv_qing_kuangAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Qi_ta_huan_jing_wu_ran_qing_kuang)
class Qi_ta_huan_jing_wu_ran_qing_kuangAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Ji_xu_shi_yong_qing_kuang)
class Ji_xu_shi_yong_qing_kuangAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Qian_yue_qing_kuang)
class Qian_yue_qing_kuangAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Man_bing_diao_cha)
class Man_bing_diao_chaAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Jian_kang_zi_wo_ping_jia)
class Jian_kang_zi_wo_ping_jiaAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Qian_yue_que_ren)
class Qian_yue_que_renAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Sui_fang_ping_gu)
class Sui_fang_ping_guAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Tong_ti)
class Tong_tiAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Niao_tang)
class Niao_tangAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]


@admin.register(Dan_bai_zhi)
class Dan_bai_zhiAdmin(admin.ModelAdmin):
    search_fields = ['value', 'pym']
    list_display = ["value"]
