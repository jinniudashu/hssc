from django.contrib import admin
from .models import *


class Li_pei_dui_zhang_danAdmin(admin.ModelAdmin):
    pass
admin.site.register(Li_pei_dui_zhang_dan, Li_pei_dui_zhang_danAdmin)

class Bang_ding_que_ren_biaoAdmin(admin.ModelAdmin):
        radio_fields = {"boolfield_shi_fou_bang_ding_bei_bao_ren_xin_xi": admin.VERTICAL, }

admin.site.register(Bang_ding_que_ren_biao, Bang_ding_que_ren_biaoAdmin)

class He_bao_danAdmin(admin.ModelAdmin):
        radio_fields = {"boolfield_shi_fou_shen_he_tong_guo": admin.VERTICAL, }

admin.site.register(He_bao_dan, He_bao_danAdmin)

class Yu_yue_tong_zhi_danAdmin(admin.ModelAdmin):
    pass
admin.site.register(Yu_yue_tong_zhi_dan, Yu_yue_tong_zhi_danAdmin)

class Zhen_jian_sui_fang_biaoAdmin(admin.ModelAdmin):
        radio_fields = {"boolfield_deng_hou_qing_kuang": admin.VERTICAL, "boolfield_jie_dai_fu_wu": admin.VERTICAL, "boolfield_zhi_liao_jian_gou_tong_qing_kuang": admin.VERTICAL, "boolfield_zhi_liao_gan_shou_he_xiao_guo_ping_jia": admin.VERTICAL, }

admin.site.register(Zhen_jian_sui_fang_biao, Zhen_jian_sui_fang_biaoAdmin)

class Fen_zhen_que_ren_biaoAdmin(admin.ModelAdmin):
        radio_fields = {"boolfield_dao_da_que_ren": admin.VERTICAL, }

admin.site.register(Fen_zhen_que_ren_biao, Fen_zhen_que_ren_biaoAdmin)

class A6401Admin(admin.ModelAdmin):
        autocomplete_fields = ["boolfield_jiu_zhen_ji_gou_ze_ren_ren", ]

admin.site.register(A6401, A6401Admin)

class A6203Admin(admin.ModelAdmin):
    pass
admin.site.register(A6203, A6203Admin)

class Zhen_hou_hui_fang_danAdmin(admin.ModelAdmin):
        radio_fields = {"boolfield_zhi_liao_gan_shou_he_xiao_guo_ping_jia": admin.VERTICAL, "boolfield_deng_hou_qing_kuang": admin.VERTICAL, "boolfield_nin_cong_he_chu_zhi_dao_wo_men_de_fu_wu": admin.VERTICAL, "boolfield_nin_shi_fou_yuan_yi_xiang_ta_ren_tui_jian_wo_men": admin.VERTICAL, }

admin.site.register(Zhen_hou_hui_fang_dan, Zhen_hou_hui_fang_danAdmin)

class Men_zhen_fu_wu_ji_lu_2Admin(admin.ModelAdmin):
        autocomplete_fields = ["boolfield_zheng_zhuang", "boolfield_jian_cha_xiang_mu", "boolfield_zhen_duan", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_jian_kang_gan_yu_fu_wu", ]

admin.site.register(Men_zhen_fu_wu_ji_lu_2, Men_zhen_fu_wu_ji_lu_2Admin)

class Tou_su_jian_yi_biaoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tou_su_jian_yi_biao, Tou_su_jian_yi_biaoAdmin)

class Yi_an_pai_fu_wu_cha_xun_biaoAdmin(admin.ModelAdmin):
        autocomplete_fields = ["boolfield_jiu_zhen_ji_gou_ze_ren_ren", ]

admin.site.register(Yi_an_pai_fu_wu_cha_xun_biao, Yi_an_pai_fu_wu_cha_xun_biaoAdmin)

class Kou_qiang_jian_cha_ji_zhen_duanAdmin(admin.ModelAdmin):
        radio_fields = {"boolfield_shi_fou_an_pai_zhi_liao_ji_hua": admin.VERTICAL, }

admin.site.register(Kou_qiang_jian_cha_ji_zhen_duan, Kou_qiang_jian_cha_ji_zhen_duanAdmin)

class Tui_bao_shen_qing_biaoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tui_bao_shen_qing_biao, Tui_bao_shen_qing_biaoAdmin)

class Tui_bao_que_ren_danAdmin(admin.ModelAdmin):
        radio_fields = {"boolfield_ke_hu_tui_bao_shen_qing_shi_fou_tong_guo": admin.VERTICAL, }

admin.site.register(Tui_bao_que_ren_dan, Tui_bao_que_ren_danAdmin)

class Ji_gou_ji_ben_xin_xi_biaoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Ji_gou_ji_ben_xin_xi_biao, Ji_gou_ji_ben_xin_xi_biaoAdmin)

class Zhi_yuan_ji_ben_xin_xi_biaoAdmin(admin.ModelAdmin):
        autocomplete_fields = ["boolfield_suo_shu_ji_gou", ]

admin.site.register(Zhi_yuan_ji_ben_xin_xi_biao, Zhi_yuan_ji_ben_xin_xi_biaoAdmin)

class She_bei_ji_ben_xin_xi_biaoAdmin(admin.ModelAdmin):
        autocomplete_fields = ["boolfield_she_bei_shi_yong_fu_wu_gong_neng", ]

admin.site.register(She_bei_ji_ben_xin_xi_biao, She_bei_ji_ben_xin_xi_biaoAdmin)

class Zhi_liao_fei_yong_hui_zong_danAdmin(admin.ModelAdmin):
    pass
admin.site.register(Zhi_liao_fei_yong_hui_zong_dan, Zhi_liao_fei_yong_hui_zong_danAdmin)

class Man_yi_du_diao_cha_biaoAdmin(admin.ModelAdmin):
        radio_fields = {"boolfield_yi_liao_fu_wu_ji_neng_xiang_mu_ping_fen": admin.VERTICAL, "boolfield_ping_tai_fu_wu_xiang_mu_ping_fen": admin.VERTICAL, "boolfield_fu_wu_liu_cheng_ping_fen": admin.VERTICAL, "boolfield_fu_wu_xiao_lv_ping_fen": admin.VERTICAL, }

admin.site.register(Man_yi_du_diao_cha_biao, Man_yi_du_diao_cha_biaoAdmin)

class Qian_shu_que_ren_danAdmin(admin.ModelAdmin):
        radio_fields = {"boolfield_ren_shen_xian_li_pei_shen_qing_shu_qian_shu": admin.VERTICAL, }

admin.site.register(Qian_shu_que_ren_dan, Qian_shu_que_ren_danAdmin)

class Men_zhen_ji_lu_dan_shen_he_danAdmin(admin.ModelAdmin):
        radio_fields = {"boolfield_li_pei_men_zhen_ji_lu_qian_shu": admin.VERTICAL, }

admin.site.register(Men_zhen_ji_lu_dan_shen_he_dan, Men_zhen_ji_lu_dan_shen_he_danAdmin)

class Li_pei_dui_zhang_dan_shen_he_danAdmin(admin.ModelAdmin):
        radio_fields = {"boolfield_li_pei_dui_zhang_dan_qian_shu": admin.VERTICAL, }

admin.site.register(Li_pei_dui_zhang_dan_shen_he_dan, Li_pei_dui_zhang_dan_shen_he_danAdmin)

class Zhi_liao_ji_hua_biaoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Zhi_liao_ji_hua_biao, Zhi_liao_ji_hua_biaoAdmin)

class Li_pei_fei_yong_hui_zong_dan_shen_heAdmin(admin.ModelAdmin):
        radio_fields = {"boolfield_li_pei_fei_yong_hui_zong_dan_qian_shu": admin.VERTICAL, }

admin.site.register(Li_pei_fei_yong_hui_zong_dan_shen_he, Li_pei_fei_yong_hui_zong_dan_shen_heAdmin)

class Men_zhen_fu_wu_ji_lu_danAdmin(admin.ModelAdmin):
        autocomplete_fields = ["boolfield_zheng_zhuang", "boolfield_jian_cha_xiang_mu", "boolfield_zhen_duan", "boolfield_zhi_liao_xiang_mu", "boolfield_qi_ta_jian_kang_gan_yu_fu_wu", ]

admin.site.register(Men_zhen_fu_wu_ji_lu_dan, Men_zhen_fu_wu_ji_lu_danAdmin)

class A6502Admin(admin.ModelAdmin):
        radio_fields = {"boolfield_jie_dan_que_ren": admin.VERTICAL, }

admin.site.register(A6502, A6502Admin)

class Ren_shen_xian_li_pei_shen_qing_shuAdmin(admin.ModelAdmin):
        radio_fields = {"boolfield_yu_chu_xian_ren_guan_xi": admin.VERTICAL, }

admin.site.register(Ren_shen_xian_li_pei_shen_qing_shu, Ren_shen_xian_li_pei_shen_qing_shuAdmin)
