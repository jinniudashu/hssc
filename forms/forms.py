from django.forms import ModelForm, Form,  widgets, fields, RadioSelect, Select, CheckboxSelectMultiple, CheckboxInput, SelectMultiple, NullBooleanSelect
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit

from .models import *

class Z6205_ModelForm(ModelForm):
    class Meta:
        model = Z6205
        fields = ['characterfield_name', 'characterfield_gender', 'characterfield_age', 'characterhssc_identification_number', 'characterfield_contact_address', 'characterfield_practice_qualification', 'characterfield_password_setting', 'characterfield_confirm_password', 'characterfield_expertise', 'characterfield_practice_time', 'datetimefield_date_of_birth', 'relatedfield_affiliation', 'relatedfield_service_role', ]
        widgets = {'relatedfield_affiliation': Select, 'relatedfield_service_role': CheckboxSelectMultiple, }
    
class A3109_ModelForm(ModelForm):
    class Meta:
        model = A3109
        fields = ['characterfield_right_eye_vision', 'characterfield_left_eye_vision', ]
        
    
class A3108_ModelForm(ModelForm):
    class Meta:
        model = A3108
        fields = ['relatedfield_lips', 'relatedfield_dentition', 'relatedfield_pharynx', ]
        widgets = {'relatedfield_lips': RadioSelect, 'relatedfield_dentition': RadioSelect, 'relatedfield_pharynx': Select, }
    
class T4502_ModelForm(ModelForm):
    class Meta:
        model = T4502
        fields = ['T4502', ]
        widgets = {'T4502': SelectMultiple, }
    
class Ji_gou_ji_ben_xin_xi_biao_ModelForm(ModelForm):
    class Meta:
        model = Ji_gou_ji_ben_xin_xi_biao
        fields = ['characterfield_contact_address', 'characterfield_contact_number', 'boolfield_ji_gou_bian_ma', 'boolfield_ji_gou_ming_cheng', 'boolfield_ji_gou_dai_ma', 'boolfield_ji_gou_shu_xing', 'boolfield_ji_gou_ceng_ji', 'boolfield_suo_zai_hang_zheng_qu_hua_dai_ma', 'boolfield_xing_zheng_qu_hua_gui_shu', 'boolfield_fa_ding_fu_ze_ren', ]
        
    
class Wu_liu_gong_ying_shang_ji_ben_xin_xi_biao_ModelForm(ModelForm):
    class Meta:
        model = Wu_liu_gong_ying_shang_ji_ben_xin_xi_biao
        fields = ['characterfield_contact_address', 'characterfield_contact_number', 'boolfield_gong_ying_shang_bian_ma', 'boolfield_zhu_yao_gong_ying_chan_pin', 'boolfield_gong_huo_zhou_qi', 'boolfield_gong_ying_shang_ming_cheng', 'boolfield_xin_yu_ping_ji', ]
        widgets = {'boolfield_xin_yu_ping_ji': Select, }
    
class Zhi_yuan_ji_ben_xin_xi_biao_ModelForm(ModelForm):
    class Meta:
        model = Zhi_yuan_ji_ben_xin_xi_biao
        fields = ['characterfield_name', 'characterhssc_identification_number', 'characterfield_practice_qualification', 'characterfield_expertise', 'characterfield_practice_time', 'characterfield_contact_number', 'boolfield_zhi_yuan_bian_ma', 'relatedfield_affiliation', 'relatedfield_service_role', ]
        widgets = {'relatedfield_affiliation': Select, 'relatedfield_service_role': CheckboxSelectMultiple, }
    
class She_bei_ji_ben_xin_xi_biao_ModelForm(ModelForm):
    class Meta:
        model = She_bei_ji_ben_xin_xi_biao
        fields = ['characterfield_contact_number', 'boolfield_she_bei_ming_cheng', 'boolfield_she_bei_bian_ma', 'boolfield_sheng_chan_chang_jia', 'boolfield_she_bei_fu_wu_dan_wei_hao_shi', 'boolfield_she_bei_jian_xiu_zhou_qi', 'boolfield_she_bei_shi_yong_cheng_ben', 'boolfield_she_bei_shi_yong_fu_wu_gong_neng', ]
        widgets = {'boolfield_she_bei_shi_yong_fu_wu_gong_neng': Select, }
    
class Yong_yao_diao_cha_biao_ModelForm(ModelForm):
    class Meta:
        model = Yong_yao_diao_cha_biao
        fields = ['relatedfield_drug_name', ]
        widgets = {'relatedfield_drug_name': SelectMultiple, }
    
class T3003_ModelForm(ModelForm):
    class Meta:
        model = T3003
        fields = ['relatedfield_left_foot', 'relatedfield_right_foot', ]
        widgets = {'relatedfield_left_foot': RadioSelect, 'relatedfield_right_foot': RadioSelect, }
    
class T3002_ModelForm(ModelForm):
    class Meta:
        model = T3002
        fields = ['relatedfield_fundus', ]
        widgets = {'relatedfield_fundus': Select, }
    
class Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_biao_ModelForm(ModelForm):
    class Meta:
        model = Fu_wu_fen_gong_ji_gou_ji_ben_xin_xi_biao
        fields = ['characterfield_contact_address', 'characterfield_contact_number', 'boolfield_ji_gou_dai_ma', 'boolfield_ji_gou_shu_xing', 'boolfield_gong_ying_shang_bian_ma', 'boolfield_gong_ying_shang_ming_cheng', 'boolfield_zhuan_ye_fu_wu', 'boolfield_xin_yu_ping_ji', ]
        widgets = {'boolfield_xin_yu_ping_ji': Select, }
    
class A6208_ModelForm(ModelForm):
    class Meta:
        model = A6208
        fields = ['numberfield_blood_transfusion', 'boolfield_shu_xue_ri_qi', ]
        
    
class Z6233_ModelForm(ModelForm):
    class Meta:
        model = Z6233
        fields = ['characterfield_username', 'characterfield_password', ]
        
    
class Yao_pin_ji_ben_xin_xi_biao_ModelForm(ModelForm):
    class Meta:
        model = Yao_pin_ji_ben_xin_xi_biao
        fields = ['boolfield_yao_pin_bian_ma', 'boolfield_yao_pin_gui_ge', 'boolfield_yong_yao_zhou_qi', 'boolfield_chang_yong_chu_fang_liang', 'boolfield_dui_zhao_yi_bao_ming_cheng', 'boolfield_dui_zhao_ji_yao_ming_cheng', 'boolfield_huan_suan_gui_ze', 'boolfield_fu_yong_pin_ci', 'boolfield_chu_fang_ji_liang_dan_wei', 'boolfield_ru_ku_ji_liang_dan_wei', 'boolfield_xiao_shou_ji_liang_dan_wei', 'relatedfield_drug_name', 'boolfield_yong_yao_tu_jing', 'boolfield_yao_pin_fen_lei', ]
        widgets = {'boolfield_chu_fang_ji_liang_dan_wei': Select, 'boolfield_ru_ku_ji_liang_dan_wei': Select, 'boolfield_xiao_shou_ji_liang_dan_wei': Select, 'relatedfield_drug_name': SelectMultiple, 'boolfield_yong_yao_tu_jing': Select, 'boolfield_yao_pin_fen_lei': Select, }
    
class A5001_ModelForm(ModelForm):
    class Meta:
        model = A5001
        fields = ['boolfield_yong_yao_zhou_qi', 'boolfield_chang_yong_chu_fang_liang', 'boolfield_fu_yong_pin_ci', 'relatedfield_drug_name', 'boolfield_yong_yao_tu_jing', ]
        widgets = {'relatedfield_drug_name': SelectMultiple, 'boolfield_yong_yao_tu_jing': Select, }
    
class T4504_ModelForm(ModelForm):
    class Meta:
        model = T4504
        fields = ['T4504', ]
        widgets = {'T4504': SelectMultiple, }
    
class Shu_ye_zhu_she_dan_ModelForm(ModelForm):
    class Meta:
        model = Shu_ye_zhu_she_dan
        fields = ['boolfield_yao_pin_gui_ge', 'boolfield_yong_yao_zhou_qi', 'boolfield_chang_yong_chu_fang_liang', 'boolfield_zhi_xing_qian_ming', 'boolfield_fu_yong_pin_ci', 'boolfield_zhu_she_ri_qi', 'relatedfield_drug_name', ]
        widgets = {'relatedfield_drug_name': SelectMultiple, }
    
class A6219_ModelForm(ModelForm):
    class Meta:
        model = A6219
        fields = ['characterfield_supplementary_description_of_the_condition', 'relatedfield_symptom_list', 'boolfield_tang_niao_bing_zheng_zhuang', ]
        widgets = {'relatedfield_symptom_list': SelectMultiple, 'boolfield_tang_niao_bing_zheng_zhuang': CheckboxSelectMultiple, }
    
class A6203_ModelForm(ModelForm):
    class Meta:
        model = A6203
        fields = ['characterfield_name', 'characterhssc_identification_number', 'characterfield_resident_file_number', 'characterfield_family_address', 'characterfield_contact_number', 'characterfield_medical_ic_card_number', 'datetimefield_date_of_birth', 'relatedfield_gender', 'relatedfield_nationality', 'relatedfield_marital_status', 'relatedfield_education', 'relatedfield_occupational_status', 'relatedfield_medical_expenses_burden', 'relatedfield_type_of_residence', 'relatedfield_blood_type', 'relatedfield_signed_family_doctor', 'relatedfield_family_relationship', ]
        widgets = {'relatedfield_gender': Select, 'relatedfield_nationality': Select, 'relatedfield_marital_status': Select, 'relatedfield_education': Select, 'relatedfield_occupational_status': Select, 'relatedfield_medical_expenses_burden': CheckboxSelectMultiple, 'relatedfield_type_of_residence': Select, 'relatedfield_blood_type': Select, 'relatedfield_signed_family_doctor': Select, 'relatedfield_family_relationship': Select, }
    
class A3001_ModelForm(ModelForm):
    class Meta:
        model = A3001
        fields = ['characterfield_right_eye_vision', 'characterfield_left_eye_vision', 'numberfield_body_temperature', 'numberfield_pulse', 'numberfield_respiratory_rate', 'numberfield_hight', 'numberfield_weight', 'numberfield_body_mass_index', 'numberfield_systolic_blood_pressure', 'numberfield_diastolic_blood_pressure', 'boolfield_yao_wei', 'relatedfield_athletic_ability', 'relatedfield_left_ear_hearing', 'relatedfield_right_ear_hearing', 'relatedfield_lips', 'relatedfield_dentition', 'relatedfield_pharynx', 'relatedfield_lower_extremity_edema', ]
        widgets = {'relatedfield_athletic_ability': Select, 'relatedfield_left_ear_hearing': Select, 'relatedfield_right_ear_hearing': Select, 'relatedfield_lips': RadioSelect, 'relatedfield_dentition': RadioSelect, 'relatedfield_pharynx': Select, 'relatedfield_lower_extremity_edema': RadioSelect, }
    
class A3101_ModelForm(ModelForm):
    class Meta:
        model = A3101
        fields = ['numberfield_hight', 'numberfield_weight', 'numberfield_body_mass_index', ]
        
    
class A6501_ModelForm(ModelForm):
    class Meta:
        model = A6501
        fields = ['datetimefield_ri_qi_shi_jian', 'boolfield_ze_ren_ren', ]
        widgets = {'boolfield_ze_ren_ren': Select, }
    
class T4505_ModelForm(ModelForm):
    class Meta:
        model = T4505
        fields = ['numberfield_kong_fu_xue_tang', ]
        
    
class A6211_ModelForm(ModelForm):
    class Meta:
        model = A6211
        fields = ['datetimefield_date', 'relatedfield_major_life', ]
        widgets = {'relatedfield_major_life': CheckboxSelectMultiple, }
    
class A3502_ModelForm(ModelForm):
    class Meta:
        model = A3502
        fields = ['boolfield_niao_tang', 'boolfield_dan_bai_zhi', 'boolfield_tong_ti', ]
        widgets = {'boolfield_niao_tang': Select, 'boolfield_dan_bai_zhi': Select, 'boolfield_tong_ti': Select, }
    
class T4501_ModelForm(ModelForm):
    class Meta:
        model = T4501
        fields = ['T4501', ]
        widgets = {'T4501': SelectMultiple, }
    
class A6207_ModelForm(ModelForm):
    class Meta:
        model = A6207
        fields = ['relatedfield_drug_name', ]
        widgets = {'relatedfield_drug_name': SelectMultiple, }
    
class A6206_ModelForm(ModelForm):
    class Meta:
        model = A6206
        fields = ['boolfield_wai_shang_ri_qi', 'boolfield_wai_shang_xing_ji_bing', ]
        widgets = {'boolfield_wai_shang_xing_ji_bing': Select, }
    
class A3103_ModelForm(ModelForm):
    class Meta:
        model = A3103
        fields = ['numberfield_body_temperature', 'numberfield_pulse', 'numberfield_respiratory_rate', ]
        
    
class A6215_ModelForm(ModelForm):
    class Meta:
        model = A6215
        fields = ['characterfield_working_hours_per_day', 'relatedfield_are_you_satisfied_with_the_job_and_life', 'relatedfield_are_you_satisfied_with_your_adaptability', ]
        widgets = {'relatedfield_are_you_satisfied_with_the_job_and_life': Select, 'relatedfield_are_you_satisfied_with_your_adaptability': Select, }
    
class Z6201_ModelForm(ModelForm):
    class Meta:
        model = Z6201
        fields = ['characterfield_name', 'characterfield_gender', 'characterfield_age', 'characterhssc_identification_number', 'characterfield_contact_address', 'characterfield_password_setting', 'characterfield_confirm_password', 'datetimefield_date_of_birth', ]
        
    
class T3404_ModelForm(ModelForm):
    class Meta:
        model = T3404
        fields = ['numberfield_kong_fu_xue_tang', ]
        
    
class A3110_ModelForm(ModelForm):
    class Meta:
        model = A3110
        fields = ['relatedfield_left_ear_hearing', 'relatedfield_right_ear_hearing', ]
        widgets = {'relatedfield_left_ear_hearing': Select, 'relatedfield_right_ear_hearing': Select, }
    
class A6216_ModelForm(ModelForm):
    class Meta:
        model = A6216
        fields = ['relatedfield_is_the_living_environment_satisfactory', 'relatedfield_is_the_transportation_convenient', ]
        widgets = {'relatedfield_is_the_living_environment_satisfactory': Select, 'relatedfield_is_the_transportation_convenient': Select, }
    
class A6218_ModelForm(ModelForm):
    class Meta:
        model = A6218
        fields = ['characterfield_supplementary_description_of_the_condition', 'relatedfield_symptom_list', ]
        widgets = {'relatedfield_symptom_list': SelectMultiple, }
    
class A6205_ModelForm(ModelForm):
    class Meta:
        model = A6205
        fields = ['datetimefield_date', 'relatedfield_name_of_operation', ]
        widgets = {'relatedfield_name_of_operation': RadioSelect, }
    
class A6214_ModelForm(ModelForm):
    class Meta:
        model = A6214
        fields = ['relatedfield_own_health', 'relatedfield_compared_to_last_year', 'relatedfield_sports_preference', 'relatedfield_exercise_time', 'relatedfield_have_any_recent_symptoms_of_physical_discomfort', ]
        widgets = {'relatedfield_own_health': RadioSelect, 'relatedfield_compared_to_last_year': Select, 'relatedfield_sports_preference': Select, 'relatedfield_exercise_time': RadioSelect, 'relatedfield_have_any_recent_symptoms_of_physical_discomfort': CheckboxSelectMultiple, }
    
class Z6230_ModelForm(ModelForm):
    class Meta:
        model = Z6230
        fields = ['characterfield_username', 'characterfield_password', ]
        
    
class A3105_ModelForm(ModelForm):
    class Meta:
        model = A3105
        fields = ['numberfield_systolic_blood_pressure', 'numberfield_diastolic_blood_pressure', ]
        
    
class A6217_ModelForm(ModelForm):
    class Meta:
        model = A6217
        fields = ['characterfield_supplementary_description_of_the_condition', 'relatedfield_symptom_list', ]
        widgets = {'relatedfield_symptom_list': SelectMultiple, }
    
class T3405_ModelForm(ModelForm):
    class Meta:
        model = T3405
        fields = ['numberfield_tang_hua_xue_hong_dan_bai', ]
        
    
class A6202_ModelForm(ModelForm):
    class Meta:
        model = A6202
        fields = ['characterfield_supplementary_description_of_the_condition', 'relatedfield_symptom_list', ]
        widgets = {'relatedfield_symptom_list': SelectMultiple, }
    
class A6220_ModelForm(ModelForm):
    class Meta:
        model = A6220
        fields = ['boolfield_yuan_wai_jian_kang_ping_gu', ]
        widgets = {'boolfield_yuan_wai_jian_kang_ping_gu': Select, }
    
class A6212_ModelForm(ModelForm):
    class Meta:
        model = A6212
        fields = ['characterfield_average_sleep_duration', 'characterfield_duration_of_insomnia', 'relatedfield_drinking_frequency', 'relatedfield_smoking_frequency', ]
        widgets = {'relatedfield_drinking_frequency': RadioSelect, 'relatedfield_smoking_frequency': RadioSelect, }
    
class T9001_ModelForm(ModelForm):
    class Meta:
        model = T9001
        fields = ['relatedfield_disease_name', 'relatedfield_yi_lou_zhen_duan', 'relatedfield_pai_chu_zhen_duan', ]
        widgets = {'relatedfield_disease_name': Select, 'relatedfield_yi_lou_zhen_duan': SelectMultiple, 'relatedfield_pai_chu_zhen_duan': SelectMultiple, }
    
class A5002_ModelForm(ModelForm):
    class Meta:
        model = A5002
        fields = ['relatedfield_drug_name', 'relatedfield_disease_name', 'boolfield_shi_fou_ji_xu_shi_yong', ]
        widgets = {'relatedfield_drug_name': SelectMultiple, 'relatedfield_disease_name': Select, 'boolfield_shi_fou_ji_xu_shi_yong': RadioSelect, }
    
class Physical_examination_athletic_ability_ModelForm(ModelForm):
    class Meta:
        model = Physical_examination_athletic_ability
        fields = ['relatedfield_athletic_ability', ]
        widgets = {'relatedfield_athletic_ability': Select, }
    
class A6213_ModelForm(ModelForm):
    class Meta:
        model = A6213
        fields = ['relatedfield_personality_tendency', 'boolfield_shi_mian_qing_kuang', 'boolfield_sheng_huo_gong_zuo_ya_li_qing_kuang', ]
        widgets = {'relatedfield_personality_tendency': RadioSelect, 'boolfield_shi_mian_qing_kuang': RadioSelect, 'boolfield_sheng_huo_gong_zuo_ya_li_qing_kuang': RadioSelect, }
    
class Z6261_ModelForm(ModelForm):
    class Meta:
        model = Z6261
        fields = ['boolfield_jia_ting_qian_yue_fu_wu_xie_yi', 'boolfield_qian_yue_que_ren', 'boolfield_ze_ren_ren', ]
        widgets = {'boolfield_qian_yue_que_ren': Select, 'boolfield_ze_ren_ren': Select, }
    
class A6201_ModelForm(ModelForm):
    class Meta:
        model = A6201
        fields = ['characterfield_supplementary_description_of_the_condition', 'relatedfield_symptom_list', 'boolfield_chang_yong_zheng_zhuang', ]
        widgets = {'relatedfield_symptom_list': SelectMultiple, 'boolfield_chang_yong_zheng_zhuang': CheckboxSelectMultiple, }
    
class A6502_ModelForm(ModelForm):
    class Meta:
        model = A6502
        fields = ['boolfield_qian_dao_que_ren', ]
        widgets = {'boolfield_qian_dao_que_ren': RadioSelect, }
    
class A6204_ModelForm(ModelForm):
    class Meta:
        model = A6204
        fields = ['datetimefield_time_of_diagnosis', 'boolfield_ge_ren_bing_shi', ]
        widgets = {'boolfield_ge_ren_bing_shi': Select, }
    
class T6301_ModelForm(ModelForm):
    class Meta:
        model = T6301
        fields = ['boolfield_fu_yong_pin_ci', 'boolfield_yao_pin_dan_wei', 'relatedfield_drug_name', 'relatedfield_drinking_frequency', 'relatedfield_smoking_frequency', 'boolfield_tang_niao_bing_zheng_zhuang', ]
        widgets = {'boolfield_yao_pin_dan_wei': Select, 'relatedfield_drug_name': SelectMultiple, 'relatedfield_drinking_frequency': RadioSelect, 'relatedfield_smoking_frequency': RadioSelect, 'boolfield_tang_niao_bing_zheng_zhuang': CheckboxSelectMultiple, }
    
class A6210_ModelForm(ModelForm):
    class Meta:
        model = A6210
        fields = ['boolfield_yi_chuan_ji_bing', 'boolfield_yi_chuan_bing_shi_cheng_yuan', ]
        widgets = {'boolfield_yi_chuan_ji_bing': Select, 'boolfield_yi_chuan_bing_shi_cheng_yuan': SelectMultiple, }
    
class A6209_ModelForm(ModelForm):
    class Meta:
        model = A6209
        fields = ['boolfield_jia_zu_xing_ji_bing', 'boolfield_jia_zu_bing_shi_cheng_yuan', ]
        widgets = {'boolfield_jia_zu_xing_ji_bing': Select, 'boolfield_jia_zu_bing_shi_cheng_yuan': SelectMultiple, }
    