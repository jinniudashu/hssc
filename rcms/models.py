# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ComponentsFieldsCharFields(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    icpc_list = models.IntegerField(blank=True, null=True)
    auxiliary_input = models.IntegerField(blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)
    input_style = models.CharField(max_length=255, blank=True, null=True)
    score = models.BooleanField(blank=True, null=True)
    field_parameters = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'components_fields_char_fields'


class ComponentsFieldsComputedFields(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    include = models.CharField(max_length=255, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'components_fields_computed_fields'


class ComponentsFieldsDateFields(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    icpc_list = models.IntegerField(blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)
    field_parameters = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'components_fields_date_fields'


class ComponentsFieldsNumberFields(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    icpc_list = models.IntegerField(blank=True, null=True)
    standard = models.FloatField(blank=True, null=True)
    up_limit = models.FloatField(blank=True, null=True)
    down_limit = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=255, blank=True, null=True)
    group = models.CharField(max_length=255, blank=True, null=True)
    prifix = models.CharField(max_length=255, blank=True, null=True)
    for_calculating = models.BooleanField(blank=True, null=True)
    field_parameters = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'components_fields_number_fields'


class CoreStore(models.Model):
    key = models.CharField(max_length=255, blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    environment = models.CharField(max_length=255, blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_store'


class Dictionaries(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    did = models.CharField(unique=True, max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dictionaries'


class DictionaryData(models.Model):
    value = models.CharField(max_length=255, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    dictionary = models.IntegerField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dictionary_data'


class Forms(models.Model):
    operation_id = models.IntegerField(blank=True, null=True)
    icpc_code = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    fid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    oid = models.IntegerField(blank=True, null=True)
    uid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    cid = models.CharField(unique=True, max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'forms'


class FormsComponents(models.Model):
    field = models.CharField(max_length=255)
    order = models.IntegerField()
    component_type = models.CharField(max_length=255)
    component_id = models.IntegerField()
    form = models.ForeignKey(Forms, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'forms_components'


class I18NLocales(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(unique=True, max_length=255, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'i18n_locales'


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

    class Meta:
        managed = False
        db_table = 'icpc10_test_results_and_statistics'


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

    class Meta:
        managed = False
        db_table = 'icpc1s'


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

    class Meta:
        managed = False
        db_table = 'icpc2s'


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

    class Meta:
        managed = False
        db_table = 'icpc3s'


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

    class Meta:
        managed = False
        db_table = 'icpc4s'


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

    class Meta:
        managed = False
        db_table = 'icpc5s'


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

    class Meta:
        managed = False
        db_table = 'icpc6s'


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

    class Meta:
        managed = False
        db_table = 'icpc7s'


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

    class Meta:
        managed = False
        db_table = 'icpc8s'


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

    class Meta:
        managed = False
        db_table = 'icpc9s'


class IcpcLists(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    icpc_list_id = models.CharField(unique=True, max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'icpc_lists'


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

    class Meta:
        managed = False
        db_table = 'icpcs'


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

    class Meta:
        managed = False
        db_table = 'operation_processes'


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

    class Meta:
        managed = False
        db_table = 'operations'


class Osms(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    status_machine = models.JSONField(blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'osms'


class StrapiAdministrator(models.Model):
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255, blank=True, null=True)
    resetpasswordtoken = models.CharField(db_column='resetPasswordToken', max_length=255, blank=True, null=True)  # Field name made lowercase.
    registrationtoken = models.CharField(db_column='registrationToken', max_length=255, blank=True, null=True)  # Field name made lowercase.
    isactive = models.BooleanField(db_column='isActive', blank=True, null=True)  # Field name made lowercase.
    blocked = models.BooleanField(blank=True, null=True)
    preferedlanguage = models.CharField(db_column='preferedLanguage', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'strapi_administrator'


class StrapiPermission(models.Model):
    action = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, blank=True, null=True)
    properties = models.JSONField(blank=True, null=True)
    conditions = models.JSONField(blank=True, null=True)
    role = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'strapi_permission'


class StrapiRole(models.Model):
    name = models.CharField(unique=True, max_length=255)
    code = models.CharField(unique=True, max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'strapi_role'


class StrapiUsersRoles(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    role_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'strapi_users_roles'


class StrapiWebhooks(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    headers = models.JSONField(blank=True, null=True)
    events = models.JSONField(blank=True, null=True)
    enabled = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'strapi_webhooks'


class UploadFile(models.Model):
    name = models.CharField(max_length=255)
    alternativetext = models.CharField(db_column='alternativeText', max_length=255, blank=True, null=True)  # Field name made lowercase.
    caption = models.CharField(max_length=255, blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    formats = models.JSONField(blank=True, null=True)
    hash = models.CharField(max_length=255)
    ext = models.CharField(max_length=255, blank=True, null=True)
    mime = models.CharField(max_length=255)
    size = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.CharField(max_length=255)
    previewurl = models.CharField(db_column='previewUrl', max_length=255, blank=True, null=True)  # Field name made lowercase.
    provider = models.CharField(max_length=255)
    provider_metadata = models.JSONField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'upload_file'


class UploadFileMorph(models.Model):
    upload_file_id = models.IntegerField(blank=True, null=True)
    related_id = models.IntegerField(blank=True, null=True)
    related_type = models.TextField(blank=True, null=True)
    field = models.TextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'upload_file_morph'


class UsersPermissionsPermission(models.Model):
    type = models.CharField(max_length=255)
    controller = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    enabled = models.BooleanField()
    policy = models.CharField(max_length=255, blank=True, null=True)
    role = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users-permissions_permission'


class UsersPermissionsRole(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(unique=True, max_length=255, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users-permissions_role'


class UsersPermissionsUser(models.Model):
    username = models.CharField(unique=True, max_length=255)
    email = models.CharField(max_length=255)
    provider = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    resetpasswordtoken = models.CharField(db_column='resetPasswordToken', max_length=255, blank=True, null=True)  # Field name made lowercase.
    confirmationtoken = models.CharField(db_column='confirmationToken', max_length=255, blank=True, null=True)  # Field name made lowercase.
    confirmed = models.BooleanField(blank=True, null=True)
    blocked = models.BooleanField(blank=True, null=True)
    role = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    updated_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users-permissions_user'
