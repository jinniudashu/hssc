from django.contrib import admin
from .models import *

class MedicineAdmin(admin.ModelAdmin):
	search_fields=["name"]
admin.site.register(Medicine, MedicineAdmin)


class InstitutionAdmin(admin.ModelAdmin):
	search_fields=["name"]
admin.site.register(Institution, InstitutionAdmin)
