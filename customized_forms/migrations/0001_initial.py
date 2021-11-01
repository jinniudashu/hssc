# Generated by Django 3.2.6 on 2021-10-29 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('label', models.CharField(max_length=100, verbose_name='组件名称')),
                ('field_type', models.CharField(choices=[('char_field', {}), ('text_field', {}), ('integer_field', {}), ('float_field', {}), ('select_field', {}), ('datetime_field', {}), ('calculated_field', {})], max_length=100, verbose_name='类型')),
                ('attribute', models.JSONField(verbose_name='属性')),
            ],
            options={
                'verbose_name': '组件',
                'verbose_name_plural': '组件',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SubForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('label', models.CharField(max_length=100, verbose_name='子表单')),
                ('components', models.CharField(max_length=255, verbose_name='组件清单')),
                ('style', models.CharField(choices=[('detail', '详情'), ('list', '列表')], default='detail', max_length=100, verbose_name='风格')),
            ],
            options={
                'verbose_name': '子表单',
                'verbose_name_plural': '子表单',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Operand_Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('label', models.CharField(blank=True, max_length=100, null=True, verbose_name='表单名称')),
                ('subforms', models.CharField(max_length=255, verbose_name='子表单集')),
                ('layout', models.CharField(choices=[('monomer', '单体'), ('pagination', '分页')], default='monomer', max_length=100, verbose_name='布局')),
                ('meta_form', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customized_forms.subform', verbose_name='元表单')),
            ],
            options={
                'verbose_name': '作业表单',
                'verbose_name_plural': '作业表单',
                'ordering': ['id'],
            },
        ),
    ]