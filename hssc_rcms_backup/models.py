from django.db import models


class Dictionaries(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    did = models.CharField(unique=True, max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)




class DictionaryData(models.Model):
    value = models.CharField(max_length=255, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    dictionary = models.IntegerField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)




class Icpc10TestResultsAndStatistics(models.Model):
    icpc_code = models.CharField(max_length=255, blank=True, null=True)
    icode = models.CharField(max_length=255, blank=True, null=True)
    iname = models.CharField(max_length=255, blank=True, null=True)
    iename = models.CharField(max_length=255, blank=True, null=True)
    include = models.CharField(max_length=255, blank=True, null=True)
    criteria = models.CharField(max_length=255, blank=True, null=True)
    exclude = models.CharField(max_length=255, blank=True, null=True)
    consider = models.CharField(max_length=255, blank=True, null=True)
    icd10 = models.CharField(max_length=255, blank=True, null=True)
    icpc2 = models.CharField(max_length=255, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    pym = models.CharField(max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)




class Icpc1S(models.Model):
    icpc_code = models.CharField(max_length=255, blank=True, null=True)
    icode = models.CharField(max_length=255, blank=True, null=True)
    iname = models.CharField(max_length=255, blank=True, null=True)
    iename = models.CharField(max_length=255, blank=True, null=True)
    include = models.CharField(max_length=255, blank=True, null=True)
    criteria = models.CharField(max_length=255, blank=True, null=True)
    exclude = models.CharField(max_length=255, blank=True, null=True)
    consider = models.CharField(max_length=255, blank=True, null=True)
    icd10 = models.CharField(max_length=255, blank=True, null=True)
    icpc2 = models.CharField(max_length=255, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    pym = models.CharField(max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)




class Icpc2S(models.Model):
    icpc_code = models.CharField(max_length=255, blank=True, null=True)
    icode = models.CharField(max_length=255, blank=True, null=True)
    iname = models.CharField(max_length=255, blank=True, null=True)
    iename = models.CharField(max_length=255, blank=True, null=True)
    include = models.CharField(max_length=255, blank=True, null=True)
    criteria = models.CharField(max_length=255, blank=True, null=True)
    exclude = models.CharField(max_length=255, blank=True, null=True)
    consider = models.CharField(max_length=255, blank=True, null=True)
    icd10 = models.CharField(max_length=255, blank=True, null=True)
    icpc2 = models.CharField(max_length=255, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    pym = models.CharField(max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)




class Icpc3S(models.Model):
    icpc_code = models.CharField(max_length=255, blank=True, null=True)
    icode = models.CharField(max_length=255, blank=True, null=True)
    iname = models.CharField(max_length=255, blank=True, null=True)
    iename = models.CharField(max_length=255, blank=True, null=True)
    include = models.CharField(max_length=255, blank=True, null=True)
    criteria = models.CharField(max_length=255, blank=True, null=True)
    exclude = models.CharField(max_length=255, blank=True, null=True)
    consider = models.CharField(max_length=255, blank=True, null=True)
    icd10 = models.CharField(max_length=255, blank=True, null=True)
    icpc2 = models.CharField(max_length=255, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    pym = models.CharField(max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)




class Icpc4S(models.Model):
    icpc_code = models.CharField(max_length=255, blank=True, null=True)
    icode = models.CharField(max_length=255, blank=True, null=True)
    iname = models.CharField(max_length=255, blank=True, null=True)
    iename = models.CharField(max_length=255, blank=True, null=True)
    include = models.CharField(max_length=255, blank=True, null=True)
    criteria = models.CharField(max_length=255, blank=True, null=True)
    exclude = models.CharField(max_length=255, blank=True, null=True)
    consider = models.CharField(max_length=255, blank=True, null=True)
    icd10 = models.CharField(max_length=255, blank=True, null=True)
    icpc2 = models.CharField(max_length=255, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    pym = models.CharField(max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)




class Icpc5S(models.Model):
    icpc_code = models.CharField(max_length=255, blank=True, null=True)
    icode = models.CharField(max_length=255, blank=True, null=True)
    iname = models.CharField(max_length=255, blank=True, null=True)
    iename = models.CharField(max_length=255, blank=True, null=True)
    include = models.CharField(max_length=255, blank=True, null=True)
    criteria = models.CharField(max_length=255, blank=True, null=True)
    exclude = models.CharField(max_length=255, blank=True, null=True)
    consider = models.CharField(max_length=255, blank=True, null=True)
    icd10 = models.CharField(max_length=255, blank=True, null=True)
    icpc2 = models.CharField(max_length=255, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    pym = models.CharField(max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)




class Icpc6S(models.Model):
    icpc_code = models.CharField(max_length=255, blank=True, null=True)
    icode = models.CharField(max_length=255, blank=True, null=True)
    iname = models.CharField(max_length=255, blank=True, null=True)
    iename = models.CharField(max_length=255, blank=True, null=True)
    include = models.CharField(max_length=255, blank=True, null=True)
    criteria = models.CharField(max_length=255, blank=True, null=True)
    exclude = models.CharField(max_length=255, blank=True, null=True)
    consider = models.CharField(max_length=255, blank=True, null=True)
    icd10 = models.CharField(max_length=255, blank=True, null=True)
    icpc2 = models.CharField(max_length=255, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    pym = models.CharField(max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)




class Icpc7S(models.Model):
    icpc_code = models.CharField(max_length=255, blank=True, null=True)
    icode = models.CharField(max_length=255, blank=True, null=True)
    iname = models.CharField(max_length=255, blank=True, null=True)
    iename = models.CharField(max_length=255, blank=True, null=True)
    include = models.CharField(max_length=255, blank=True, null=True)
    criteria = models.CharField(max_length=255, blank=True, null=True)
    exclude = models.CharField(max_length=255, blank=True, null=True)
    consider = models.CharField(max_length=255, blank=True, null=True)
    icd10 = models.CharField(max_length=255, blank=True, null=True)
    icpc2 = models.CharField(max_length=255, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    pym = models.CharField(max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)




class Icpc8S(models.Model):
    icpc_code = models.CharField(max_length=255, blank=True, null=True)
    icode = models.CharField(max_length=255, blank=True, null=True)
    iname = models.CharField(max_length=255, blank=True, null=True)
    iename = models.CharField(max_length=255, blank=True, null=True)
    include = models.CharField(max_length=255, blank=True, null=True)
    criteria = models.CharField(max_length=255, blank=True, null=True)
    exclude = models.CharField(max_length=255, blank=True, null=True)
    consider = models.CharField(max_length=255, blank=True, null=True)
    icd10 = models.CharField(max_length=255, blank=True, null=True)
    icpc2 = models.CharField(max_length=255, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    pym = models.CharField(max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)




class Icpc9S(models.Model):
    icpc_code = models.CharField(max_length=255, blank=True, null=True)
    icode = models.CharField(max_length=255, blank=True, null=True)
    iname = models.CharField(max_length=255, blank=True, null=True)
    iename = models.CharField(max_length=255, blank=True, null=True)
    include = models.CharField(max_length=255, blank=True, null=True)
    criteria = models.CharField(max_length=255, blank=True, null=True)
    exclude = models.CharField(max_length=255, blank=True, null=True)
    consider = models.CharField(max_length=255, blank=True, null=True)
    icd10 = models.CharField(max_length=255, blank=True, null=True)
    icpc2 = models.CharField(max_length=255, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    pym = models.CharField(max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)




class IcpcLists(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    icpc_list_id = models.CharField(unique=True, max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)




class Icpcs(models.Model):
    icpc_code = models.CharField(max_length=255, blank=True, null=True)
    icode = models.CharField(max_length=255, blank=True, null=True)
    iname = models.CharField(max_length=255, blank=True, null=True)
    iename = models.CharField(max_length=255, blank=True, null=True)
    include = models.CharField(max_length=255, blank=True, null=True)
    criteria = models.CharField(max_length=255, blank=True, null=True)
    exclude = models.CharField(max_length=255, blank=True, null=True)
    consider = models.CharField(max_length=255, blank=True, null=True)
    icd10 = models.CharField(max_length=255, blank=True, null=True)
    icpc2 = models.CharField(max_length=255, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    pym = models.CharField(max_length=255, blank=True, null=True)
    subclass = models.IntegerField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)




class OperationProcesses(models.Model):
    oid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    tid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    sid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    pid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    uid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    cid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    operation_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)




class Operations(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    operation_id = models.CharField(unique=True, max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)




class Osms(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    status_machine = models.JSONField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

