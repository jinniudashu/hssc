from django.contrib import admin
from .models import *

class A6219Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_symptom_list", "boolfield_tang_niao_bing_zheng_zhuang", ]
admin.site.register(A6219, A6219Admin)

class A6501Admin(admin.ModelAdmin):
    autocomplete_fields = ["boolfield_ze_ren_ren", ]
admin.site.register(A6501, A6501Admin)

class A5001Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_drug_name", ]
admin.site.register(A5001, A5001Admin)

admin.site.register(T4505)

class A6211Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_major_life", ]
admin.site.register(A6211, A6211Admin)

class T3003Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_left_foot", "relatedfield_right_foot", ]
admin.site.register(T3003, T3003Admin)

class T4504Admin(admin.ModelAdmin):
    autocomplete_fields = ["T4504", ]
admin.site.register(T4504, T4504Admin)

class Yao_pin_qing_danAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_drug_name", ]
admin.site.register(Yao_pin_qing_dan, Yao_pin_qing_danAdmin)

class Ji_gou_qing_danAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_affiliation", ]
admin.site.register(Ji_gou_qing_dan, Ji_gou_qing_danAdmin)

class A3502Admin(admin.ModelAdmin):
    autocomplete_fields = ["boolfield_niao_tang", "boolfield_dan_bai_zhi", "boolfield_tong_ti", ]
admin.site.register(A3502, A3502Admin)

class A6210Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_family_relationship", ]
admin.site.register(A6210, A6210Admin)

class Zhi_yuan_biaoAdmin(admin.ModelAdmin):
    autocomplete_fields = ["boolfield_ze_ren_ren", ]
admin.site.register(Zhi_yuan_biao, Zhi_yuan_biaoAdmin)

admin.site.register(A3101)

class A6207Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_drug_name", ]
admin.site.register(A6207, A6207Admin)

class T9001Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_disease_name", "relatedfield_yi_lou_zhen_duan", "relatedfield_pai_chu_zhen_duan", "relatedfield_di_yi_zhen_duan", ]
admin.site.register(T9001, T9001Admin)

class A6209Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_family_relationship", ]
admin.site.register(A6209, A6209Admin)

admin.site.register(A3103)

admin.site.register(Z6201)

class T4501Admin(admin.ModelAdmin):
    autocomplete_fields = ["T4501", ]
admin.site.register(T4501, T4501Admin)

class A6201Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_symptom_list", ]
admin.site.register(A6201, A6201Admin)

class A3110Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_left_ear_hearing", "relatedfield_right_ear_hearing", ]
admin.site.register(A3110, A3110Admin)

class A6215Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_are_you_satisfied_with_the_job_and_life", "relatedfield_are_you_satisfied_with_your_adaptability", ]
admin.site.register(A6215, A6215Admin)

admin.site.register(T3404)

admin.site.register(Z6233)

class A6204Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_disease_name", ]
admin.site.register(A6204, A6204Admin)

class A6218Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_symptom_list", ]
admin.site.register(A6218, A6218Admin)

class Z6205Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_affiliation", "relatedfield_service_role", ]
admin.site.register(Z6205, Z6205Admin)

class T4502Admin(admin.ModelAdmin):
    autocomplete_fields = ["T4502", ]
admin.site.register(T4502, T4502Admin)

class A6216Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_is_the_living_environment_satisfactory", "relatedfield_is_the_transportation_convenient", ]
admin.site.register(A6216, A6216Admin)

class A6205Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_name_of_operation", ]
admin.site.register(A6205, A6205Admin)

class A6214Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_own_health", "relatedfield_compared_to_last_year", "relatedfield_sports_preference", "relatedfield_exercise_time", "relatedfield_have_any_recent_symptoms_of_physical_discomfort", ]
admin.site.register(A6214, A6214Admin)

admin.site.register(A3105)

class A3108Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_lips", "relatedfield_dentition", "relatedfield_pharynx", ]
admin.site.register(A3108, A3108Admin)

admin.site.register(A3109)

class A6502Admin(admin.ModelAdmin):
    autocomplete_fields = ["boolfield_qian_yue_que_ren", "boolfield_ze_ren_ren", ]
admin.site.register(A6502, A6502Admin)

class A6206Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_disease_name", ]
admin.site.register(A6206, A6206Admin)

admin.site.register(Z6230)

admin.site.register(A6208)

class T3002Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_fundus", ]
admin.site.register(T3002, T3002Admin)

class Yong_yao_diao_cha_biaoAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_drug_name", ]
admin.site.register(Yong_yao_diao_cha_biao, Yong_yao_diao_cha_biaoAdmin)

class A6203Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_gender", "relatedfield_nationality", "relatedfield_marital_status", "relatedfield_education", "relatedfield_occupational_status", "relatedfield_medical_expenses_burden", "relatedfield_type_of_residence", "relatedfield_blood_type", "relatedfield_signed_family_doctor", "relatedfield_family_relationship", ]
admin.site.register(A6203, A6203Admin)

class A3001Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_athletic_ability", "relatedfield_left_ear_hearing", "relatedfield_right_ear_hearing", "relatedfield_lips", "relatedfield_dentition", "relatedfield_pharynx", ]
admin.site.register(A3001, A3001Admin)

admin.site.register(T3405)

class A6202Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_symptom_list", ]
admin.site.register(A6202, A6202Admin)

class A6217Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_symptom_list", ]
admin.site.register(A6217, A6217Admin)

class Physical_examination_athletic_abilityAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_athletic_ability", ]
admin.site.register(Physical_examination_athletic_ability, Physical_examination_athletic_abilityAdmin)

class A6212Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_drinking_frequency", "relatedfield_smoking_frequency", ]
admin.site.register(A6212, A6212Admin)

class A5002Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_drug_name", "relatedfield_disease_name", "boolfield_shi_fou_ji_xu_shi_yong", ]
admin.site.register(A5002, A5002Admin)

class A6213Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_personality_tendency", "boolfield_shi_mian_qing_kuang", "boolfield_sheng_huo_gong_zuo_ya_li_qing_kuang", ]
admin.site.register(A6213, A6213Admin)

class Z6261Admin(admin.ModelAdmin):
    autocomplete_fields = ["boolfield_qian_yue_que_ren", "boolfield_ze_ren_ren", ]
admin.site.register(Z6261, Z6261Admin)

class T6301Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_drug_name", "relatedfield_gender", "relatedfield_nationality", "relatedfield_marital_status", "relatedfield_education", "relatedfield_occupational_status", "relatedfield_medical_expenses_burden", "relatedfield_type_of_residence", "relatedfield_blood_type", "relatedfield_signed_family_doctor", "relatedfield_drinking_frequency", "relatedfield_smoking_frequency", "relatedfield_family_relationship", "relatedfield_fundus", "relatedfield_left_foot", "relatedfield_right_foot", ]
admin.site.register(T6301, T6301Admin)

class A6220Admin(admin.ModelAdmin):
    autocomplete_fields = ["boolfield_yuan_wai_jian_kang_ping_gu", ]
admin.site.register(A6220, A6220Admin)
