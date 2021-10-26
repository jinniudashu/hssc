from django.urls import path
from django.urls.resolvers import URLPattern
from .views import *

# app_name = 'forms'

urlpatterns = [
	path('', htmx_test, name='htmx_test'),
]