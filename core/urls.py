from django.urls import path
from django.urls.resolvers import URLPattern
from .views import index_customer, jinshuju_test, test_celery

# app_name = 'service'
urlpatterns = [	
	path('index_customer/', index_customer, name='index_customer'),
	path('jinshuju_test/', jinshuju_test, name='jinshuju_test'),
	path('test_celery/', test_celery, name='test_celery'),
]
