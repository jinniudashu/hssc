from django.urls import path
from .views import *

urlpatterns = [
	path('', Index_view.as_view(), name='index'),
	path('index/', Index_view.as_view(), name='index'),
    path('guo_min_shi_diao_cha_biao', Guo_min_shi_diao_cha_biao_CreateView.as_view(), name='guo_min_shi_diao_cha_biao_create_url'),
    path('ge_ren_ji_bing_shi_diao_cha_biao', Ge_ren_ji_bing_shi_diao_cha_biao_CreateView.as_view(), name='ge_ren_ji_bing_shi_diao_cha_biao_create_url'),
    path('yuan_qian_wen_zhen_biao', Yuan_qian_wen_zhen_biao_CreateView.as_view(), name='yuan_qian_wen_zhen_biao_create_url'),
    path('bing_li_shou_ye', Bing_li_shou_ye_CreateView.as_view(), name='bing_li_shou_ye_create_url'),
    path('men_zhen_wen_zhen_biao', Men_zhen_wen_zhen_biao_CreateView.as_view(), name='men_zhen_wen_zhen_biao_create_url'),
    path('ju_min_jian_kang_dang_an', Ju_min_jian_kang_dang_an_CreateView.as_view(), name='ju_min_jian_kang_dang_an_create_url'),
    path('ti_jian_cha_ti_biao', Ti_jian_cha_ti_biao_CreateView.as_view(), name='ti_jian_cha_ti_biao_create_url'),
    path('xue_ya_jian_ce_biao', Xue_ya_jian_ce_biao_CreateView.as_view(), name='xue_ya_jian_ce_biao_create_url'),
    path('tang_hua_xue_hong_dan_bai_jian_cha_biao', Tang_hua_xue_hong_dan_bai_jian_cha_biao_CreateView.as_view(), name='tang_hua_xue_hong_dan_bai_jian_cha_biao_create_url'),
    path('kong_fu_xue_tang_jian_cha_biao', Kong_fu_xue_tang_jian_cha_biao_CreateView.as_view(), name='kong_fu_xue_tang_jian_cha_biao_create_url'),
    path('tang_niao_bing_cha_ti_biao', Tang_niao_bing_cha_ti_biao_CreateView.as_view(), name='tang_niao_bing_cha_ti_biao_create_url'),
]