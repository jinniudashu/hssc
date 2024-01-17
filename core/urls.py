from django.urls import path
from django.conf.urls import url
from django.urls.resolvers import URLPattern
from .views import index_customer, get_employees, CustomerServiceLogView, MedicineItemView, IcpcItemView

# app_name = 'service'
urlpatterns = [	
	path('index_customer/', index_customer, name='index_customer'),
    path('api/customer_service_log/', CustomerServiceLogView.as_view(), name='customer_service_log'),
    path('api/get_medicine_item/', MedicineItemView.as_view(), name='medicine_item'),
    path('api/get_icpc_item/', IcpcItemView.as_view(), name='icpc_item'),
    path('api/get_employees/', get_employees, name='get_employees'),
    # url("message/$", Message.as_view(), name='message'),
    # url("access/token/$", AccessToken.as_view(), name='token'),
]
