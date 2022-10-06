# Generated by Django 3.2.6 on 2022-09-27 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CycleUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='名称')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('hssc_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='hsscID')),
                ('pym', models.CharField(blank=True, max_length=255, null=True, verbose_name='拼音码')),
                ('cycle_unit', models.CharField(blank=True, max_length=255, null=True, verbose_name='周期单位')),
                ('days', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='天数')),
            ],
            options={
                'verbose_name': '服务周期单位',
                'verbose_name_plural': '服务周期单位',
            },
        ),
        migrations.AlterModelOptions(
            name='servicepackagedetail',
            options={'ordering': ['order'], 'verbose_name': '服务内容模板', 'verbose_name_plural': '服务内容模板'},
        ),
        migrations.RemoveField(
            model_name='servicepackage',
            name='overtime',
        ),
        migrations.AddField(
            model_name='servicepackagedetail',
            name='order',
            field=models.PositiveSmallIntegerField(default=100, verbose_name='顺序'),
        ),
        migrations.AlterField(
            model_name='servicepackagedetail',
            name='cycle_unit',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.cycleunit', verbose_name='周期单位'),
        ),
    ]