from django.urls import path
from .views import *

urlpatterns = [
	path('', Index_view.as_view(), name='index'),
	path('index/', Index_view.as_view(), name='index'),
    path('yuan_qian_zheng_zhuang_diao_cha_biao/create', yuan_qian_zheng_zhuang_diao_cha_biao_create, name='yuan_qian_zheng_zhuang_diao_cha_biao_create_url'),
    path('yuan_qian_zheng_zhuang_diao_cha_biao/<int:id>/update', yuan_qian_zheng_zhuang_diao_cha_biao_update, name='yuan_qian_zheng_zhuang_diao_cha_biao_update_url'),
    path('ge_ren_ji_bing_shi_diao_cha_biao/create', ge_ren_ji_bing_shi_diao_cha_biao_create, name='ge_ren_ji_bing_shi_diao_cha_biao_create_url'),
    path('ge_ren_ji_bing_shi_diao_cha_biao/<int:id>/update', ge_ren_ji_bing_shi_diao_cha_biao_update, name='ge_ren_ji_bing_shi_diao_cha_biao_update_url'),
    path('kong_fu_xue_tang_jian_cha_biao/create', kong_fu_xue_tang_jian_cha_biao_create, name='kong_fu_xue_tang_jian_cha_biao_create_url'),
    path('kong_fu_xue_tang_jian_cha_biao/<int:id>/update', kong_fu_xue_tang_jian_cha_biao_update, name='kong_fu_xue_tang_jian_cha_biao_update_url'),
    path('men_zhen_zhen_duan_biao/create', men_zhen_zhen_duan_biao_create, name='men_zhen_zhen_duan_biao_create_url'),
    path('men_zhen_zhen_duan_biao/<int:id>/update', men_zhen_zhen_duan_biao_update, name='men_zhen_zhen_duan_biao_update_url'),
    path('tang_hua_xue_hong_dan_bai_jian_cha_biao/create', tang_hua_xue_hong_dan_bai_jian_cha_biao_create, name='tang_hua_xue_hong_dan_bai_jian_cha_biao_create_url'),
    path('tang_hua_xue_hong_dan_bai_jian_cha_biao/<int:id>/update', tang_hua_xue_hong_dan_bai_jian_cha_biao_update, name='tang_hua_xue_hong_dan_bai_jian_cha_biao_update_url'),
    path('chang_gui_cha_ti_biao/create', chang_gui_cha_ti_biao_create, name='chang_gui_cha_ti_biao_create_url'),
    path('chang_gui_cha_ti_biao/<int:id>/update', chang_gui_cha_ti_biao_update, name='chang_gui_cha_ti_biao_update_url'),
    path('tang_niao_bing_cha_ti_biao/create', tang_niao_bing_cha_ti_biao_create, name='tang_niao_bing_cha_ti_biao_create_url'),
    path('tang_niao_bing_cha_ti_biao/<int:id>/update', tang_niao_bing_cha_ti_biao_update, name='tang_niao_bing_cha_ti_biao_update_url'),
    path('ge_ren_guo_min_shi_diao_cha_biao/create', ge_ren_guo_min_shi_diao_cha_biao_create, name='ge_ren_guo_min_shi_diao_cha_biao_create_url'),
    path('ge_ren_guo_min_shi_diao_cha_biao/<int:id>/update', ge_ren_guo_min_shi_diao_cha_biao_update, name='ge_ren_guo_min_shi_diao_cha_biao_update_url'),
    path('men_zhen_wen_zhen_diao_cha_biao/create', men_zhen_wen_zhen_diao_cha_biao_create, name='men_zhen_wen_zhen_diao_cha_biao_create_url'),
    path('men_zhen_wen_zhen_diao_cha_biao/<int:id>/update', men_zhen_wen_zhen_diao_cha_biao_update, name='men_zhen_wen_zhen_diao_cha_biao_update_url'),
    path('men_zhen_chu_fang_biao/create', men_zhen_chu_fang_biao_create, name='men_zhen_chu_fang_biao_create_url'),
    path('men_zhen_chu_fang_biao/<int:id>/update', men_zhen_chu_fang_biao_update, name='men_zhen_chu_fang_biao_update_url'),
]