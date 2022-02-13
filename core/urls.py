from django.urls import path
from django.urls.resolvers import URLPattern
from .views import index_staff, index_customer, htmx_test

# app_name = 'forms'

urlpatterns = [	
	path('', htmx_test, name='htmx_test'),
	path('index_staff/', index_staff, name='index_staff'),
	path('index_customer/', index_customer, name='index_customer'),
]