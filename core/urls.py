from django.urls import path
from django.urls.resolvers import URLPattern
from .views import index_customer, get_services, new_service

# app_name = 'core'

urlpatterns = [	
	path('get_services/<int:customer_id>/', get_services, name='get_services'),
	path('index_customer/', index_customer, name='index_customer'),
    path('new_service/<int:customer_id>/<int:service_id>/', new_service, name='new_service'),
]