from django.contrib import admin
from .models import *

class Metadata_follow_up_formAdmin(admin.ModelAdmin):
	autocomplete_fields = ["method"]
admin.site.register(Metadata_follow_up_form, Metadata_follow_up_formAdmin)

class Routine_physical_examinationAdmin(admin.ModelAdmin):
	autocomplete_fields = ["test_comments"]
admin.site.register(Routine_physical_examination, Routine_physical_examinationAdmin)