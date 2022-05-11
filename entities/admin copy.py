from django.contrib import admin
from hssc.site import clinic_site
from .models import *

class MedicineAdmin(admin.ModelAdmin):
	search_fields=["name"]
admin.site.register(Medicine, MedicineAdmin)
clinic_site.register(Medicine, MedicineAdmin)


class InstitutionAdmin(admin.ModelAdmin):
	search_fields=["name"]
admin.site.register(Institution, InstitutionAdmin)
clinic_site.register(Institution, InstitutionAdmin)
