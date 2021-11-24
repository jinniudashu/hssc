from django.urls import path
from .views import *

urlpatterns = [
	path('', Index_view.as_view(), name='index'),
	path('index/', Index_view.as_view(), name='index'),
    path('test_operation', Test_operation_CreateView.as_view(), name='test_operation_create_url'),
]