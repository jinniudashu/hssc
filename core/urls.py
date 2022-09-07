from django.urls import path
from django.conf.urls import url
from django.urls.resolvers import URLPattern
from .views import index_customer, jinshuju_post, test_celery

# app_name = 'service'
urlpatterns = [	
	path('index_customer/', index_customer, name='index_customer'),
	path('jinshuju_post/', jinshuju_post, name='jinshuju_post'),
	path('test_celery/', test_celery, name='test_celery'),
    # url("message/$", Message.as_view(), name='message'),
    # url("access/token/$", AccessToken.as_view(), name='token'),
]
