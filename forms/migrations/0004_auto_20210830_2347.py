# Generated by Django 3.2.6 on 2021-08-30 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0003_basic_personal_information_doctor_login_doctor_registry_user_login_user_registry'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Basic_personal_information',
        ),
        migrations.DeleteModel(
            name='Doctor_login',
        ),
        migrations.DeleteModel(
            name='Doctor_registry',
        ),
        migrations.DeleteModel(
            name='User_login',
        ),
        migrations.DeleteModel(
            name='User_registry',
        ),
    ]
