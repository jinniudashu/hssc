# Generated by Django 3.2.6 on 2021-11-10 03:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forms', '0028_alter_history_of_trauma_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL, verbose_name='客户')),
            ],
            options={
                'verbose_name': '客户登记表',
                'verbose_name_plural': '客户登记表',
            },
        ),
        migrations.RemoveField(
            model_name='basic_personal_information',
            name='family_id',
        ),
        migrations.RemoveField(
            model_name='basic_personal_information',
            name='user',
        ),
        migrations.RemoveField(
            model_name='blood_pressure_monitoring',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='blood_pressure_monitoring',
            name='user',
        ),
        migrations.RemoveField(
            model_name='doctor_login',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='doctor_login',
            name='user',
        ),
        migrations.RemoveField(
            model_name='doctor_registry',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='doctor_registry',
            name='user',
        ),
        migrations.RemoveField(
            model_name='family_survey',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='family_survey',
            name='diseases',
        ),
        migrations.RemoveField(
            model_name='family_survey',
            name='user',
        ),
        migrations.RemoveField(
            model_name='history_of_blood_transfusion',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='history_of_blood_transfusion',
            name='user',
        ),
        migrations.RemoveField(
            model_name='history_of_infectious_diseases',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='history_of_infectious_diseases',
            name='diseases',
        ),
        migrations.RemoveField(
            model_name='history_of_infectious_diseases',
            name='user',
        ),
        migrations.RemoveField(
            model_name='history_of_surgery',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='history_of_surgery',
            name='name_of_operation',
        ),
        migrations.RemoveField(
            model_name='history_of_surgery',
            name='user',
        ),
        migrations.RemoveField(
            model_name='history_of_trauma',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='history_of_trauma',
            name='diseases_name',
        ),
        migrations.RemoveField(
            model_name='history_of_trauma',
            name='user',
        ),
        migrations.RemoveField(
            model_name='major_life_events',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='major_life_events',
            name='user',
        ),
        migrations.RemoveField(
            model_name='medical_history',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='medical_history',
            name='disease_name',
        ),
        migrations.RemoveField(
            model_name='medical_history',
            name='user',
        ),
        migrations.RemoveField(
            model_name='out_of_hospital_self_report_survey',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='out_of_hospital_self_report_survey',
            name='user',
        ),
        migrations.RemoveField(
            model_name='personal_adaptability_assessment',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='personal_adaptability_assessment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='personal_comprehensive_psychological_quality_survey',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='personal_comprehensive_psychological_quality_survey',
            name='user',
        ),
        migrations.RemoveField(
            model_name='personal_health_assessment',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='personal_health_assessment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='personal_health_behavior_survey',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='personal_health_behavior_survey',
            name='user',
        ),
        migrations.RemoveField(
            model_name='physical_examination',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='physical_examination',
            name='user',
        ),
        migrations.RemoveField(
            model_name='physical_examination_abdomen',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='physical_examination_abdomen',
            name='user',
        ),
        migrations.RemoveField(
            model_name='physical_examination_athletic_ability',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='physical_examination_athletic_ability',
            name='user',
        ),
        migrations.RemoveField(
            model_name='physical_examination_diabetes',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='physical_examination_diabetes',
            name='user',
        ),
        migrations.RemoveField(
            model_name='physical_examination_hearing',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='physical_examination_hearing',
            name='user',
        ),
        migrations.RemoveField(
            model_name='physical_examination_limbs',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='physical_examination_limbs',
            name='user',
        ),
        migrations.RemoveField(
            model_name='physical_examination_lungs',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='physical_examination_lungs',
            name='user',
        ),
        migrations.RemoveField(
            model_name='physical_examination_lymph_nodes',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='physical_examination_lymph_nodes',
            name='lymph_nodes',
        ),
        migrations.RemoveField(
            model_name='physical_examination_lymph_nodes',
            name='user',
        ),
        migrations.RemoveField(
            model_name='physical_examination_oral_cavity',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='physical_examination_oral_cavity',
            name='user',
        ),
        migrations.RemoveField(
            model_name='physical_examination_sclera',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='physical_examination_sclera',
            name='sclera',
        ),
        migrations.RemoveField(
            model_name='physical_examination_sclera',
            name='user',
        ),
        migrations.RemoveField(
            model_name='physical_examination_skin',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='physical_examination_skin',
            name='skin',
        ),
        migrations.RemoveField(
            model_name='physical_examination_skin',
            name='user',
        ),
        migrations.RemoveField(
            model_name='physical_examination_spine',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='physical_examination_spine',
            name='user',
        ),
        migrations.RemoveField(
            model_name='physical_examination_vision',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='physical_examination_vision',
            name='user',
        ),
        migrations.RemoveField(
            model_name='social_environment_assessment',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='social_environment_assessment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user_login',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='user_login',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user_registry',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='user_registry',
            name='user',
        ),
        migrations.RemoveField(
            model_name='vital_signs_check',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='vital_signs_check',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='staff',
            options={'verbose_name': '员工基本情况', 'verbose_name_plural': '员工基本情况'},
        ),
        migrations.AddField(
            model_name='staff',
            name='group',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='组别'),
        ),
        migrations.DeleteModel(
            name='Allergies_history',
        ),
        migrations.DeleteModel(
            name='Basic_personal_information',
        ),
        migrations.DeleteModel(
            name='Blood_pressure_monitoring',
        ),
        migrations.DeleteModel(
            name='Doctor_login',
        ),
        migrations.DeleteModel(
            name='Doctor_registry',
        ),
        migrations.DeleteModel(
            name='Family_survey',
        ),
        migrations.DeleteModel(
            name='History_of_blood_transfusion',
        ),
        migrations.DeleteModel(
            name='History_of_infectious_diseases',
        ),
        migrations.DeleteModel(
            name='History_of_surgery',
        ),
        migrations.DeleteModel(
            name='History_of_trauma',
        ),
        migrations.DeleteModel(
            name='Major_life_events',
        ),
        migrations.DeleteModel(
            name='Medical_history',
        ),
        migrations.DeleteModel(
            name='Out_of_hospital_self_report_survey',
        ),
        migrations.DeleteModel(
            name='Personal_adaptability_assessment',
        ),
        migrations.DeleteModel(
            name='Personal_comprehensive_psychological_quality_survey',
        ),
        migrations.DeleteModel(
            name='Personal_health_assessment',
        ),
        migrations.DeleteModel(
            name='Personal_health_behavior_survey',
        ),
        migrations.DeleteModel(
            name='Physical_examination',
        ),
        migrations.DeleteModel(
            name='Physical_examination_abdomen',
        ),
        migrations.DeleteModel(
            name='Physical_examination_athletic_ability',
        ),
        migrations.DeleteModel(
            name='Physical_examination_diabetes',
        ),
        migrations.DeleteModel(
            name='Physical_examination_hearing',
        ),
        migrations.DeleteModel(
            name='Physical_examination_limbs',
        ),
        migrations.DeleteModel(
            name='Physical_examination_lungs',
        ),
        migrations.DeleteModel(
            name='Physical_examination_lymph_nodes',
        ),
        migrations.DeleteModel(
            name='Physical_examination_oral_cavity',
        ),
        migrations.DeleteModel(
            name='Physical_examination_sclera',
        ),
        migrations.DeleteModel(
            name='Physical_examination_skin',
        ),
        migrations.DeleteModel(
            name='Physical_examination_spine',
        ),
        migrations.DeleteModel(
            name='Physical_examination_vision',
        ),
        migrations.DeleteModel(
            name='Social_environment_assessment',
        ),
        migrations.DeleteModel(
            name='User_login',
        ),
        migrations.DeleteModel(
            name='User_registry',
        ),
        migrations.DeleteModel(
            name='Vital_signs_check',
        ),
    ]
