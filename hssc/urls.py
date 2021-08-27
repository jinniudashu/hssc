from django.contrib import admin
from django.urls import path, include

# from .views import redirect_blog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('icpc_update/', include('icpc.urls')),
    # path('grappelli/', include('grappelli.urls')),
    path('', include('forms.urls')),
]

admin.site.site_header = '智益医养服务供应链管理系统'
admin.site.site_title = 'HSSC'
admin.site.index_title = '系统管理控制台'