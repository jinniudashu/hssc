from django.contrib import admin
from hssc.site import clinic_site

from .models import *

class A6203Admin(admin.ModelAdmin):
    autocomplete_fields = ["relatedfield_gender", "relatedfield_nationality", "relatedfield_marital_status", "relatedfield_education", "relatedfield_occupational_status", "relatedfield_medical_expenses_burden", "relatedfield_type_of_residence", "relatedfield_blood_type", "relatedfield_signed_family_doctor", "relatedfield_family_relationship", ]
    search_fields=["name"]
admin.site.register(A6203, A6203Admin)

class Yao_pin_ji_ben_xin_xi_biaoAdmin(admin.ModelAdmin):
    search_fields=["boolfield_yao_pin_ming_cheng", ]
    autocomplete_fields = ["boolfield_chu_fang_ji_liang_dan_wei", "boolfield_ru_ku_ji_liang_dan_wei", "boolfield_xiao_shou_ji_liang_dan_wei", "boolfield_yong_yao_tu_jing", "boolfield_yao_pin_fen_lei", ]
admin.site.register(Yao_pin_ji_ben_xin_xi_biao, Yao_pin_ji_ben_xin_xi_biaoAdmin)
clinic_site.register(Yao_pin_ji_ben_xin_xi_biao, Yao_pin_ji_ben_xin_xi_biaoAdmin)

class Zhi_yuan_ji_ben_xin_xi_biaoAdmin(admin.ModelAdmin):
    search_fields=["characterfield_name"]
    autocomplete_fields = ["relatedfield_affiliation", "relatedfield_service_role", ]
admin.site.register(Zhi_yuan_ji_ben_xin_xi_biao, Zhi_yuan_ji_ben_xin_xi_biaoAdmin)
clinic_site.register(Zhi_yuan_ji_ben_xin_xi_biao, Zhi_yuan_ji_ben_xin_xi_biaoAdmin)

class Ji_gou_ji_ben_xin_xi_biaoAdmin(admin.ModelAdmin):
    search_fields=["name"]
admin.site.register(Ji_gou_ji_ben_xin_xi_biao, Ji_gou_ji_ben_xin_xi_biaoAdmin)
clinic_site.register(Ji_gou_ji_ben_xin_xi_biao, Ji_gou_ji_ben_xin_xi_biaoAdmin)

class She_bei_ji_ben_xin_xi_biaoAdmin(admin.ModelAdmin):
    search_fields=["name"]
    autocomplete_fields = ["boolfield_she_bei_shi_yong_fu_wu_gong_neng", ]
admin.site.register(She_bei_ji_ben_xin_xi_biao, She_bei_ji_ben_xin_xi_biaoAdmin)

class Wu_liu_gong_ying_shang_ji_ben_xin_xi_biaoAdmin(admin.ModelAdmin):
    search_fields=["name"]
    autocomplete_fields = ["boolfield_xin_yu_ping_ji", ]
admin.site.register(Wu_liu_gong_ying_shang_ji_ben_xin_xi_biao, Wu_liu_gong_ying_shang_ji_ben_xin_xi_biaoAdmin)
