from django.urls import path
from django.urls.resolvers import URLPattern
from .views import Index_staff, htmx_test

# app_name = 'forms'

urlpatterns = [	
	path('', htmx_test, name='htmx_test'),
	path('index_staff/', Index_staff.as_view(), name='index_staff'),
]