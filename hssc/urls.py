from django.contrib import admin
from django.urls import path, include

# from django.conf import settings
# from django.conf.urls.static import static

from core.admin import clinic_site
from .views import index, check_signature

urlpatterns = [
    path('', index, name='index'),
    # path('', check_signature, name='check_signature'),
    path('accounts/', include('registration.backends.simple.urls')),
    path('admin/', admin.site.urls, name='admin'),
	path('clinic/customer_service/<int:customer_id>', clinic_site.customer_service, name='customer_homepage'),
    path('clinic/', clinic_site.urls, name='clinic:index'),
    path('core/', include('core.urls')),
    path("template/", include('core.urls')),
    # path('grappelli/', include('grappelli.urls')),
]

# from django.conf.urls.static import static
# from hssc import settings
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = '智益医养服务供应链管理系统'
admin.site.site_title = 'HSSC'
admin.site.index_title = '系统管理控制台'

# print('settings.DEBUG:', settings.DEBUG)
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     print('urlpatterns:', urlpatterns)
