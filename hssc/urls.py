from django.contrib import admin
from django.urls import path, include

from forms.admin import clinic_site
from .views import index

urlpatterns = [
    path('', index, name='index'),
    path('accounts/', include('registration.backends.simple.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('clinic/', clinic_site.urls, name='clinic'),
    path('clinic/forms/', include('forms.urls')),
    path('core/', include('core.urls')),
    # path('grappelli/', include('grappelli.urls')),
]

admin.site.site_header = '智益医养服务供应链管理系统'
admin.site.site_title = 'HSSC'
admin.site.index_title = '系统管理控制台'