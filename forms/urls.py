from django.urls import path
from .views import *

urlpatterns = [
	path('', Index_view.as_view(), name='index'),
	path('index/', Index_view.as_view(), name='index'),
    path('yuan_qian_zheng_zhuang_diao_cha_biao', Yuan_qian_zheng_zhuang_diao_cha_biao_CreateView.as_view(), name='yuan_qian_zheng_zhuang_diao_cha_biao_create_url'),
    path('guo_min_shi_diao_cha_biao', Guo_min_shi_diao_cha_biao_CreateView.as_view(), name='guo_min_shi_diao_cha_biao_create_url'),
    path('ge_ren_ji_bing_shi_diao_cha_biao', Ge_ren_ji_bing_shi_diao_cha_biao_CreateView.as_view(), name='ge_ren_ji_bing_shi_diao_cha_biao_create_url'),
    path('ge_ren_jian_kang_xing_wei_diao_cha_biao', Ge_ren_jian_kang_xing_wei_diao_cha_biao_CreateView.as_view(), name='ge_ren_jian_kang_xing_wei_diao_cha_biao_create_url'),
    path('yuan_nei_wen_zhen_diao_cha_biao', Yuan_nei_wen_zhen_diao_cha_biao_CreateView.as_view(), name='yuan_nei_wen_zhen_diao_cha_biao_create_url'),
    path('chang_gui_cha_ti_biao', Chang_gui_cha_ti_biao_CreateView.as_view(), name='chang_gui_cha_ti_biao_create_url'),
    path('tang_niao_bing_cha_ti_biao', Tang_niao_bing_cha_ti_biao_CreateView.as_view(), name='tang_niao_bing_cha_ti_biao_create_url'),
    path('xue_ya_jian_ce_biao', Xue_ya_jian_ce_biao_CreateView.as_view(), name='xue_ya_jian_ce_biao_create_url'),
    path('kong_fu_xue_tang_jian_cha_biao', Kong_fu_xue_tang_jian_cha_biao_CreateView.as_view(), name='kong_fu_xue_tang_jian_cha_biao_create_url'),
    path('tang_hua_xue_hong_dan_bai_jian_cha_biao', Tang_hua_xue_hong_dan_bai_jian_cha_biao_CreateView.as_view(), name='tang_hua_xue_hong_dan_bai_jian_cha_biao_create_url'),
    path('men_zhen_zhen_duan_biao', Men_zhen_zhen_duan_biao_CreateView.as_view(), name='men_zhen_zhen_duan_biao_create_url'),
    path('yong_yao_chu_fang_biao', Yong_yao_chu_fang_biao_CreateView.as_view(), name='yong_yao_chu_fang_biao_create_url'),
]