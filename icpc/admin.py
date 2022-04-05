from django.contrib import admin
from .models import *

@admin.register(Icpc)
class IcpcAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Icpc._meta.fields]
    search_fields=["iname", "pym", "icpc_code"]
    ordering = ["icpc_code"]
    readonly_fields = [field.name for field in Icpc._meta.fields]
    actions = None

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Icpc1_register_logins)
class Icpc1_register_loginsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Icpc1_register_logins._meta.fields]
    search_fields=["iname", "pym", "icpc_code"]
    ordering = ["icpc_code"]
    readonly_fields = [field.name for field in Icpc1_register_logins._meta.fields]
    actions = None

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Icpc2_reservation_investigations)
class Icpc2_reservation_investigationsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Icpc2_reservation_investigations._meta.fields]
    search_fields=["iname", "pym", "icpc_code"]
    ordering = ["icpc_code"]
    readonly_fields = [field.name for field in Icpc2_reservation_investigations._meta.fields]
    actions = None

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Icpc3_symptoms_and_problems)
class Icpc3_symptoms_and_problemsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Icpc3_symptoms_and_problems._meta.fields]
    search_fields=["iname", "pym", "icpc_code"]
    ordering = ["icpc_code"]
    readonly_fields = [field.name for field in Icpc3_symptoms_and_problems._meta.fields]
    actions = None

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Icpc4_physical_examination_and_tests)
class Icpc4_physical_examination_and_testsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Icpc4_physical_examination_and_tests._meta.fields]
    search_fields=["iname", "pym", "icpc_code"]
    ordering = ["icpc_code"]
    readonly_fields = [field.name for field in Icpc4_physical_examination_and_tests._meta.fields]
    actions = None

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Icpc5_evaluation_and_diagnoses)
class Icpc5_evaluation_and_diagnosesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Icpc5_evaluation_and_diagnoses._meta.fields]
    search_fields=["iname", "pym", "icpc_code"]
    ordering = ["icpc_code"]
    readonly_fields = [field.name for field in Icpc5_evaluation_and_diagnoses._meta.fields]
    actions = None

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Icpc6_prescribe_medicines)
class Icpc6_prescribe_medicinesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Icpc6_prescribe_medicines._meta.fields]
    search_fields=["iname", "pym", "icpc_code"]
    ordering = ["icpc_code"]
    readonly_fields = [field.name for field in Icpc6_prescribe_medicines._meta.fields]
    actions = None

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Icpc7_treatments)
class Icpc7_treatmentsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Icpc7_treatments._meta.fields]
    search_fields=["iname", "pym", "icpc_code"]
    ordering = ["icpc_code"]
    readonly_fields = [field.name for field in Icpc7_treatments._meta.fields]
    actions = None

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Icpc8_other_health_interventions)
class Icpc8_other_health_interventionsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Icpc8_other_health_interventions._meta.fields]
    search_fields=["iname", "pym", "icpc_code"]
    ordering = ["icpc_code"]
    readonly_fields = [field.name for field in Icpc8_other_health_interventions._meta.fields]
    actions = None

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Icpc9_referral_consultations)
class Icpc9_referral_consultationsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Icpc9_referral_consultations._meta.fields]
    search_fields=["iname", "pym", "icpc_code"]
    ordering = ["icpc_code"]
    readonly_fields = [field.name for field in Icpc9_referral_consultations._meta.fields]
    actions = None

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Icpc10_test_results_and_statistics)
class Icpc10_test_results_and_statisticsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Icpc10_test_results_and_statistics._meta.fields]
    search_fields=["iname", "pym", "icpc_code"]
    ordering = ["icpc_code"]
    readonly_fields = [field.name for field in Icpc10_test_results_and_statistics._meta.fields]
    actions = None

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
