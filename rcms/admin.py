from django.contrib import admin

from .models import Dictionaries, DictionaryData, Forms, FormsComponents
from .models import IcpcLists, Icpcs, Icpc1S, Icpc2S, Icpc3S, Icpc4S, Icpc5S, Icpc6S, Icpc7S, Icpc8S, Icpc9S, Icpc10TestResultsAndStatistics
from .models import OperationProcesses, Operations, Osms

admin.site.register(Dictionaries)
admin.site.register(DictionaryData)
admin.site.register(Forms)
admin.site.register(FormsComponents)
admin.site.register(IcpcLists)
admin.site.register(Icpcs)
admin.site.register(Icpc1S)
admin.site.register(Icpc2S)
admin.site.register(Icpc3S)
admin.site.register(Icpc4S)
admin.site.register(Icpc5S)
admin.site.register(Icpc6S)
admin.site.register(Icpc7S)
admin.site.register(Icpc8S)
admin.site.register(Icpc9S)
admin.site.register(Icpc10TestResultsAndStatistics)
admin.site.register(OperationProcesses)
admin.site.register(Operations)
admin.site.register(Osms)
