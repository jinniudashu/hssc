# Generated by Django 3.2.6 on 2021-09-05 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0004_blood_type_contract_signatory_education_gender_marital_status_medical_expenses_burden_nationality_oc'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Blood_type',
        ),
        migrations.DeleteModel(
            name='Contract_signatory',
        ),
        migrations.DeleteModel(
            name='Education',
        ),
        migrations.DeleteModel(
            name='Gender',
        ),
        migrations.DeleteModel(
            name='Marital_status',
        ),
        migrations.DeleteModel(
            name='Medical_expenses_burden',
        ),
        migrations.DeleteModel(
            name='Nationality',
        ),
        migrations.DeleteModel(
            name='Occupational_status',
        ),
        migrations.DeleteModel(
            name='Relationship_with_the_head_of_household',
        ),
        migrations.DeleteModel(
            name='Service_role',
        ),
        migrations.DeleteModel(
            name='Type_of_residence',
        ),
    ]
