# Generated by Django 3.2.6 on 2021-12-27 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionaries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('label', models.CharField(blank=True, max_length=255, null=True)),
                ('did', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DictionaryData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, max_length=255, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('dictionary', models.IntegerField(blank=True, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Icpc10TestResultsAndStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=255, null=True)),
                ('icode', models.CharField(blank=True, max_length=255, null=True)),
                ('iname', models.CharField(blank=True, max_length=255, null=True)),
                ('iename', models.CharField(blank=True, max_length=255, null=True)),
                ('include', models.CharField(blank=True, max_length=255, null=True)),
                ('criteria', models.CharField(blank=True, max_length=255, null=True)),
                ('exclude', models.CharField(blank=True, max_length=255, null=True)),
                ('consider', models.CharField(blank=True, max_length=255, null=True)),
                ('icd10', models.CharField(blank=True, max_length=255, null=True)),
                ('icpc2', models.CharField(blank=True, max_length=255, null=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('pym', models.CharField(blank=True, max_length=255, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Icpc1S',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=255, null=True)),
                ('icode', models.CharField(blank=True, max_length=255, null=True)),
                ('iname', models.CharField(blank=True, max_length=255, null=True)),
                ('iename', models.CharField(blank=True, max_length=255, null=True)),
                ('include', models.CharField(blank=True, max_length=255, null=True)),
                ('criteria', models.CharField(blank=True, max_length=255, null=True)),
                ('exclude', models.CharField(blank=True, max_length=255, null=True)),
                ('consider', models.CharField(blank=True, max_length=255, null=True)),
                ('icd10', models.CharField(blank=True, max_length=255, null=True)),
                ('icpc2', models.CharField(blank=True, max_length=255, null=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('pym', models.CharField(blank=True, max_length=255, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Icpc2S',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=255, null=True)),
                ('icode', models.CharField(blank=True, max_length=255, null=True)),
                ('iname', models.CharField(blank=True, max_length=255, null=True)),
                ('iename', models.CharField(blank=True, max_length=255, null=True)),
                ('include', models.CharField(blank=True, max_length=255, null=True)),
                ('criteria', models.CharField(blank=True, max_length=255, null=True)),
                ('exclude', models.CharField(blank=True, max_length=255, null=True)),
                ('consider', models.CharField(blank=True, max_length=255, null=True)),
                ('icd10', models.CharField(blank=True, max_length=255, null=True)),
                ('icpc2', models.CharField(blank=True, max_length=255, null=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('pym', models.CharField(blank=True, max_length=255, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Icpc3S',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=255, null=True)),
                ('icode', models.CharField(blank=True, max_length=255, null=True)),
                ('iname', models.CharField(blank=True, max_length=255, null=True)),
                ('iename', models.CharField(blank=True, max_length=255, null=True)),
                ('include', models.CharField(blank=True, max_length=255, null=True)),
                ('criteria', models.CharField(blank=True, max_length=255, null=True)),
                ('exclude', models.CharField(blank=True, max_length=255, null=True)),
                ('consider', models.CharField(blank=True, max_length=255, null=True)),
                ('icd10', models.CharField(blank=True, max_length=255, null=True)),
                ('icpc2', models.CharField(blank=True, max_length=255, null=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('pym', models.CharField(blank=True, max_length=255, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Icpc4S',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=255, null=True)),
                ('icode', models.CharField(blank=True, max_length=255, null=True)),
                ('iname', models.CharField(blank=True, max_length=255, null=True)),
                ('iename', models.CharField(blank=True, max_length=255, null=True)),
                ('include', models.CharField(blank=True, max_length=255, null=True)),
                ('criteria', models.CharField(blank=True, max_length=255, null=True)),
                ('exclude', models.CharField(blank=True, max_length=255, null=True)),
                ('consider', models.CharField(blank=True, max_length=255, null=True)),
                ('icd10', models.CharField(blank=True, max_length=255, null=True)),
                ('icpc2', models.CharField(blank=True, max_length=255, null=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('pym', models.CharField(blank=True, max_length=255, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Icpc5S',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=255, null=True)),
                ('icode', models.CharField(blank=True, max_length=255, null=True)),
                ('iname', models.CharField(blank=True, max_length=255, null=True)),
                ('iename', models.CharField(blank=True, max_length=255, null=True)),
                ('include', models.CharField(blank=True, max_length=255, null=True)),
                ('criteria', models.CharField(blank=True, max_length=255, null=True)),
                ('exclude', models.CharField(blank=True, max_length=255, null=True)),
                ('consider', models.CharField(blank=True, max_length=255, null=True)),
                ('icd10', models.CharField(blank=True, max_length=255, null=True)),
                ('icpc2', models.CharField(blank=True, max_length=255, null=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('pym', models.CharField(blank=True, max_length=255, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Icpc6S',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=255, null=True)),
                ('icode', models.CharField(blank=True, max_length=255, null=True)),
                ('iname', models.CharField(blank=True, max_length=255, null=True)),
                ('iename', models.CharField(blank=True, max_length=255, null=True)),
                ('include', models.CharField(blank=True, max_length=255, null=True)),
                ('criteria', models.CharField(blank=True, max_length=255, null=True)),
                ('exclude', models.CharField(blank=True, max_length=255, null=True)),
                ('consider', models.CharField(blank=True, max_length=255, null=True)),
                ('icd10', models.CharField(blank=True, max_length=255, null=True)),
                ('icpc2', models.CharField(blank=True, max_length=255, null=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('pym', models.CharField(blank=True, max_length=255, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Icpc7S',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=255, null=True)),
                ('icode', models.CharField(blank=True, max_length=255, null=True)),
                ('iname', models.CharField(blank=True, max_length=255, null=True)),
                ('iename', models.CharField(blank=True, max_length=255, null=True)),
                ('include', models.CharField(blank=True, max_length=255, null=True)),
                ('criteria', models.CharField(blank=True, max_length=255, null=True)),
                ('exclude', models.CharField(blank=True, max_length=255, null=True)),
                ('consider', models.CharField(blank=True, max_length=255, null=True)),
                ('icd10', models.CharField(blank=True, max_length=255, null=True)),
                ('icpc2', models.CharField(blank=True, max_length=255, null=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('pym', models.CharField(blank=True, max_length=255, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Icpc8S',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=255, null=True)),
                ('icode', models.CharField(blank=True, max_length=255, null=True)),
                ('iname', models.CharField(blank=True, max_length=255, null=True)),
                ('iename', models.CharField(blank=True, max_length=255, null=True)),
                ('include', models.CharField(blank=True, max_length=255, null=True)),
                ('criteria', models.CharField(blank=True, max_length=255, null=True)),
                ('exclude', models.CharField(blank=True, max_length=255, null=True)),
                ('consider', models.CharField(blank=True, max_length=255, null=True)),
                ('icd10', models.CharField(blank=True, max_length=255, null=True)),
                ('icpc2', models.CharField(blank=True, max_length=255, null=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('pym', models.CharField(blank=True, max_length=255, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Icpc9S',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=255, null=True)),
                ('icode', models.CharField(blank=True, max_length=255, null=True)),
                ('iname', models.CharField(blank=True, max_length=255, null=True)),
                ('iename', models.CharField(blank=True, max_length=255, null=True)),
                ('include', models.CharField(blank=True, max_length=255, null=True)),
                ('criteria', models.CharField(blank=True, max_length=255, null=True)),
                ('exclude', models.CharField(blank=True, max_length=255, null=True)),
                ('consider', models.CharField(blank=True, max_length=255, null=True)),
                ('icd10', models.CharField(blank=True, max_length=255, null=True)),
                ('icpc2', models.CharField(blank=True, max_length=255, null=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('pym', models.CharField(blank=True, max_length=255, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IcpcLists',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('label', models.CharField(blank=True, max_length=255, null=True)),
                ('icpc_list_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Icpcs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icpc_code', models.CharField(blank=True, max_length=255, null=True)),
                ('icode', models.CharField(blank=True, max_length=255, null=True)),
                ('iname', models.CharField(blank=True, max_length=255, null=True)),
                ('iename', models.CharField(blank=True, max_length=255, null=True)),
                ('include', models.CharField(blank=True, max_length=255, null=True)),
                ('criteria', models.CharField(blank=True, max_length=255, null=True)),
                ('exclude', models.CharField(blank=True, max_length=255, null=True)),
                ('consider', models.CharField(blank=True, max_length=255, null=True)),
                ('icd10', models.CharField(blank=True, max_length=255, null=True)),
                ('icpc2', models.CharField(blank=True, max_length=255, null=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('pym', models.CharField(blank=True, max_length=255, null=True)),
                ('subclass', models.IntegerField(blank=True, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OperationProcesses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oid', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('tid', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('sid', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('pid', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('uid', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('cid', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('operation_id', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Operations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('label', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('operation_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Osms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('label', models.CharField(blank=True, max_length=255, null=True)),
                ('status_machine', models.JSONField(blank=True, null=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
