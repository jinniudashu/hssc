from django.urls import path
from .views import *

urlpatterns = [
	path('', Index_view.as_view(), name='index'),
	path('index/', Index_view.as_view(), name='index'),
    path('test1/create', test1_create, name='test1_create_url'),
    path('test1/<int:id>/update', test1_update, name='test1_update_url'),
    path('test2/create', test2_create, name='test2_create_url'),
    path('test2/<int:id>/update', test2_update, name='test2_update_url'),
    path('test3/create', test3_create, name='test3_create_url'),
    path('test3/<int:id>/update', test3_update, name='test3_update_url'),
]