from django.contrib import admin
from .models import *
    
class Ge_ren_ji_ben_xin_xi_1638359483Admin(admin.ModelAdmin):
    autocomplete_fields = ["zheng_zhuang_1638359376", ]
admin.site.register(Ge_ren_ji_ben_xin_xi_1638359483, Ge_ren_ji_ben_xin_xi_1638359483Admin)

class Ji_bing_shi_1638359530Admin(admin.ModelAdmin):
    autocomplete_fields = ["zhen_duan_1638359350", ]
admin.site.register(Ji_bing_shi_1638359530, Ji_bing_shi_1638359530Admin)
