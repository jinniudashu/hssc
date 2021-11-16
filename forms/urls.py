from django.urls import path
from .views import *

urlpatterns = [
	path('', Index_view.as_view(), name='index'),
	path('index/', Index_view.as_view(), name='index'),
    path('test_operation3', Test_operation3_CreateView.as_view(), name='test_operation3_create_url'),
    path('test_operation_form3', Test_operation_form3_CreateView.as_view(), name='test_operation_form3_create_url'),
    path('test', Test_CreateView.as_view(), name='test_create_url'),
    path('persen', Persen_CreateView.as_view(), name='persen_create_url'),
]