from django.urls import path
from .views import *

urlpatterns = [
	path('', Index_view.as_view(), name='index'),
	path('index/', Index_view.as_view(), name='index'),
    path('chang_gui_cha_ti_biao/create', Chang_gui_cha_ti_biao_CreateView.as_view(), name='chang_gui_cha_ti_biao_create_url'),
    path('tang_niao_bing_cha_ti_biao/create', Tang_niao_bing_cha_ti_biao_CreateView.as_view(), name='tang_niao_bing_cha_ti_biao_create_url'),
    path('men_zhen_chu_fang_biao/create', Men_zhen_chu_fang_biao_CreateView.as_view(), name='men_zhen_chu_fang_biao_create_url'),
    path('user_registry/create', User_registry_CreateView.as_view(), name='user_registry_create_url'),
    path('user_login/create', User_login_CreateView.as_view(), name='user_login_create_url'),
    path('doctor_login/create', Doctor_login_CreateView.as_view(), name='doctor_login_create_url'),
    path('A6501/create', A6501_CreateView.as_view(), name='A6501_create_url'),
    path('men_zhen_fu_zhu_jian_cha/create', Men_zhen_fu_zhu_jian_cha_CreateView.as_view(), name='men_zhen_fu_zhu_jian_cha_create_url'),
    path('tang_niao_bing_zhuan_yong_wen_zhen/create', Tang_niao_bing_zhuan_yong_wen_zhen_CreateView.as_view(), name='tang_niao_bing_zhuan_yong_wen_zhen_create_url'),
    path('yao_shi_fu_wu/create', Yao_shi_fu_wu_CreateView.as_view(), name='yao_shi_fu_wu_create_url'),
    path('tang_niao_bing_zi_wo_jian_ce/create', Tang_niao_bing_zi_wo_jian_ce_CreateView.as_view(), name='tang_niao_bing_zi_wo_jian_ce_create_url'),
    path('yuan_nei_fu_zhu_wen_zhen/create', Yuan_nei_fu_zhu_wen_zhen_CreateView.as_view(), name='yuan_nei_fu_zhu_wen_zhen_create_url'),
    path('A6201/create', A6201_CreateView.as_view(), name='A6201_create_url'),
    path('men_zhen_yi_sheng_wen_zhen/create', Men_zhen_yi_sheng_wen_zhen_CreateView.as_view(), name='men_zhen_yi_sheng_wen_zhen_create_url'),
    path('T8901/create', T8901_CreateView.as_view(), name='T8901_create_url'),
    path('T6301/create', T6301_CreateView.as_view(), name='T6301_create_url'),
    path('A6202/create', A6202_CreateView.as_view(), name='A6202_create_url'),
    path('A6220/create', A6220_CreateView.as_view(), name='A6220_create_url'),
    path('A6299/create', A6299_CreateView.as_view(), name='A6299_create_url'),
    path('A3502/create', A3502_CreateView.as_view(), name='A3502_create_url'),
]