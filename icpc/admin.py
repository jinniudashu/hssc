from django.contrib import admin
from .models import *


class Icpc1_register_loginsAdmin(admin.ModelAdmin):
	list_display = ('icpc_code', 'iname', 'iename', 'include', 'criteria', 'exclude', 'consider',)
	search_fields=["iname", "pym"]
	ordering = ["icpc_code"]
admin.site.register(Icpc1_register_logins, Icpc1_register_loginsAdmin)

class Icpc2_reservation_investigationsAdmin(admin.ModelAdmin):
	list_display = ('icpc_code', 'iname', 'iename', 'include', 'criteria', 'exclude', 'consider',)
	search_fields=["iname", "pym"]
	ordering = ["icpc_code"]
admin.site.register(Icpc2_reservation_investigations, Icpc2_reservation_investigationsAdmin)

class Icpc3_symptoms_and_problemsAdmin(admin.ModelAdmin):
	list_display = ('icpc_code', 'iname', 'iename', 'include', 'criteria', 'exclude', 'consider',)
	search_fields=["iname", "pym"]
	ordering = ["icpc_code"]
admin.site.register(Icpc3_symptoms_and_problems, Icpc3_symptoms_and_problemsAdmin)

class Icpc4_physical_examination_and_testsAdmin(admin.ModelAdmin):
	list_display = ('icpc_code', 'iname', 'iename', 'include', 'criteria', 'exclude', 'consider',)
	search_fields=["iname", "pym"]
	ordering = ["icpc_code"]
admin.site.register(Icpc4_physical_examination_and_tests, Icpc4_physical_examination_and_testsAdmin)

class Icpc5_evaluation_and_diagnosesAdmin(admin.ModelAdmin):
	list_display = ('icpc_code', 'iname', 'iename', 'include', 'criteria', 'exclude', 'consider',)
	search_fields=["iname", "pym"]
	ordering = ["icpc_code"]
admin.site.register(Icpc5_evaluation_and_diagnoses, Icpc5_evaluation_and_diagnosesAdmin)

class Icpc6_prescribe_medicinesAdmin(admin.ModelAdmin):
	list_display = ('icpc_code', 'iname', 'iename', 'include', 'criteria', 'exclude', 'consider',)
	search_fields=["iname", "pym"]
	ordering = ["icpc_code"]
admin.site.register(Icpc6_prescribe_medicines, Icpc6_prescribe_medicinesAdmin)

class Icpc7_treatmentsAdmin(admin.ModelAdmin):
	list_display = ('icpc_code', 'iname', 'iename', 'include', 'criteria', 'exclude', 'consider',)
	search_fields=["iname", "pym"]
	ordering = ["icpc_code"]
admin.site.register(Icpc7_treatments, Icpc7_treatmentsAdmin)

class Icpc8_other_health_interventionsAdmin(admin.ModelAdmin):
	list_display = ('icpc_code', 'iname', 'iename', 'include', 'criteria', 'exclude', 'consider',)
	search_fields=["iname", "pym"]
	ordering = ["icpc_code"]
admin.site.register(Icpc8_other_health_interventions, Icpc8_other_health_interventionsAdmin)

class Icpc9_referral_consultationsAdmin(admin.ModelAdmin):
	list_display = ('icpc_code', 'iname', 'iename', 'include', 'criteria', 'exclude', 'consider',)
	search_fields=["iname", "pym"]
	ordering = ["icpc_code"]
admin.site.register(Icpc9_referral_consultations, Icpc9_referral_consultationsAdmin)

class Icpc10_test_results_and_statisticsAdmin(admin.ModelAdmin):
	list_display = ('icpc_code', 'iname', 'iename', 'include', 'criteria', 'exclude', 'consider',)
	search_fields=["iname", "pym"]
	ordering = ["icpc_code"]
admin.site.register(Icpc10_test_results_and_statistics, Icpc10_test_results_and_statisticsAdmin)
