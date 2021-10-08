from django.contrib import admin
from .models import *

class History_of_traumaAdmin(admin.ModelAdmin):
	autocomplete_fields = ["diseases_name"]
admin.site.register(History_of_trauma, History_of_traumaAdmin)

class Medical_historyAdmin(admin.ModelAdmin):
	autocomplete_fields = ["disease_name"]
admin.site.register(Medical_history, Medical_historyAdmin)

class Family_surveyAdmin(admin.ModelAdmin):
	autocomplete_fields = ["diseases"]
admin.site.register(Family_survey, Family_surveyAdmin)

class History_of_surgeryAdmin(admin.ModelAdmin):
	autocomplete_fields = ["name_of_operation"]
admin.site.register(History_of_surgery, History_of_surgeryAdmin)

class Basic_personal_informationAdmin(admin.ModelAdmin):
	autocomplete_fields = ["family_id"]
admin.site.register(Basic_personal_information, Basic_personal_informationAdmin)

class History_of_infectious_diseasesAdmin(admin.ModelAdmin):
	autocomplete_fields = ["diseases"]
admin.site.register(History_of_infectious_diseases, History_of_infectious_diseasesAdmin)