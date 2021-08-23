from django.urls import path
from django.urls.resolvers import URLPattern
from .views import *

urlpatterns = [
	path('', index_view, name='index'),
	path('index/', index_view, name='index'),
	path("metadata_follow_up_forms/", Metadata_follow_up_form_ListView.as_view(), name="metadata_follow_up_form_list_url"),
	path("metadata_follow_up_form/create/", Metadata_follow_up_form_CreateView.as_view(), name="metadata_follow_up_form_create_url"),
	path("metadata_follow_up_form/<str:slug>/", Metadata_follow_up_form_DetailView.as_view(), name="metadata_follow_up_form_detail_url"),
	path("metadata_follow_up_form/<str:slug>/update/", Metadata_follow_up_form_UpdateView.as_view(), name="metadata_follow_up_form_update_url"),
	path("metadata_follow_up_form/<str:slug>/delete/", Metadata_follow_up_form_DeleteView.as_view(), name="metadata_follow_up_form_delete_url"),
	path("classification_checklists/", Classification_checklist_ListView.as_view(), name="classification_checklist_list_url"),
	path("classification_checklist/create/", Classification_checklist_CreateView.as_view(), name="classification_checklist_create_url"),
	path("classification_checklist/<str:slug>/", Classification_checklist_DetailView.as_view(), name="classification_checklist_detail_url"),
	path("classification_checklist/<str:slug>/update/", Classification_checklist_UpdateView.as_view(), name="classification_checklist_update_url"),
	path("classification_checklist/<str:slug>/delete/", Classification_checklist_DeleteView.as_view(), name="classification_checklist_delete_url"),
	path("routine_physical_examinations/", Routine_physical_examination_ListView.as_view(), name="routine_physical_examination_list_url"),
	path("routine_physical_examination/create/", Routine_physical_examination_CreateView.as_view(), name="routine_physical_examination_create_url"),
	path("routine_physical_examination/<str:slug>/", Routine_physical_examination_DetailView.as_view(), name="routine_physical_examination_detail_url"),
	path("routine_physical_examination/<str:slug>/update/", Routine_physical_examination_UpdateView.as_view(), name="routine_physical_examination_update_url"),
	path("routine_physical_examination/<str:slug>/delete/", Routine_physical_examination_DeleteView.as_view(), name="routine_physical_examination_delete_url"),
	path("classification_survey_lists/", Classification_survey_list_ListView.as_view(), name="classification_survey_list_list_url"),
	path("classification_survey_list/create/", Classification_survey_list_CreateView.as_view(), name="classification_survey_list_create_url"),
	path("classification_survey_list/<str:slug>/", Classification_survey_list_DetailView.as_view(), name="classification_survey_list_detail_url"),
	path("classification_survey_list/<str:slug>/update/", Classification_survey_list_UpdateView.as_view(), name="classification_survey_list_update_url"),
	path("classification_survey_list/<str:slug>/delete/", Classification_survey_list_DeleteView.as_view(), name="classification_survey_list_delete_url"),
]