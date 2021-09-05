from django.contrib import admin
from .models import *

class Basic_personal_informationAdmin(admin.ModelAdmin):
	autocomplete_fields = ["family_id"]
admin.site.register(Basic_personal_information, Basic_personal_informationAdmin)

class Family_historyAdmin(admin.ModelAdmin):
	autocomplete_fields = ["diseases"]
admin.site.register(Family_history, Family_historyAdmin)

class History_of_infectious_diseasesAdmin(admin.ModelAdmin):
	autocomplete_fields = ["diseases"]
admin.site.register(History_of_infectious_diseases, History_of_infectious_diseasesAdmin)