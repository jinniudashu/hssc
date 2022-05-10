from django.shortcuts import redirect
from django.contrib import admin
from django.shortcuts import reverse

from hssc.site import clinic_site
# 导入自定义作业完成信号
from core.signals import operand_finished
from service.models import *


class HsscFormAdmin(admin.ModelAdmin):
    exclude = ["hssc_id", "label", "name", "customer", "operator", "creater", "pid", "cpid", "slug", "created_time", "updated_time", ]
    view_on_site = False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        base_form = 'base_form'
        extra_context['base_form'] = base_form
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def save_model(self, request, obj, form, change):
        # 发送服务作业完成信号
        pid = obj.pid.id
        ocode = 'RTC'
        uid = request.user.id
        form_data = request.POST.copy()
        form_data.pop('csrfmiddlewaretoken')
        form_data.pop('_save')
        operand_finished.send(sender=self, pid=pid, ocode=ocode, uid=uid, form_data=form_data)
        print('发送操作完成信号：', pid, ocode, uid, form_data)
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


class Men_zhen_chu_fang_biaoAdmin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("药物处方", {"fields": ("boolfield_yong_yao_zhou_qi", "boolfield_chang_yong_chu_fang_liang", "boolfield_fu_yong_pin_ci", "relatedfield_drug_name", "boolfield_yong_yao_tu_jing", )}), )
    autocomplete_fields = ["relatedfield_drug_name", "boolfield_yong_yao_tu_jing", ]
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(Men_zhen_chu_fang_biao, Men_zhen_chu_fang_biaoAdmin)
clinic_site.register(Men_zhen_chu_fang_biao, Men_zhen_chu_fang_biaoAdmin)

class A6501Admin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("代人预约挂号", {"fields": ("datetimefield_ri_qi_shi_jian", "boolfield_ze_ren_ren", )}), )
    autocomplete_fields = ["boolfield_ze_ren_ren", ]
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(A6501, A6501Admin)
clinic_site.register(A6501, A6501Admin)

class A6502Admin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("门诊分诊", {"fields": ("boolfield_qian_dao_que_ren", )}), )
    autocomplete_fields = ["boolfield_qian_dao_que_ren", ]
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(A6502, A6502Admin)
clinic_site.register(A6502, A6502Admin)

class A3101Admin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("体格检查表", {"fields": ("characterfield_right_eye_vision", "characterfield_left_eye_vision", "numberfield_body_temperature", "numberfield_pulse", "numberfield_respiratory_rate", "numberfield_hight", "numberfield_weight", "numberfield_body_mass_index", "numberfield_systolic_blood_pressure", "numberfield_diastolic_blood_pressure", "boolfield_yao_wei", "relatedfield_athletic_ability", "relatedfield_left_ear_hearing", "relatedfield_right_ear_hearing", "relatedfield_lips", "relatedfield_dentition", "relatedfield_pharynx", "relatedfield_lower_extremity_edema", )}), )
    autocomplete_fields = ["relatedfield_athletic_ability", "relatedfield_left_ear_hearing", "relatedfield_right_ear_hearing", "relatedfield_lips", "relatedfield_dentition", "relatedfield_pharynx", "relatedfield_lower_extremity_edema", ]
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(A3101, A3101Admin)
clinic_site.register(A3101, A3101Admin)

class Tang_niao_bing_zhuan_yong_wen_zhenAdmin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("糖尿病专用问诊", {"fields": ("characterfield_supplementary_description_of_the_condition", "relatedfield_symptom_list", "boolfield_tang_niao_bing_zheng_zhuang", )}), )
    autocomplete_fields = ["relatedfield_symptom_list", "boolfield_tang_niao_bing_zheng_zhuang", ]
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(Tang_niao_bing_zhuan_yong_wen_zhen, Tang_niao_bing_zhuan_yong_wen_zhenAdmin)
clinic_site.register(Tang_niao_bing_zhuan_yong_wen_zhen, Tang_niao_bing_zhuan_yong_wen_zhenAdmin)

class Yao_shi_fu_wuAdmin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("药事服务", {"fields": ("relatedfield_drug_name", "relatedfield_disease_name", "boolfield_shi_fou_ji_xu_shi_yong", )}), )
    autocomplete_fields = ["relatedfield_drug_name", "relatedfield_disease_name", "boolfield_shi_fou_ji_xu_shi_yong", ]
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(Yao_shi_fu_wu, Yao_shi_fu_wuAdmin)
clinic_site.register(Yao_shi_fu_wu, Yao_shi_fu_wuAdmin)

class Tang_niao_bing_zi_wo_jian_ceAdmin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("糖尿病自我监测", {"fields": ("numberfield_kong_fu_xue_tang", )}), )
    
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(Tang_niao_bing_zi_wo_jian_ce, Tang_niao_bing_zi_wo_jian_ceAdmin)
clinic_site.register(Tang_niao_bing_zi_wo_jian_ce, Tang_niao_bing_zi_wo_jian_ceAdmin)

class A6217Admin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("院内辅助问诊", {"fields": ("characterfield_supplementary_description_of_the_condition", "relatedfield_symptom_list", )}), )
    autocomplete_fields = ["relatedfield_symptom_list", ]
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(A6217, A6217Admin)
clinic_site.register(A6217, A6217Admin)

class A6201Admin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("院外咨询", {"fields": ("characterfield_supplementary_description_of_the_condition", "relatedfield_symptom_list", "boolfield_chang_yong_zheng_zhuang", )}), )
    autocomplete_fields = ["relatedfield_symptom_list", "boolfield_chang_yong_zheng_zhuang", ]
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(A6201, A6201Admin)
clinic_site.register(A6201, A6201Admin)

class A6218Admin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("门诊医生问诊", {"fields": ("characterfield_supplementary_description_of_the_condition", "relatedfield_symptom_list", )}), )
    autocomplete_fields = ["relatedfield_symptom_list", ]
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(A6218, A6218Admin)
clinic_site.register(A6218, A6218Admin)

class T8901Admin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("非胰岛素依赖性糖尿病", {"fields": ("relatedfield_disease_name", "relatedfield_yi_lou_zhen_duan", "relatedfield_pai_chu_zhen_duan", )}), )
    autocomplete_fields = ["relatedfield_disease_name", "relatedfield_yi_lou_zhen_duan", "relatedfield_pai_chu_zhen_duan", ]
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(T8901, T8901Admin)
clinic_site.register(T8901, T8901Admin)

class T6301Admin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("糖尿病一般随访", {"fields": ("boolfield_fu_yong_pin_ci", "boolfield_yao_pin_dan_wei", "relatedfield_drug_name", "relatedfield_drinking_frequency", "relatedfield_smoking_frequency", "boolfield_tang_niao_bing_zheng_zhuang", )}), 
        ("足背动脉检查", {"fields": ("relatedfield_left_foot", "relatedfield_right_foot", )}), 
        ("眼底检查", {"fields": ("relatedfield_fundus", )}), 
        ("血压监测", {"fields": ("numberfield_systolic_blood_pressure", "numberfield_diastolic_blood_pressure", )}), 
        ("空腹血糖检查", {"fields": ("numberfield_kong_fu_xue_tang", )}), )
    autocomplete_fields = ["boolfield_yao_pin_dan_wei", "relatedfield_drug_name", "relatedfield_drinking_frequency", "relatedfield_smoking_frequency", "boolfield_tang_niao_bing_zheng_zhuang", "relatedfield_left_foot", "relatedfield_right_foot", "relatedfield_fundus", ]
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(T6301, T6301Admin)
clinic_site.register(T6301, T6301Admin)

class A6202Admin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("院外辅助问诊", {"fields": ("characterfield_supplementary_description_of_the_condition", "relatedfield_symptom_list", )}), )
    autocomplete_fields = ["relatedfield_symptom_list", ]
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(A6202, A6202Admin)
clinic_site.register(A6202, A6202Admin)

class A6220Admin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("监测评估", {"fields": ("boolfield_yuan_wai_jian_kang_ping_gu", )}), )
    autocomplete_fields = ["boolfield_yuan_wai_jian_kang_ping_gu", ]
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(A6220, A6220Admin)
clinic_site.register(A6220, A6220Admin)

class A6299Admin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("遗传病史", {"fields": ("boolfield_yi_chuan_ji_bing", "boolfield_yi_chuan_bing_shi_cheng_yuan", )}), 
        ("过敏史", {"fields": ("relatedfield_drug_name", )}), 
        ("家族病史", {"fields": ("boolfield_jia_zu_xing_ji_bing", "boolfield_jia_zu_bing_shi_cheng_yuan", )}), 
        ("手术史", {"fields": ("datetimefield_date", "relatedfield_name_of_operation", )}), 
        ("疾病史", {"fields": ("datetimefield_time_of_diagnosis", "boolfield_ge_ren_bing_shi", )}), 
        ("外伤史", {"fields": ("boolfield_wai_shang_ri_qi", "boolfield_wai_shang_xing_ji_bing", )}), 
        ("输血史", {"fields": ("numberfield_blood_transfusion", "boolfield_shu_xue_ri_qi", )}), 
        ("个人心理综合素质调查", {"fields": ("relatedfield_personality_tendency", "boolfield_shi_mian_qing_kuang", "boolfield_sheng_huo_gong_zuo_ya_li_qing_kuang", )}), 
        ("个人适应能力评估", {"fields": ("characterfield_working_hours_per_day", "relatedfield_are_you_satisfied_with_the_job_and_life", "relatedfield_are_you_satisfied_with_your_adaptability", )}), 
        ("个人身体健康评估", {"fields": ("relatedfield_own_health", "relatedfield_compared_to_last_year", "relatedfield_sports_preference", "relatedfield_exercise_time", "relatedfield_have_any_recent_symptoms_of_physical_discomfort", )}), 
        ("个人健康行为调查", {"fields": ("characterfield_average_sleep_duration", "characterfield_duration_of_insomnia", "relatedfield_drinking_frequency", "relatedfield_smoking_frequency", )}), 
        ("社会环境评估", {"fields": ("relatedfield_is_the_living_environment_satisfactory", "relatedfield_is_the_transportation_convenient", )}), )
    autocomplete_fields = ["boolfield_yi_chuan_ji_bing", "boolfield_yi_chuan_bing_shi_cheng_yuan", "relatedfield_drug_name", "boolfield_jia_zu_xing_ji_bing", "boolfield_jia_zu_bing_shi_cheng_yuan", "relatedfield_name_of_operation", "boolfield_ge_ren_bing_shi", "boolfield_wai_shang_xing_ji_bing", "relatedfield_personality_tendency", "boolfield_shi_mian_qing_kuang", "boolfield_sheng_huo_gong_zuo_ya_li_qing_kuang", "relatedfield_are_you_satisfied_with_the_job_and_life", "relatedfield_are_you_satisfied_with_your_adaptability", "relatedfield_own_health", "relatedfield_compared_to_last_year", "relatedfield_sports_preference", "relatedfield_exercise_time", "relatedfield_have_any_recent_symptoms_of_physical_discomfort", "relatedfield_drinking_frequency", "relatedfield_smoking_frequency", "relatedfield_is_the_living_environment_satisfactory", "relatedfield_is_the_transportation_convenient", ]
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(A6299, A6299Admin)
clinic_site.register(A6299, A6299Admin)

class A3502Admin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("尿常规检查", {"fields": ("boolfield_niao_tang", "boolfield_dan_bai_zhi", "boolfield_tong_ti", )}), )
    autocomplete_fields = ["boolfield_niao_tang", "boolfield_dan_bai_zhi", "boolfield_tong_ti", ]
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(A3502, A3502Admin)
clinic_site.register(A3502, A3502Admin)

class Tang_niao_bing_cha_tiAdmin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("眼底检查", {"fields": ("relatedfield_fundus", )}), 
        ("足背动脉检查", {"fields": ("relatedfield_left_foot", "relatedfield_right_foot", )}), )
    autocomplete_fields = ["relatedfield_fundus", "relatedfield_left_foot", "relatedfield_right_foot", ]
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(Tang_niao_bing_cha_ti, Tang_niao_bing_cha_tiAdmin)
clinic_site.register(Tang_niao_bing_cha_ti, Tang_niao_bing_cha_tiAdmin)

class Xue_ya_jian_ceAdmin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("血压监测", {"fields": ("numberfield_systolic_blood_pressure", "numberfield_diastolic_blood_pressure", )}), )
    
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(Xue_ya_jian_ce, Xue_ya_jian_ceAdmin)
clinic_site.register(Xue_ya_jian_ce, Xue_ya_jian_ceAdmin)

class Kong_fu_xue_tang_jian_chaAdmin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("空腹血糖检查", {"fields": ("numberfield_kong_fu_xue_tang", )}), )
    
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(Kong_fu_xue_tang_jian_cha, Kong_fu_xue_tang_jian_chaAdmin)
clinic_site.register(Kong_fu_xue_tang_jian_cha, Kong_fu_xue_tang_jian_chaAdmin)

class Tang_hua_xue_hong_dan_bai_jian_cha_biaoAdmin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("糖化血红蛋白检查", {"fields": ("numberfield_tang_hua_xue_hong_dan_bai", )}), )
    
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(Tang_hua_xue_hong_dan_bai_jian_cha_biao, Tang_hua_xue_hong_dan_bai_jian_cha_biaoAdmin)
clinic_site.register(Tang_hua_xue_hong_dan_bai_jian_cha_biao, Tang_hua_xue_hong_dan_bai_jian_cha_biaoAdmin)

class T9001Admin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("非胰岛素依赖性糖尿病", {"fields": ("relatedfield_disease_name", "relatedfield_yi_lou_zhen_duan", "relatedfield_pai_chu_zhen_duan", )}), )
    autocomplete_fields = ["relatedfield_disease_name", "relatedfield_yi_lou_zhen_duan", "relatedfield_pai_chu_zhen_duan", ]
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(T9001, T9001Admin)
clinic_site.register(T9001, T9001Admin)

class Qian_yue_fu_wuAdmin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("家庭医生签约", {"fields": ("boolfield_jia_ting_qian_yue_fu_wu_xie_yi", "boolfield_qian_yue_que_ren", "boolfield_ze_ren_ren", )}), )
    autocomplete_fields = ["boolfield_qian_yue_que_ren", "boolfield_ze_ren_ren", ]
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(Qian_yue_fu_wu, Qian_yue_fu_wuAdmin)
clinic_site.register(Qian_yue_fu_wu, Qian_yue_fu_wuAdmin)

class Shu_ye_zhu_sheAdmin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": (("characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ),)}), 
        ("输液注射单", {"fields": ("boolfield_yao_pin_gui_ge", "boolfield_yong_yao_zhou_qi", "boolfield_chang_yong_chu_fang_liang", "boolfield_zhi_xing_qian_ming", "boolfield_fu_yong_pin_ci", "boolfield_zhu_she_ri_qi", "relatedfield_drug_name", )}), )
    autocomplete_fields = ["relatedfield_drug_name", ]
    readonly_fields = ["characterfield_name", "characterfield_gender", "characterfield_age", "characterfield_contact_address", "characterfield_contact_number", ]
admin.site.register(Shu_ye_zhu_she, Shu_ye_zhu_sheAdmin)
clinic_site.register(Shu_ye_zhu_she, Shu_ye_zhu_sheAdmin)

class Ju_min_ji_ben_xin_xi_diao_chaAdmin(HsscFormAdmin):
    fieldsets = (("基本信息", {"fields": ((),)}), 
        ("个人基本信息", {"fields": ("characterfield_name", "characterhssc_identification_number", "characterfield_resident_file_number", "characterfield_family_address", "characterfield_contact_number", "characterfield_medical_ic_card_number", "datetimefield_date_of_birth", "relatedfield_gender", "relatedfield_nationality", "relatedfield_marital_status", "relatedfield_education", "relatedfield_occupational_status", "relatedfield_medical_expenses_burden", "relatedfield_type_of_residence", "relatedfield_blood_type", "relatedfield_signed_family_doctor", "relatedfield_family_relationship", )}), )
    autocomplete_fields = ["relatedfield_gender", "relatedfield_nationality", "relatedfield_marital_status", "relatedfield_education", "relatedfield_occupational_status", "relatedfield_medical_expenses_burden", "relatedfield_type_of_residence", "relatedfield_blood_type", "relatedfield_signed_family_doctor", "relatedfield_family_relationship", ]
    readonly_fields = []
admin.site.register(Ju_min_ji_ben_xin_xi_diao_cha, Ju_min_ji_ben_xin_xi_diao_chaAdmin)
clinic_site.register(Ju_min_ji_ben_xin_xi_diao_cha, Ju_min_ji_ben_xin_xi_diao_chaAdmin)
