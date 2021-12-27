from django.core.management import BaseCommand
import requests


class Command(BaseCommand):
    help = '从设计系统导入forms脚本'

    def handle(self, *args, **kwargs):

        # 获取脚本源码，创建文件
        print('开始导入forms脚本...')
        # url = 'http://127.0.0.1:8000/define/source_codes_list/'
        url = 'https://hssc-formdesign.herokuapp.com/define/source_codes_list/'
        res = requests.get(url)
        res_json = res.json()[0]
        code =eval(res_json['code'])

        for key, value in code.items():
            if key == 'templates':
                for item in value:
                    (k, v), = item.items()
                    self.write_file(f'.\\forms\\templates\\{k}', v)
                    print(k)
            elif key == 'dicts_models':
                self.write_file(f'.\\dictionaries\\models.py', value)
                print(key)
            elif key == 'dicts_admin':
                self.write_file(f'.\\dictionaries\\admin.py', value)
                print(key)
            elif key == 'dicts_data':
                print(value)
            else:
                self.write_file(f'.\\forms\\{key}.py', value)
                print(key)

    def write_file(self, file_name, content):
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)


# form1 = Allergies_history_baseform_ModelForm(self.request.POST, prefix="form1")
# form2 = Out_of_hospital_self_report_survey_baseform_ModelForm(self.request.POST, prefix="form2")
# form3 = Family_history_of_illness_baseform_ModelForm(self.request.POST, prefix="form3")
# form4 = Medical_history_baseform_ModelForm(self.request.POST, prefix="form4")
# form5 = History_of_infectious_diseases_baseform_ModelForm(self.request.POST, prefix="form5")
# form6 = Blood_pressure_monitoring_baseform_ModelForm(self.request.POST, prefix="form6")
# form7 = Men_zhen_wen_zhen_diao_cha_baseform_ModelForm(self.request.POST, prefix="form7")

# form1 = Out_of_hospital_self_report_survey_baseform_ModelForm(self.request.POST, prefix="form1")

# form1 = Allergies_history_baseform_ModelForm(self.request.POST, prefix="form1")
# form2 = Family_history_of_illness_baseform_ModelForm(self.request.POST, prefix="form2")
# form3 = Medical_history_baseform_ModelForm(self.request.POST, prefix="form3")
# form4 = History_of_infectious_diseases_baseform_ModelForm(self.request.POST, prefix="form4")

# form0 = Allergies_history_baseform_ModelForm(self.request.POST, prefix="form0")
# form1 = Personal_comprehensive_psychological_quality_survey_baseform_ModelForm(self.request.POST, prefix="form1")
# form2 = Personal_adaptability_assessment_baseform_ModelForm(self.request.POST, prefix="form2")
# form3 = Personal_health_behavior_survey_baseform_ModelForm(self.request.POST, prefix="form3")
# form4 = Personal_health_assessment_baseform_ModelForm(self.request.POST, prefix="form4")
# form5 = Social_environment_assessment_baseform_ModelForm(self.request.POST, prefix="form5")
# form6 = Family_history_of_illness_baseform_ModelForm(self.request.POST, prefix="form6")
# form7 = History_of_blood_transfusion_baseform_ModelForm(self.request.POST, prefix="form7")
# form8 = History_of_trauma_baseform_ModelForm(self.request.POST, prefix="form8")
# form9 = Medical_history_baseform_ModelForm(self.request.POST, prefix="form9")
# form10 = History_of_infectious_diseases_baseform_ModelForm(self.request.POST, prefix="form10")
# form11 = History_of_surgery_baseform_ModelForm(self.request.POST, prefix="form11")
# form12 = Major_life_events_baseform_ModelForm(self.request.POST, prefix="form12")
# form13 = Basic_personal_information_baseform_ModelForm(self.request.POST, prefix="form13")

# form1 = Fundus_examination_baseform_ModelForm(self.request.POST, prefix="form1")
# form2 = Dorsal_artery_pulsation_examination_baseform_ModelForm(self.request.POST, prefix="form2")

# RadioSelect
# CheckboxSelectMultiple