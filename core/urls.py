from django.urls import path
from django.urls.resolvers import URLPattern
from .views import index_customer, get_services_list, new_service, jinshuju_test

# app_name = 'service'
urlpatterns = [	
	path('get_services_list/<int:customer_id>/', get_services_list, name='get_services_list'),
	path('index_customer/', index_customer, name='index_customer'),
    path('new_service/<int:customer_id>/<int:service_id>/<int:recommended_service_id>/', new_service, name='new_service'),
	path('jinshuju_test/', jinshuju_test, name='jinshuju_test'),
]
