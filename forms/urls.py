from django.urls import path
from .views import *

urlpatterns = [
	path('', Index_view.as_view(), name='index'),
	path('index/', Index_view.as_view(), name='index'),
    path('ge_ren_ji_ben_xin_xi_diao_cha_1638359668', Ge_ren_ji_ben_xin_xi_diao_cha_1638359668_CreateView.as_view(), name='ge_ren_ji_ben_xin_xi_diao_cha_1638359668_create_url'),
    path('ge_ren_ji_bing_shi_1638359691', Ge_ren_ji_bing_shi_1638359691_CreateView.as_view(), name='ge_ren_ji_bing_shi_1638359691_create_url'),
    path('ge_ren_jian_kang_diao_cha_biao_1638361044', Ge_ren_jian_kang_diao_cha_biao_1638361044_CreateView.as_view(), name='ge_ren_jian_kang_diao_cha_biao_1638361044_create_url'),
    path('sfs_1638362066', Sfs_1638362066_CreateView.as_view(), name='sfs_1638362066_create_url'),
]