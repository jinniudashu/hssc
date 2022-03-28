from django.contrib import admin
from .models import *
    
@admin.register(T3003)
class T3003Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_left_foot", "relatedfield_right_foot", ]

@admin.register(A6210)
class A6210Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_family_relationship", ]

admin.site.register(A3101)

@admin.register(A6207)
class A6207Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_drug_name", ]

@admin.register(Tang_niao_bing_zhen_duan_biao)
class Tang_niao_bing_zhen_duan_biaoAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_disease_name", "relatedfield_yi_lou_zhen_duan", "relatedfield_pai_chu_zhen_duan", "relatedfield_di_yi_zhen_duan", ]

@admin.register(A6209)
class A6209Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_family_relationship", ]

admin.site.register(A3103)

@admin.register(A6201)
class A6201Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_symptom_list", ]

@admin.register(A3110)
class A3110Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_left_ear_hearing", "relatedfield_right_ear_hearing", ]

@admin.register(T4501)
class T4501Admin(admin.ModelAdmin):
    autocomplete_fields = ["T4501", ]

@admin.register(A6215)
class A6215Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_are_you_satisfied_with_the_job_and_life", "relatedfield_are_you_satisfied_with_your_adaptability", ]

admin.site.register(T3404)

admin.site.register(Z6233)

@admin.register(A6204)
class A6204Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_disease_name", ]

@admin.register(Z6205)
class Z6205Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_affiliation", "relatedfield_service_role", ]

@admin.register(T4502)
class T4502Admin(admin.ModelAdmin):
    autocomplete_fields = ["T4502", ]

@admin.register(A6218)
class A6218Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_symptom_list", ]

@admin.register(A6205)
class A6205Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_name_of_operation", ]

@admin.register(Tang_niao_bing_cha_ti_biao)
class Tang_niao_bing_cha_ti_biaoAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_fundus", "relatedfield_left_foot", "relatedfield_right_foot", ]

@admin.register(A6214)
class A6214Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_own_health", "relatedfield_compared_to_last_year", "relatedfield_sports_preference", "relatedfield_exercise_time", "relatedfield_have_any_recent_symptoms_of_physical_discomfort", ]

admin.site.register(A3105)

@admin.register(A3108)
class A3108Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_lips", "relatedfield_dentition", "relatedfield_pharynx", ]

admin.site.register(A3109)

@admin.register(A6206)
class A6206Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_disease_name", ]

admin.site.register(Z6230)

admin.site.register(A6208)

@admin.register(Yong_yao_diao_cha_biao)
class Yong_yao_diao_cha_biaoAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_drug_name", ]

@admin.register(A6203)
class A6203Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_family_id", "relatedfield_gender", "relatedfield_nationality", "relatedfield_marital_status", "relatedfield_education", "relatedfield_occupational_status", "relatedfield_medical_expenses_burden", "relatedfield_type_of_residence", "relatedfield_blood_type", "relatedfield_signed_family_doctor", "relatedfield_family_relationship", ]

admin.site.register(Z6201)

admin.site.register(T3405)

@admin.register(A6202)
class A6202Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_symptom_list", ]

admin.site.register(A6501)

admin.site.register(T4505)

@admin.register(T4504)
class T4504Admin(admin.ModelAdmin):
    autocomplete_fields = ["T4504", ]

@admin.register(T3002)
class T3002Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_fundus", ]

@admin.register(A5001)
class A5001Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_drug_name", ]

@admin.register(A6217)
class A6217Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_symptom_list", ]

@admin.register(Physical_examination_athletic_ability)
class Physical_examination_athletic_abilityAdmin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_athletic_ability", ]

@admin.register(A6212)
class A6212Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_drinking_frequency", "relatedfield_smoking_frequency", ]

@admin.register(A6216)
class A6216Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_is_the_living_environment_satisfactory", "relatedfield_is_the_transportation_convenient", ]

@admin.register(A5002)
class A5002Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_drug_name", "relatedfield_disease_name", "boolfield_shi_fou_ji_xu_shi_yong", ]

@admin.register(A3001)
class A3001Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_athletic_ability", "relatedfield_left_ear_hearing", "relatedfield_right_ear_hearing", "relatedfield_lips", "relatedfield_dentition", "relatedfield_pharynx", ]

@admin.register(A6213)
class A6213Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_personality_tendency", "boolfield_shi_mian_qing_kuang", "boolfield_sheng_huo_gong_zuo_ya_li_qing_kuang", ]

@admin.register(T6301)
class T6301Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_family_id", "relatedfield_gender", "relatedfield_nationality", "relatedfield_marital_status", "relatedfield_education", "relatedfield_occupational_status", "relatedfield_medical_expenses_burden", "relatedfield_type_of_residence", "relatedfield_blood_type", "relatedfield_signed_family_doctor", "relatedfield_drug_name", "relatedfield_drinking_frequency", "relatedfield_smoking_frequency", "relatedfield_family_relationship", "relatedfield_fundus", "relatedfield_left_foot", "relatedfield_right_foot", ]

@admin.register(A6211)
class A6211Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_major_life", ]

@admin.register(A6219)
class A6219Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_symptom_list", ]

@admin.register(Z6261)
class Z6261Admin(admin.ModelAdmin):
    autocomplete_fields = ["boolfield_qian_yue_que_ren", "boolfield_ze_ren_ren", ]

@admin.register(A6220)
class A6220Admin(admin.ModelAdmin):
    autocomplete_fields = ["boolfield_yuan_wai_jian_kang_ping_gu", ]
