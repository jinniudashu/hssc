from django.contrib import admin
from django.urls import path, include

from .views import index

urlpatterns = [
    path('', index, name='index'),
    path('accounts/', include('registration.backends.simple.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('forms/', include('forms.urls')),
    path('core/', include('core.urls')),
    # path('grappelli/', include('grappelli.urls')),
]

admin.site.site_header = '智益医养服务供应链管理系统'
admin.site.site_title = 'HSSC'
admin.site.index_title = '系统管理控制台'