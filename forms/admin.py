from django.contrib import admin
from .models import *

from hssc.site import clinic_site
from forms.forms import A6203_ModelForm

class HsscFormAdmin(admin.ModelAdmin):
    exclude = ('hssc_id','slug')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        base_form = A6203_ModelForm(prefix="base_form")
        extra_context['base_form'] = base_form
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )


class Z6205Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_affiliation", "relatedfield_service_role", ]
admin.site.register(Z6205, Z6205Admin)
clinic_site.register(Z6205, Z6205Admin)

class A3109Admin(HsscFormAdmin):
    pass
admin.site.register(A3109, A3109Admin)
clinic_site.register(A3109, A3109Admin)

class A3108Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_lips", "relatedfield_dentition", "relatedfield_pharynx", ]
admin.site.register(A3108, A3108Admin)
clinic_site.register(A3108, A3108Admin)

class T4502Admin(HsscFormAdmin):
    autocomplete_fields = ["T4502", ]
admin.site.register(T4502, T4502Admin)
clinic_site.register(T4502, T4502Admin)

class Ji_gou_ji_ben_xin_xi_biaoAdmin(HsscFormAdmin):
    pass
admin.site.register(Ji_gou_ji_ben_xin_xi_biao, Ji_gou_ji_ben_xin_xi_biaoAdmin)
clinic_site.register(Ji_gou_ji_ben_xin_xi_biao, Ji_gou_ji_ben_xin_xi_biaoAdmin)

class Wu_liu_gong_ying_shang_ji_ben_xin_xi_biaoAdmin(HsscFormAdmin):
    autocomplete_fields = ["boolfield_xin_yu_ping_ji", ]
admin.site.register(Wu_liu_gong_ying_shang_ji_ben_xin_xi_biao, Wu_liu_gong_ying_shang_ji_ben_xin_xi_biaoAdmin)
clinic_site.register(Wu_liu_gong_ying_shang_ji_ben_xin_xi_biao, Wu_liu_gong_ying_shang_ji_ben_xin_xi_biaoAdmin)

class Zhi_yuan_ji_ben_xin_xi_biaoAdmin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_affiliation", "relatedfield_service_role", ]
admin.site.register(Zhi_yuan_ji_ben_xin_xi_biao, Zhi_yuan_ji_ben_xin_xi_biaoAdmin)
clinic_site.register(Zhi_yuan_ji_ben_xin_xi_biao, Zhi_yuan_ji_ben_xin_xi_biaoAdmin)

class She_bei_ji_ben_xin_xi_biaoAdmin(HsscFormAdmin):
    autocomplete_fields = ["boolfield_she_bei_shi_yong_fu_wu_gong_neng", ]
admin.site.register(She_bei_ji_ben_xin_xi_biao, She_bei_ji_ben_xin_xi_biaoAdmin)
clinic_site.register(She_bei_ji_ben_xin_xi_biao, She_bei_ji_ben_xin_xi_biaoAdmin)

class Yong_yao_diao_cha_biaoAdmin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_drug_name", ]
admin.site.register(Yong_yao_diao_cha_biao, Yong_yao_diao_cha_biaoAdmin)
clinic_site.register(Yong_yao_diao_cha_biao, Yong_yao_diao_cha_biaoAdmin)

class T3003Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_left_foot", "relatedfield_right_foot", ]
admin.site.register(T3003, T3003Admin)
clinic_site.register(T3003, T3003Admin)

class T3002Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_fundus", ]
admin.site.register(T3002, T3002Admin)
clinic_site.register(T3002, T3002Admin)

class Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_biaoAdmin(HsscFormAdmin):
    autocomplete_fields = ["boolfield_xin_yu_ping_ji", ]
admin.site.register(Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_biao, Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_biaoAdmin)
clinic_site.register(Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_biao, Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_biaoAdmin)

class A6208Admin(HsscFormAdmin):
    pass
admin.site.register(A6208, A6208Admin)
clinic_site.register(A6208, A6208Admin)

class Z6233Admin(HsscFormAdmin):
    pass
admin.site.register(Z6233, Z6233Admin)
clinic_site.register(Z6233, Z6233Admin)

class Yao_pin_ji_ben_xin_xi_biaoAdmin(HsscFormAdmin):
    autocomplete_fields = ["boolfield_chu_fang_ji_liang_dan_wei", "boolfield_ru_ku_ji_liang_dan_wei", "boolfield_xiao_shou_ji_liang_dan_wei", "relatedfield_drug_name", "boolfield_yong_yao_tu_jing", "boolfield_yao_pin_fen_lei", ]
admin.site.register(Yao_pin_ji_ben_xin_xi_biao, Yao_pin_ji_ben_xin_xi_biaoAdmin)
clinic_site.register(Yao_pin_ji_ben_xin_xi_biao, Yao_pin_ji_ben_xin_xi_biaoAdmin)

class A5001Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_drug_name", "boolfield_yong_yao_tu_jing", ]
admin.site.register(A5001, A5001Admin)
clinic_site.register(A5001, A5001Admin)

class T4504Admin(HsscFormAdmin):
    autocomplete_fields = ["T4504", ]
admin.site.register(T4504, T4504Admin)
clinic_site.register(T4504, T4504Admin)

class Shu_ye_zhu_she_danAdmin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_drug_name", ]
admin.site.register(Shu_ye_zhu_she_dan, Shu_ye_zhu_she_danAdmin)
clinic_site.register(Shu_ye_zhu_she_dan, Shu_ye_zhu_she_danAdmin)

class A6219Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_symptom_list", "boolfield_tang_niao_bing_zheng_zhuang", ]
admin.site.register(A6219, A6219Admin)
clinic_site.register(A6219, A6219Admin)

class A6203Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_gender", "relatedfield_nationality", "relatedfield_marital_status", "relatedfield_education", "relatedfield_occupational_status", "relatedfield_medical_expenses_burden", "relatedfield_type_of_residence", "relatedfield_blood_type", "relatedfield_signed_family_doctor", "relatedfield_family_relationship", ]
admin.site.register(A6203, A6203Admin)
clinic_site.register(A6203, A6203Admin)

class A3001Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_athletic_ability", "relatedfield_left_ear_hearing", "relatedfield_right_ear_hearing", "relatedfield_lips", "relatedfield_dentition", "relatedfield_pharynx", "relatedfield_lower_extremity_edema", ]
admin.site.register(A3001, A3001Admin)
clinic_site.register(A3001, A3001Admin)

class A3101Admin(HsscFormAdmin):
    pass
admin.site.register(A3101, A3101Admin)
clinic_site.register(A3101, A3101Admin)

class A6501Admin(HsscFormAdmin):
    autocomplete_fields = ["boolfield_ze_ren_ren", ]
admin.site.register(A6501, A6501Admin)
clinic_site.register(A6501, A6501Admin)

class T4505Admin(HsscFormAdmin):
    pass
admin.site.register(T4505, T4505Admin)
clinic_site.register(T4505, T4505Admin)

class A6211Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_major_life", ]
admin.site.register(A6211, A6211Admin)
clinic_site.register(A6211, A6211Admin)

class A3502Admin(HsscFormAdmin):
    autocomplete_fields = ["boolfield_niao_tang", "boolfield_dan_bai_zhi", "boolfield_tong_ti", ]
admin.site.register(A3502, A3502Admin)
clinic_site.register(A3502, A3502Admin)

class T4501Admin(HsscFormAdmin):
    autocomplete_fields = ["T4501", ]
admin.site.register(T4501, T4501Admin)
clinic_site.register(T4501, T4501Admin)

class A6207Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_drug_name", ]
admin.site.register(A6207, A6207Admin)
clinic_site.register(A6207, A6207Admin)

class A6206Admin(HsscFormAdmin):
    autocomplete_fields = ["boolfield_wai_shang_xing_ji_bing", ]
admin.site.register(A6206, A6206Admin)
clinic_site.register(A6206, A6206Admin)

class A3103Admin(HsscFormAdmin):
    pass
admin.site.register(A3103, A3103Admin)
clinic_site.register(A3103, A3103Admin)

class A6215Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_are_you_satisfied_with_the_job_and_life", "relatedfield_are_you_satisfied_with_your_adaptability", ]
admin.site.register(A6215, A6215Admin)
clinic_site.register(A6215, A6215Admin)

class Z6201Admin(HsscFormAdmin):
    pass
admin.site.register(Z6201, Z6201Admin)
clinic_site.register(Z6201, Z6201Admin)

class T3404Admin(HsscFormAdmin):
    pass
admin.site.register(T3404, T3404Admin)
clinic_site.register(T3404, T3404Admin)

class A3110Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_left_ear_hearing", "relatedfield_right_ear_hearing", ]
admin.site.register(A3110, A3110Admin)
clinic_site.register(A3110, A3110Admin)

class A6216Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_is_the_living_environment_satisfactory", "relatedfield_is_the_transportation_convenient", ]
admin.site.register(A6216, A6216Admin)
clinic_site.register(A6216, A6216Admin)

class A6218Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_symptom_list", ]
admin.site.register(A6218, A6218Admin)
clinic_site.register(A6218, A6218Admin)

class A6205Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_name_of_operation", ]
admin.site.register(A6205, A6205Admin)
clinic_site.register(A6205, A6205Admin)

class A6214Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_own_health", "relatedfield_compared_to_last_year", "relatedfield_sports_preference", "relatedfield_exercise_time", "relatedfield_have_any_recent_symptoms_of_physical_discomfort", ]
admin.site.register(A6214, A6214Admin)
clinic_site.register(A6214, A6214Admin)

class Z6230Admin(HsscFormAdmin):
    pass
admin.site.register(Z6230, Z6230Admin)
clinic_site.register(Z6230, Z6230Admin)

class A3105Admin(HsscFormAdmin):
    pass
admin.site.register(A3105, A3105Admin)
clinic_site.register(A3105, A3105Admin)

class A6217Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_symptom_list", ]
admin.site.register(A6217, A6217Admin)
clinic_site.register(A6217, A6217Admin)

class T3405Admin(HsscFormAdmin):
    pass
admin.site.register(T3405, T3405Admin)
clinic_site.register(T3405, T3405Admin)

class A6202Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_symptom_list", ]
admin.site.register(A6202, A6202Admin)
clinic_site.register(A6202, A6202Admin)

class A6220Admin(HsscFormAdmin):
    autocomplete_fields = ["boolfield_yuan_wai_jian_kang_ping_gu", ]
admin.site.register(A6220, A6220Admin)
clinic_site.register(A6220, A6220Admin)

class A6212Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_drinking_frequency", "relatedfield_smoking_frequency", ]
admin.site.register(A6212, A6212Admin)
clinic_site.register(A6212, A6212Admin)

class T9001Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_disease_name", "relatedfield_yi_lou_zhen_duan", "relatedfield_pai_chu_zhen_duan", ]
admin.site.register(T9001, T9001Admin)
clinic_site.register(T9001, T9001Admin)

class A5002Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_drug_name", "relatedfield_disease_name", "boolfield_shi_fou_ji_xu_shi_yong", ]
admin.site.register(A5002, A5002Admin)
clinic_site.register(A5002, A5002Admin)

class Physical_examination_athletic_abilityAdmin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_athletic_ability", ]
admin.site.register(Physical_examination_athletic_ability, Physical_examination_athletic_abilityAdmin)
clinic_site.register(Physical_examination_athletic_ability, Physical_examination_athletic_abilityAdmin)

class A6213Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_personality_tendency", "boolfield_shi_mian_qing_kuang", "boolfield_sheng_huo_gong_zuo_ya_li_qing_kuang", ]
admin.site.register(A6213, A6213Admin)
clinic_site.register(A6213, A6213Admin)

class Z6261Admin(HsscFormAdmin):
    autocomplete_fields = ["boolfield_qian_yue_que_ren", "boolfield_ze_ren_ren", ]
admin.site.register(Z6261, Z6261Admin)
clinic_site.register(Z6261, Z6261Admin)

class A6201Admin(HsscFormAdmin):
    autocomplete_fields = ["relatedfield_symptom_list", "boolfield_chang_yong_zheng_zhuang", ]
admin.site.register(A6201, A6201Admin)
clinic_site.register(A6201, A6201Admin)

class A6502Admin(HsscFormAdmin):
    autocomplete_fields = ["boolfield_qian_dao_que_ren", ]
admin.site.register(A6502, A6502Admin)
clinic_site.register(A6502, A6502Admin)

class A6204Admin(HsscFormAdmin):
    autocomplete_fields = ["boolfield_ge_ren_bing_shi", ]
admin.site.register(A6204, A6204Admin)
clinic_site.register(A6204, A6204Admin)

class T6301Admin(HsscFormAdmin):
    autocomplete_fields = ["boolfield_yao_pin_dan_wei", "relatedfield_drug_name", "relatedfield_drinking_frequency", "relatedfield_smoking_frequency", "boolfield_tang_niao_bing_zheng_zhuang", ]
admin.site.register(T6301, T6301Admin)
clinic_site.register(T6301, T6301Admin)

class A6210Admin(HsscFormAdmin):
    autocomplete_fields = ["boolfield_yi_chuan_ji_bing", "boolfield_yi_chuan_bing_shi_cheng_yuan", ]
admin.site.register(A6210, A6210Admin)
clinic_site.register(A6210, A6210Admin)

class A6209Admin(HsscFormAdmin):
    autocomplete_fields = ["boolfield_jia_zu_xing_ji_bing", "boolfield_jia_zu_bing_shi_cheng_yuan", ]
admin.site.register(A6209, A6209Admin)
clinic_site.register(A6209, A6209Admin)
