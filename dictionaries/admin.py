from django.contrib import admin
from .models import *

class Drug_listAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Drug_list, Drug_listAdmin)

class CharacterAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Character, CharacterAdmin)

class SatisfactionAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Satisfaction, SatisfactionAdmin)

class FrequencyAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Frequency, FrequencyAdmin)

class State_degreeAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(State_degree, State_degreeAdmin)

class Comparative_expressionAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Comparative_expression, Comparative_expressionAdmin)

class Sports_preferenceAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Sports_preference, Sports_preferenceAdmin)

class Exercise_timeAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Exercise_time, Exercise_timeAdmin)

class ConvenienceAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Convenience, ConvenienceAdmin)

class Family_relationshipAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Family_relationship, Family_relationshipAdmin)

class NormalityAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Normality, NormalityAdmin)

class Service_roleAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Service_role, Service_roleAdmin)

class Institutions_listAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Institutions_list, Institutions_listAdmin)

class Dorsal_artery_pulsationAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Dorsal_artery_pulsation, Dorsal_artery_pulsationAdmin)

class HearingAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Hearing, HearingAdmin)

class LipsAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Lips, LipsAdmin)

class DentitionAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Dentition, DentitionAdmin)

class PharynxAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Pharynx, PharynxAdmin)

class Life_eventAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Life_event, Life_eventAdmin)

class EdemaAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Edema, EdemaAdmin)

class GenderAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Gender, GenderAdmin)

class NationalityAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Nationality, NationalityAdmin)

class Marital_statusAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Marital_status, Marital_statusAdmin)

class EducationAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Education, EducationAdmin)

class Occupational_statusAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Occupational_status, Occupational_statusAdmin)

class Medical_expenses_burdenAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Medical_expenses_burden, Medical_expenses_burdenAdmin)

class Type_of_residenceAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Type_of_residence, Type_of_residenceAdmin)

class Blood_typeAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Blood_type, Blood_typeAdmin)

class Employee_listAdmin(admin.ModelAdmin):
    search_fields = ["value"]
admin.site.register(Employee_list, Employee_listAdmin)

