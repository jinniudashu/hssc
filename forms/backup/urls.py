from django.urls import path
from django.urls.resolvers import URLPattern
from .views import *

# app_name = 'forms'

urlpatterns = [
	path('', Index_view.as_view(), name='index'),
	path('index/', Index_view.as_view(), name='index'),
	path('test_operation', Test_operation_CreateView.as_view(), name='test_operation_create_url'),
	path("history_of_traumas/", History_of_trauma_ListView.as_view(), name="history_of_trauma_list_url"),
	path("history_of_trauma/create/", History_of_trauma_CreateView.as_view(), name="history_of_trauma_create_url"),
	path("history_of_trauma/<str:slug>/", History_of_trauma_DetailView.as_view(), name="history_of_trauma_detail_url"),
	path("history_of_trauma/<str:slug>/update/", History_of_trauma_UpdateView.as_view(), name="history_of_trauma_update_url"),
	path("history_of_trauma/<str:slug>/delete/", History_of_trauma_DeleteView.as_view(), name="history_of_trauma_delete_url"),
	path("out_of_hospital_self_report_surveys/", Out_of_hospital_self_report_survey_ListView.as_view(), name="out_of_hospital_self_report_survey_list_url"),
	path("out_of_hospital_self_report_survey/create/", Out_of_hospital_self_report_survey_CreateView.as_view(), name="out_of_hospital_self_report_survey_create_url"),
	path("out_of_hospital_self_report_survey/<str:slug>/", Out_of_hospital_self_report_survey_DetailView.as_view(), name="out_of_hospital_self_report_survey_detail_url"),
	path("out_of_hospital_self_report_survey/<str:slug>/update/", Out_of_hospital_self_report_survey_UpdateView.as_view(), name="out_of_hospital_self_report_survey_update_url"),
	path("out_of_hospital_self_report_survey/<str:slug>/delete/", Out_of_hospital_self_report_survey_DeleteView.as_view(), name="out_of_hospital_self_report_survey_delete_url"),
	path("personal_comprehensive_psychological_quality_surveys/", Personal_comprehensive_psychological_quality_survey_ListView.as_view(), name="personal_comprehensive_psychological_quality_survey_list_url"),
	path("personal_comprehensive_psychological_quality_survey/create/", Personal_comprehensive_psychological_quality_survey_CreateView.as_view(), name="personal_comprehensive_psychological_quality_survey_create_url"),
	path("personal_comprehensive_psychological_quality_survey/<str:slug>/", Personal_comprehensive_psychological_quality_survey_DetailView.as_view(), name="personal_comprehensive_psychological_quality_survey_detail_url"),
	path("personal_comprehensive_psychological_quality_survey/<str:slug>/update/", Personal_comprehensive_psychological_quality_survey_UpdateView.as_view(), name="personal_comprehensive_psychological_quality_survey_update_url"),
	path("personal_comprehensive_psychological_quality_survey/<str:slug>/delete/", Personal_comprehensive_psychological_quality_survey_DeleteView.as_view(), name="personal_comprehensive_psychological_quality_survey_delete_url"),
	path("personal_health_assessments/", Personal_health_assessment_ListView.as_view(), name="personal_health_assessment_list_url"),
	path("personal_health_assessment/create/", Personal_health_assessment_CreateView.as_view(), name="personal_health_assessment_create_url"),
	path("personal_health_assessment/<str:slug>/", Personal_health_assessment_DetailView.as_view(), name="personal_health_assessment_detail_url"),
	path("personal_health_assessment/<str:slug>/update/", Personal_health_assessment_UpdateView.as_view(), name="personal_health_assessment_update_url"),
	path("personal_health_assessment/<str:slug>/delete/", Personal_health_assessment_DeleteView.as_view(), name="personal_health_assessment_delete_url"),
	path("allergies_historys/", Allergies_history_ListView.as_view(), name="allergies_history_list_url"),
	path("allergies_history/create/", Allergies_history_CreateView.as_view(), name="allergies_history_create_url"),
	path("allergies_history/<str:slug>/", Allergies_history_DetailView.as_view(), name="allergies_history_detail_url"),
	path("allergies_history/<str:slug>/update/", Allergies_history_UpdateView.as_view(), name="allergies_history_update_url"),
	path("allergies_history/<str:slug>/delete/", Allergies_history_DeleteView.as_view(), name="allergies_history_delete_url"),
	path("personal_health_behavior_surveys/", Personal_health_behavior_survey_ListView.as_view(), name="personal_health_behavior_survey_list_url"),
	path("personal_health_behavior_survey/create/", Personal_health_behavior_survey_CreateView.as_view(), name="personal_health_behavior_survey_create_url"),
	path("personal_health_behavior_survey/<str:slug>/", Personal_health_behavior_survey_DetailView.as_view(), name="personal_health_behavior_survey_detail_url"),
	path("personal_health_behavior_survey/<str:slug>/update/", Personal_health_behavior_survey_UpdateView.as_view(), name="personal_health_behavior_survey_update_url"),
	path("personal_health_behavior_survey/<str:slug>/delete/", Personal_health_behavior_survey_DeleteView.as_view(), name="personal_health_behavior_survey_delete_url"),
	path("history_of_blood_transfusions/", History_of_blood_transfusion_ListView.as_view(), name="history_of_blood_transfusion_list_url"),
	path("history_of_blood_transfusion/create/", History_of_blood_transfusion_CreateView.as_view(), name="history_of_blood_transfusion_create_url"),
	path("history_of_blood_transfusion/<str:slug>/", History_of_blood_transfusion_DetailView.as_view(), name="history_of_blood_transfusion_detail_url"),
	path("history_of_blood_transfusion/<str:slug>/update/", History_of_blood_transfusion_UpdateView.as_view(), name="history_of_blood_transfusion_update_url"),
	path("history_of_blood_transfusion/<str:slug>/delete/", History_of_blood_transfusion_DeleteView.as_view(), name="history_of_blood_transfusion_delete_url"),
	path("social_environment_assessments/", Social_environment_assessment_ListView.as_view(), name="social_environment_assessment_list_url"),
	path("social_environment_assessment/create/", Social_environment_assessment_CreateView.as_view(), name="social_environment_assessment_create_url"),
	path("social_environment_assessment/<str:slug>/", Social_environment_assessment_DetailView.as_view(), name="social_environment_assessment_detail_url"),
	path("social_environment_assessment/<str:slug>/update/", Social_environment_assessment_UpdateView.as_view(), name="social_environment_assessment_update_url"),
	path("social_environment_assessment/<str:slug>/delete/", Social_environment_assessment_DeleteView.as_view(), name="social_environment_assessment_delete_url"),
	path("medical_historys/", Medical_history_ListView.as_view(), name="medical_history_list_url"),
	path("medical_history/create/", Medical_history_CreateView.as_view(), name="medical_history_create_url"),
	path("medical_history/<str:slug>/", Medical_history_DetailView.as_view(), name="medical_history_detail_url"),
	path("medical_history/<str:slug>/update/", Medical_history_UpdateView.as_view(), name="medical_history_update_url"),
	path("medical_history/<str:slug>/delete/", Medical_history_DeleteView.as_view(), name="medical_history_delete_url"),
	path("major_life_eventss/", Major_life_events_ListView.as_view(), name="major_life_events_list_url"),
	path("major_life_events/create/", Major_life_events_CreateView.as_view(), name="major_life_events_create_url"),
	path("major_life_events/<str:slug>/", Major_life_events_DetailView.as_view(), name="major_life_events_detail_url"),
	path("major_life_events/<str:slug>/update/", Major_life_events_UpdateView.as_view(), name="major_life_events_update_url"),
	path("major_life_events/<str:slug>/delete/", Major_life_events_DeleteView.as_view(), name="major_life_events_delete_url"),
	path("physical_examination_visions/", Physical_examination_vision_ListView.as_view(), name="physical_examination_vision_list_url"),
	path("physical_examination_vision/create/", Physical_examination_vision_CreateView.as_view(), name="physical_examination_vision_create_url"),
	path("physical_examination_vision/<str:slug>/", Physical_examination_vision_DetailView.as_view(), name="physical_examination_vision_detail_url"),
	path("physical_examination_vision/<str:slug>/update/", Physical_examination_vision_UpdateView.as_view(), name="physical_examination_vision_update_url"),
	path("physical_examination_vision/<str:slug>/delete/", Physical_examination_vision_DeleteView.as_view(), name="physical_examination_vision_delete_url"),
	path("family_surveys/", Family_survey_ListView.as_view(), name="family_survey_list_url"),
	path("family_survey/create/", Family_survey_CreateView.as_view(), name="family_survey_create_url"),
	path("family_survey/<str:slug>/", Family_survey_DetailView.as_view(), name="family_survey_detail_url"),
	path("family_survey/<str:slug>/update/", Family_survey_UpdateView.as_view(), name="family_survey_update_url"),
	path("family_survey/<str:slug>/delete/", Family_survey_DeleteView.as_view(), name="family_survey_delete_url"),
	path("history_of_surgerys/", History_of_surgery_ListView.as_view(), name="history_of_surgery_list_url"),
	path("history_of_surgery/create/", History_of_surgery_CreateView.as_view(), name="history_of_surgery_create_url"),
	path("history_of_surgery/<str:slug>/", History_of_surgery_DetailView.as_view(), name="history_of_surgery_detail_url"),
	path("history_of_surgery/<str:slug>/update/", History_of_surgery_UpdateView.as_view(), name="history_of_surgery_update_url"),
	path("history_of_surgery/<str:slug>/delete/", History_of_surgery_DeleteView.as_view(), name="history_of_surgery_delete_url"),
	path("blood_pressure_monitorings/", Blood_pressure_monitoring_ListView.as_view(), name="blood_pressure_monitoring_list_url"),
	path("blood_pressure_monitoring/create/", Blood_pressure_monitoring_CreateView.as_view(), name="blood_pressure_monitoring_create_url"),
	path("blood_pressure_monitoring/<str:slug>/", Blood_pressure_monitoring_DetailView.as_view(), name="blood_pressure_monitoring_detail_url"),
	path("blood_pressure_monitoring/<str:slug>/update/", Blood_pressure_monitoring_UpdateView.as_view(), name="blood_pressure_monitoring_update_url"),
	path("blood_pressure_monitoring/<str:slug>/delete/", Blood_pressure_monitoring_DeleteView.as_view(), name="blood_pressure_monitoring_delete_url"),
	path("user_registrys/", User_registry_ListView.as_view(), name="user_registry_list_url"),
	path("user_registry/create/", User_registry_CreateView.as_view(), name="user_registry_create_url"),
	path("user_registry/<str:slug>/", User_registry_DetailView.as_view(), name="user_registry_detail_url"),
	path("user_registry/<str:slug>/update/", User_registry_UpdateView.as_view(), name="user_registry_update_url"),
	path("user_registry/<str:slug>/delete/", User_registry_DeleteView.as_view(), name="user_registry_delete_url"),
	path("doctor_registrys/", Doctor_registry_ListView.as_view(), name="doctor_registry_list_url"),
	path("doctor_registry/create/", Doctor_registry_CreateView.as_view(), name="doctor_registry_create_url"),
	path("doctor_registry/<str:slug>/", Doctor_registry_DetailView.as_view(), name="doctor_registry_detail_url"),
	path("doctor_registry/<str:slug>/update/", Doctor_registry_UpdateView.as_view(), name="doctor_registry_update_url"),
	path("doctor_registry/<str:slug>/delete/", Doctor_registry_DeleteView.as_view(), name="doctor_registry_delete_url"),
	path("user_logins/", User_login_ListView.as_view(), name="user_login_list_url"),
	path("user_login/create/", User_login_CreateView.as_view(), name="user_login_create_url"),
	path("user_login/<str:slug>/", User_login_DetailView.as_view(), name="user_login_detail_url"),
	path("user_login/<str:slug>/update/", User_login_UpdateView.as_view(), name="user_login_update_url"),
	path("user_login/<str:slug>/delete/", User_login_DeleteView.as_view(), name="user_login_delete_url"),
	path("doctor_logins/", Doctor_login_ListView.as_view(), name="doctor_login_list_url"),
	path("doctor_login/create/", Doctor_login_CreateView.as_view(), name="doctor_login_create_url"),
	path("doctor_login/<str:slug>/", Doctor_login_DetailView.as_view(), name="doctor_login_detail_url"),
	path("doctor_login/<str:slug>/update/", Doctor_login_UpdateView.as_view(), name="doctor_login_update_url"),
	path("doctor_login/<str:slug>/delete/", Doctor_login_DeleteView.as_view(), name="doctor_login_delete_url"),
	path("vital_signs_checks/", Vital_signs_check_ListView.as_view(), name="vital_signs_check_list_url"),
	path("vital_signs_check/create/", Vital_signs_check_CreateView.as_view(), name="vital_signs_check_create_url"),
	path("vital_signs_check/<str:slug>/", Vital_signs_check_DetailView.as_view(), name="vital_signs_check_detail_url"),
	path("vital_signs_check/<str:slug>/update/", Vital_signs_check_UpdateView.as_view(), name="vital_signs_check_update_url"),
	path("vital_signs_check/<str:slug>/delete/", Vital_signs_check_DeleteView.as_view(), name="vital_signs_check_delete_url"),
	path("physical_examination_hearings/", Physical_examination_hearing_ListView.as_view(), name="physical_examination_hearing_list_url"),
	path("physical_examination_hearing/create/", Physical_examination_hearing_CreateView.as_view(), name="physical_examination_hearing_create_url"),
	path("physical_examination_hearing/<str:slug>/", Physical_examination_hearing_DetailView.as_view(), name="physical_examination_hearing_detail_url"),
	path("physical_examination_hearing/<str:slug>/update/", Physical_examination_hearing_UpdateView.as_view(), name="physical_examination_hearing_update_url"),
	path("physical_examination_hearing/<str:slug>/delete/", Physical_examination_hearing_DeleteView.as_view(), name="physical_examination_hearing_delete_url"),
	path("basic_personal_informations/", Basic_personal_information_ListView.as_view(), name="basic_personal_information_list_url"),
	path("basic_personal_information/create/", Basic_personal_information_CreateView.as_view(), name="basic_personal_information_create_url"),
	path("basic_personal_information/<str:slug>/", Basic_personal_information_DetailView.as_view(), name="basic_personal_information_detail_url"),
	path("basic_personal_information/<str:slug>/update/", Basic_personal_information_UpdateView.as_view(), name="basic_personal_information_update_url"),
	path("basic_personal_information/<str:slug>/delete/", Basic_personal_information_DeleteView.as_view(), name="basic_personal_information_delete_url"),
	path("history_of_infectious_diseasess/", History_of_infectious_diseases_ListView.as_view(), name="history_of_infectious_diseases_list_url"),
	path("history_of_infectious_diseases/create/", History_of_infectious_diseases_CreateView.as_view(), name="history_of_infectious_diseases_create_url"),
	path("history_of_infectious_diseases/<str:slug>/", History_of_infectious_diseases_DetailView.as_view(), name="history_of_infectious_diseases_detail_url"),
	path("history_of_infectious_diseases/<str:slug>/update/", History_of_infectious_diseases_UpdateView.as_view(), name="history_of_infectious_diseases_update_url"),
	path("history_of_infectious_diseases/<str:slug>/delete/", History_of_infectious_diseases_DeleteView.as_view(), name="history_of_infectious_diseases_delete_url"),
	path("physical_examinations/", Physical_examination_ListView.as_view(), name="physical_examination_list_url"),
	path("physical_examination/create/", Physical_examination_CreateView.as_view(), name="physical_examination_create_url"),
	path("physical_examination/<str:slug>/", Physical_examination_DetailView.as_view(), name="physical_examination_detail_url"),
	path("physical_examination/<str:slug>/update/", Physical_examination_UpdateView.as_view(), name="physical_examination_update_url"),
	path("physical_examination/<str:slug>/delete/", Physical_examination_DeleteView.as_view(), name="physical_examination_delete_url"),
	path("personal_adaptability_assessments/", Personal_adaptability_assessment_ListView.as_view(), name="personal_adaptability_assessment_list_url"),
	path("personal_adaptability_assessment/create/", Personal_adaptability_assessment_CreateView.as_view(), name="personal_adaptability_assessment_create_url"),
	path("personal_adaptability_assessment/<str:slug>/", Personal_adaptability_assessment_DetailView.as_view(), name="personal_adaptability_assessment_detail_url"),
	path("personal_adaptability_assessment/<str:slug>/update/", Personal_adaptability_assessment_UpdateView.as_view(), name="personal_adaptability_assessment_update_url"),
	path("personal_adaptability_assessment/<str:slug>/delete/", Personal_adaptability_assessment_DeleteView.as_view(), name="personal_adaptability_assessment_delete_url"),
	path("physical_examination_abdomens/", Physical_examination_abdomen_ListView.as_view(), name="physical_examination_abdomen_list_url"),
	path("physical_examination_abdomen/create/", Physical_examination_abdomen_CreateView.as_view(), name="physical_examination_abdomen_create_url"),
	path("physical_examination_abdomen/<str:slug>/", Physical_examination_abdomen_DetailView.as_view(), name="physical_examination_abdomen_detail_url"),
	path("physical_examination_abdomen/<str:slug>/update/", Physical_examination_abdomen_UpdateView.as_view(), name="physical_examination_abdomen_update_url"),
	path("physical_examination_abdomen/<str:slug>/delete/", Physical_examination_abdomen_DeleteView.as_view(), name="physical_examination_abdomen_delete_url"),
	path("physical_examination_athletic_abilitys/", Physical_examination_athletic_ability_ListView.as_view(), name="physical_examination_athletic_ability_list_url"),
	path("physical_examination_athletic_ability/create/", Physical_examination_athletic_ability_CreateView.as_view(), name="physical_examination_athletic_ability_create_url"),
	path("physical_examination_athletic_ability/<str:slug>/", Physical_examination_athletic_ability_DetailView.as_view(), name="physical_examination_athletic_ability_detail_url"),
	path("physical_examination_athletic_ability/<str:slug>/update/", Physical_examination_athletic_ability_UpdateView.as_view(), name="physical_examination_athletic_ability_update_url"),
	path("physical_examination_athletic_ability/<str:slug>/delete/", Physical_examination_athletic_ability_DeleteView.as_view(), name="physical_examination_athletic_ability_delete_url"),
	path("physical_examination_oral_cavitys/", Physical_examination_oral_cavity_ListView.as_view(), name="physical_examination_oral_cavity_list_url"),
	path("physical_examination_oral_cavity/create/", Physical_examination_oral_cavity_CreateView.as_view(), name="physical_examination_oral_cavity_create_url"),
	path("physical_examination_oral_cavity/<str:slug>/", Physical_examination_oral_cavity_DetailView.as_view(), name="physical_examination_oral_cavity_detail_url"),
	path("physical_examination_oral_cavity/<str:slug>/update/", Physical_examination_oral_cavity_UpdateView.as_view(), name="physical_examination_oral_cavity_update_url"),
	path("physical_examination_oral_cavity/<str:slug>/delete/", Physical_examination_oral_cavity_DeleteView.as_view(), name="physical_examination_oral_cavity_delete_url"),
	path("physical_examination_lungss/", Physical_examination_lungs_ListView.as_view(), name="physical_examination_lungs_list_url"),
	path("physical_examination_lungs/create/", Physical_examination_lungs_CreateView.as_view(), name="physical_examination_lungs_create_url"),
	path("physical_examination_lungs/<str:slug>/", Physical_examination_lungs_DetailView.as_view(), name="physical_examination_lungs_detail_url"),
	path("physical_examination_lungs/<str:slug>/update/", Physical_examination_lungs_UpdateView.as_view(), name="physical_examination_lungs_update_url"),
	path("physical_examination_lungs/<str:slug>/delete/", Physical_examination_lungs_DeleteView.as_view(), name="physical_examination_lungs_delete_url"),
	path("physical_examination_limbss/", Physical_examination_limbs_ListView.as_view(), name="physical_examination_limbs_list_url"),
	path("physical_examination_limbs/create/", Physical_examination_limbs_CreateView.as_view(), name="physical_examination_limbs_create_url"),
	path("physical_examination_limbs/<str:slug>/", Physical_examination_limbs_DetailView.as_view(), name="physical_examination_limbs_detail_url"),
	path("physical_examination_limbs/<str:slug>/update/", Physical_examination_limbs_UpdateView.as_view(), name="physical_examination_limbs_update_url"),
	path("physical_examination_limbs/<str:slug>/delete/", Physical_examination_limbs_DeleteView.as_view(), name="physical_examination_limbs_delete_url"),
	path("physical_examination_skins/", Physical_examination_skin_ListView.as_view(), name="physical_examination_skin_list_url"),
	path("physical_examination_skin/create/", Physical_examination_skin_CreateView.as_view(), name="physical_examination_skin_create_url"),
	path("physical_examination_skin/<str:slug>/", Physical_examination_skin_DetailView.as_view(), name="physical_examination_skin_detail_url"),
	path("physical_examination_skin/<str:slug>/update/", Physical_examination_skin_UpdateView.as_view(), name="physical_examination_skin_update_url"),
	path("physical_examination_skin/<str:slug>/delete/", Physical_examination_skin_DeleteView.as_view(), name="physical_examination_skin_delete_url"),
	path("physical_examination_scleras/", Physical_examination_sclera_ListView.as_view(), name="physical_examination_sclera_list_url"),
	path("physical_examination_sclera/create/", Physical_examination_sclera_CreateView.as_view(), name="physical_examination_sclera_create_url"),
	path("physical_examination_sclera/<str:slug>/", Physical_examination_sclera_DetailView.as_view(), name="physical_examination_sclera_detail_url"),
	path("physical_examination_sclera/<str:slug>/update/", Physical_examination_sclera_UpdateView.as_view(), name="physical_examination_sclera_update_url"),
	path("physical_examination_sclera/<str:slug>/delete/", Physical_examination_sclera_DeleteView.as_view(), name="physical_examination_sclera_delete_url"),
	path("physical_examination_lymph_nodess/", Physical_examination_lymph_nodes_ListView.as_view(), name="physical_examination_lymph_nodes_list_url"),
	path("physical_examination_lymph_nodes/create/", Physical_examination_lymph_nodes_CreateView.as_view(), name="physical_examination_lymph_nodes_create_url"),
	path("physical_examination_lymph_nodes/<str:slug>/", Physical_examination_lymph_nodes_DetailView.as_view(), name="physical_examination_lymph_nodes_detail_url"),
	path("physical_examination_lymph_nodes/<str:slug>/update/", Physical_examination_lymph_nodes_UpdateView.as_view(), name="physical_examination_lymph_nodes_update_url"),
	path("physical_examination_lymph_nodes/<str:slug>/delete/", Physical_examination_lymph_nodes_DeleteView.as_view(), name="physical_examination_lymph_nodes_delete_url"),
	path("physical_examination_spines/", Physical_examination_spine_ListView.as_view(), name="physical_examination_spine_list_url"),
	path("physical_examination_spine/create/", Physical_examination_spine_CreateView.as_view(), name="physical_examination_spine_create_url"),
	path("physical_examination_spine/<str:slug>/", Physical_examination_spine_DetailView.as_view(), name="physical_examination_spine_detail_url"),
	path("physical_examination_spine/<str:slug>/update/", Physical_examination_spine_UpdateView.as_view(), name="physical_examination_spine_update_url"),
	path("physical_examination_spine/<str:slug>/delete/", Physical_examination_spine_DeleteView.as_view(), name="physical_examination_spine_delete_url"),
	path("dorsal_artery_pulsation_examinations/", Dorsal_artery_pulsation_examination_ListView.as_view(), name="dorsal_artery_pulsation_examination_list_url"),
	path("dorsal_artery_pulsation_examination/create/", Dorsal_artery_pulsation_examination_CreateView.as_view(), name="dorsal_artery_pulsation_examination_create_url"),
	path("dorsal_artery_pulsation_examination/<str:slug>/", Dorsal_artery_pulsation_examination_DetailView.as_view(), name="dorsal_artery_pulsation_examination_detail_url"),
	path("dorsal_artery_pulsation_examination/<str:slug>/update/", Dorsal_artery_pulsation_examination_UpdateView.as_view(), name="dorsal_artery_pulsation_examination_update_url"),
	path("dorsal_artery_pulsation_examination/<str:slug>/delete/", Dorsal_artery_pulsation_examination_DeleteView.as_view(), name="dorsal_artery_pulsation_examination_delete_url"),
	path("routine_blood_tests/", Routine_blood_test_ListView.as_view(), name="routine_blood_test_list_url"),
	path("routine_blood_test/create/", Routine_blood_test_CreateView.as_view(), name="routine_blood_test_create_url"),
	path("routine_blood_test/<str:slug>/", Routine_blood_test_DetailView.as_view(), name="routine_blood_test_detail_url"),
	path("routine_blood_test/<str:slug>/update/", Routine_blood_test_UpdateView.as_view(), name="routine_blood_test_update_url"),
	path("routine_blood_test/<str:slug>/delete/", Routine_blood_test_DeleteView.as_view(), name="routine_blood_test_delete_url"),
	path("fundus_examinations/", Fundus_examination_ListView.as_view(), name="fundus_examination_list_url"),
	path("fundus_examination/create/", Fundus_examination_CreateView.as_view(), name="fundus_examination_create_url"),
	path("fundus_examination/<str:slug>/", Fundus_examination_DetailView.as_view(), name="fundus_examination_detail_url"),
	path("fundus_examination/<str:slug>/update/", Fundus_examination_UpdateView.as_view(), name="fundus_examination_update_url"),
	path("fundus_examination/<str:slug>/delete/", Fundus_examination_DeleteView.as_view(), name="fundus_examination_delete_url"),
	path("lower_extremity_edema_examinations/", Lower_extremity_edema_examination_ListView.as_view(), name="lower_extremity_edema_examination_list_url"),
	path("lower_extremity_edema_examination/create/", Lower_extremity_edema_examination_CreateView.as_view(), name="lower_extremity_edema_examination_create_url"),
	path("lower_extremity_edema_examination/<str:slug>/", Lower_extremity_edema_examination_DetailView.as_view(), name="lower_extremity_edema_examination_detail_url"),
	path("lower_extremity_edema_examination/<str:slug>/update/", Lower_extremity_edema_examination_UpdateView.as_view(), name="lower_extremity_edema_examination_update_url"),
	path("lower_extremity_edema_examination/<str:slug>/delete/", Lower_extremity_edema_examination_DeleteView.as_view(), name="lower_extremity_edema_examination_delete_url"),
]