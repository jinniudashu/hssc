from django.contrib import admin
from .models import *


class A6207Admin(admin.ModelAdmin):
        autocomplete_fields = ["relatedfield_drug_name", ]

admin.site.register(A6207, A6207Admin)

class T4501Admin(admin.ModelAdmin):
        autocomplete_fields = ["T4501", ]

admin.site.register(T4501, T4501Admin)

class A6206Admin(admin.ModelAdmin):
        autocomplete_fields = ["boolfield_wai_shang_xing_ji_bing", ]

admin.site.register(A6206, A6206Admin)

class A3103Admin(admin.ModelAdmin):
    pass
admin.site.register(A3103, A3103Admin)

class A6215Admin(admin.ModelAdmin):
    pass
admin.site.register(A6215, A6215Admin)

class Z6201Admin(admin.ModelAdmin):
    pass
admin.site.register(Z6201, Z6201Admin)

class T3404Admin(admin.ModelAdmin):
    pass
admin.site.register(T3404, T3404Admin)

class A3110Admin(admin.ModelAdmin):
    pass
admin.site.register(A3110, A3110Admin)

class A6216Admin(admin.ModelAdmin):
    pass
admin.site.register(A6216, A6216Admin)

class A3105Admin(admin.ModelAdmin):
    pass
admin.site.register(A3105, A3105Admin)

class A6217Admin(admin.ModelAdmin):
        autocomplete_fields = ["relatedfield_symptom_list", ]

admin.site.register(A6217, A6217Admin)

class T3405Admin(admin.ModelAdmin):
    pass
admin.site.register(T3405, T3405Admin)

class A6202Admin(admin.ModelAdmin):
        autocomplete_fields = ["relatedfield_symptom_list", ]

admin.site.register(A6202, A6202Admin)

class A6201Admin(admin.ModelAdmin):
        autocomplete_fields = ["relatedfield_symptom_list", ]

admin.site.register(A6201, A6201Admin)

class A6204Admin(admin.ModelAdmin):
        autocomplete_fields = ["boolfield_ge_ren_bing_shi", ]

admin.site.register(A6204, A6204Admin)

class T6301Admin(admin.ModelAdmin):
        radio_fields = {"relatedfield_drinking_frequency": admin.VERTICAL, "relatedfield_smoking_frequency": admin.VERTICAL, }
    autocomplete_fields = ["relatedfield_drug_name", ]

admin.site.register(T6301, T6301Admin)

class Fu_wuAdmin(admin.ModelAdmin):
        autocomplete_fields = ["boolfield_ze_ren_ren", "boolfield_fu_wu_xiang_mu_ming_cheng", ]

admin.site.register(Fu_wu, Fu_wuAdmin)

class Wu_liu_gong_ying_shang_ji_ben_xin_xi_biaoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Wu_liu_gong_ying_shang_ji_ben_xin_xi_biao, Wu_liu_gong_ying_shang_ji_ben_xin_xi_biaoAdmin)

class Yao_pin_ji_ben_xin_xi_biaoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Yao_pin_ji_ben_xin_xi_biao, Yao_pin_ji_ben_xin_xi_biaoAdmin)

class Z6205Admin(admin.ModelAdmin):
        autocomplete_fields = ["relatedfield_affiliation", ]

admin.site.register(Z6205, Z6205Admin)

class A3109Admin(admin.ModelAdmin):
    pass
admin.site.register(A3109, A3109Admin)

class A3108Admin(admin.ModelAdmin):
        radio_fields = {"relatedfield_lips": admin.VERTICAL, "relatedfield_dentition": admin.VERTICAL, }

admin.site.register(A3108, A3108Admin)

class T4502Admin(admin.ModelAdmin):
        autocomplete_fields = ["T4502", ]

admin.site.register(T4502, T4502Admin)

class Ji_gou_ji_ben_xin_xi_biaoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Ji_gou_ji_ben_xin_xi_biao, Ji_gou_ji_ben_xin_xi_biaoAdmin)

class Zhi_yuan_ji_ben_xin_xi_biaoAdmin(admin.ModelAdmin):
        autocomplete_fields = ["relatedfield_affiliation", ]

admin.site.register(Zhi_yuan_ji_ben_xin_xi_biao, Zhi_yuan_ji_ben_xin_xi_biaoAdmin)

class She_bei_ji_ben_xin_xi_biaoAdmin(admin.ModelAdmin):
        autocomplete_fields = ["boolfield_she_bei_shi_yong_fu_wu_gong_neng", ]

admin.site.register(She_bei_ji_ben_xin_xi_biao, She_bei_ji_ben_xin_xi_biaoAdmin)

class Yong_yao_diao_cha_biaoAdmin(admin.ModelAdmin):
        autocomplete_fields = ["relatedfield_drug_name", ]

admin.site.register(Yong_yao_diao_cha_biao, Yong_yao_diao_cha_biaoAdmin)

class T3003Admin(admin.ModelAdmin):
        radio_fields = {"relatedfield_left_foot": admin.VERTICAL, "relatedfield_right_foot": admin.VERTICAL, }

admin.site.register(T3003, T3003Admin)

class T3002Admin(admin.ModelAdmin):
    pass
admin.site.register(T3002, T3002Admin)

class Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_biaoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_biao, Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_biaoAdmin)

class A6208Admin(admin.ModelAdmin):
    pass
admin.site.register(A6208, A6208Admin)

class Z6233Admin(admin.ModelAdmin):
    pass
admin.site.register(Z6233, Z6233Admin)

class A5001Admin(admin.ModelAdmin):
        autocomplete_fields = ["relatedfield_drug_name", ]

admin.site.register(A5001, A5001Admin)

class T4504Admin(admin.ModelAdmin):
        autocomplete_fields = ["T4504", ]

admin.site.register(T4504, T4504Admin)

class Shu_ye_zhu_she_danAdmin(admin.ModelAdmin):
        autocomplete_fields = ["relatedfield_drug_name", ]

admin.site.register(Shu_ye_zhu_she_dan, Shu_ye_zhu_she_danAdmin)

class A6219Admin(admin.ModelAdmin):
        autocomplete_fields = ["relatedfield_symptom_list", ]

admin.site.register(A6219, A6219Admin)

class A6203Admin(admin.ModelAdmin):
        autocomplete_fields = ["relatedfield_signed_family_doctor", ]

admin.site.register(A6203, A6203Admin)

class A3001Admin(admin.ModelAdmin):
        radio_fields = {"relatedfield_lips": admin.VERTICAL, "relatedfield_dentition": admin.VERTICAL, "relatedfield_lower_extremity_edema": admin.VERTICAL, }

admin.site.register(A3001, A3001Admin)

class A3101Admin(admin.ModelAdmin):
    pass
admin.site.register(A3101, A3101Admin)

class A6501Admin(admin.ModelAdmin):
        autocomplete_fields = ["boolfield_ze_ren_ren", ]

admin.site.register(A6501, A6501Admin)

class T4505Admin(admin.ModelAdmin):
    pass
admin.site.register(T4505, T4505Admin)

class A6211Admin(admin.ModelAdmin):
    pass
admin.site.register(A6211, A6211Admin)

class A3502Admin(admin.ModelAdmin):
    pass
admin.site.register(A3502, A3502Admin)

class A6218Admin(admin.ModelAdmin):
        autocomplete_fields = ["relatedfield_symptom_list", ]

admin.site.register(A6218, A6218Admin)

class A6205Admin(admin.ModelAdmin):
        autocomplete_fields = ["relatedfield_name_of_operation", ]

admin.site.register(A6205, A6205Admin)

class A6214Admin(admin.ModelAdmin):
        radio_fields = {"relatedfield_own_health": admin.VERTICAL, "relatedfield_exercise_time": admin.VERTICAL, }
    autocomplete_fields = ["relatedfield_have_any_recent_symptoms_of_physical_discomfort", ]

admin.site.register(A6214, A6214Admin)

class Z6230Admin(admin.ModelAdmin):
    pass
admin.site.register(Z6230, Z6230Admin)

class A6220Admin(admin.ModelAdmin):
    pass
admin.site.register(A6220, A6220Admin)

class A6212Admin(admin.ModelAdmin):
        radio_fields = {"relatedfield_drinking_frequency": admin.VERTICAL, "relatedfield_smoking_frequency": admin.VERTICAL, }

admin.site.register(A6212, A6212Admin)

class T9001Admin(admin.ModelAdmin):
        autocomplete_fields = ["relatedfield_disease_name", "relatedfield_yi_lou_zhen_duan", "relatedfield_pai_chu_zhen_duan", ]

admin.site.register(T9001, T9001Admin)

class A5002Admin(admin.ModelAdmin):
        radio_fields = {"boolfield_shi_fou_ji_xu_shi_yong": admin.VERTICAL, }
    autocomplete_fields = ["relatedfield_disease_name", "relatedfield_drug_name", ]

admin.site.register(A5002, A5002Admin)

class Physical_examination_athletic_abilityAdmin(admin.ModelAdmin):
    pass
admin.site.register(Physical_examination_athletic_ability, Physical_examination_athletic_abilityAdmin)

class A6213Admin(admin.ModelAdmin):
        radio_fields = {"relatedfield_personality_tendency": admin.VERTICAL, "boolfield_shi_mian_qing_kuang": admin.VERTICAL, "boolfield_sheng_huo_gong_zuo_ya_li_qing_kuang": admin.VERTICAL, }

admin.site.register(A6213, A6213Admin)

class Z6261Admin(admin.ModelAdmin):
        autocomplete_fields = ["boolfield_ze_ren_ren", ]

admin.site.register(Z6261, Z6261Admin)

class A6210Admin(admin.ModelAdmin):
        autocomplete_fields = ["boolfield_yi_chuan_ji_bing", ]

admin.site.register(A6210, A6210Admin)

class A6209Admin(admin.ModelAdmin):
        autocomplete_fields = ["boolfield_jia_zu_xing_ji_bing", ]

admin.site.register(A6209, A6209Admin)

class A6502Admin(admin.ModelAdmin):
        radio_fields = {"boolfield_qian_dao_que_ren": admin.VERTICAL, }
    autocomplete_fields = ["boolfield_ze_ren_ren", ]

admin.site.register(A6502, A6502Admin)
