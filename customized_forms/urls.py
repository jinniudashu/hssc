from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiview, name='apiview'),
    path('character_fields_list/', views.character_fields_list, name='character_fields_list'),
    path('number_fields_list/', views.number_fields_list, name='number_fields_list'),
    path('datetime_fields_list/', views.datetime_fields_list, name='datetime_fields_list'),
    path('choice_fields_list/', views.choice_fields_list, name='choice_fields_list'),
    path('related_fields_list/', views.related_fields_list, name='related_fields_list'),
    path('components_list', views.components_list, name='components_list'),
    path('component_detail/<int:pk>', views.component_detail, name='component_detail'),
    path('base_models_list/', views.base_models_list, name='base_models_list'),
    path('base_forms_list/', views.base_forms_list, name='base_forms_list'),
    path('operand_views_list/', views.operand_views_list, name='operand_views_list'),
]