import os
# Create urls.py
def write_urls(model, operation, app):
    path = f'.\\{app}\\urls.py'
    
    model = model.lower()
    if operation == 'list':
        url = f'{model}s/'
    elif operation == 'create':
        url = f'{model}/create/'
    elif operation == 'detail':
        url = f'{model}/<str:slug>/'
    elif operation == 'update':
        url = f'{model}/<str:slug>/update/'
    elif operation == 'delete':
        url = f'{model}/<str:slug>/delete/'

    f = open(path, 'a')
    f.write(f'\n\tpath("{url}", {model.capitalize()}_{operation.capitalize()}View.as_view(), name="{model}_{operation}_url"),')
    f.close

    return


# Create admin.py
def write_admin(model_name, fk_name, app):

    modelAdmin_name = f'{model_name.capitalize()}Admin'

    path = f'.\\{app}\\admin.py'
    f = open(path, 'a')

    f.write(f'\n\nclass {modelAdmin_name}(admin.ModelAdmin):')
    if fk_name:
        f.write(f'\n\tautocomplete_fields = ["{fk_name}"]')
    else:
        f.write(f'\n\tlist_display = [field.name for field in Icpc._meta.fields]')
        f.write(f'\n\tsearch_fields=["iname", "pym"]')
        f.write(f'\n\tordering = ["icpc_code"]')
	

    f.write(f'\nadmin.site.register({model_name.capitalize()}, {modelAdmin_name})')

    f.close


# Create dictionary-data(Enum)
def write_dictionary_enums(model, dict_data, app):

    # 构造enum串
    dict_str = ''
    i= 0
    for item in dict_data:
        dict_str = dict_str + f'({i},"{item["value"]}"), '
        i += 1

    # 写入enums.py
    path = f'.\\{app}\\enums.py'
    f = open(path, 'a', encoding='utf-8')
    print(dict_str)
    f.write(f'\n\n{model}Enum = [{dict_str}]')
    f.close

# Create dictionaries.py
def write_dictionary_model(obj, app):

    model = obj['name'].replace(' ', '').capitalize()
    label = obj['label'].replace(' ', '')
    dict_data = obj['dictionary_data']

    # 从dictionaries里取字典表名创建字典Model
    path = f'.\\{app}\\models.py'
    f = open(path, 'a', encoding='utf-8')
    f.write(f'\n\n\nclass {model}(models.Model):')

    # 写入field
    f.write(f'\n\tname = models.CharField(max_length=40, blank=True, null=True,  verbose_name="名称")')
    f.write(f'\n\tscore = models.SmallIntegerField(blank=True, null=True, verbose_name="分值")')

    # 实例名称显示为value
    f.write('\n\n\tdef __str__(self):')
    f.write(f'\n\t\treturn self.name')

    # model名称显示为中文
    f.write('\n\n\tclass Meta:')
    f.write(f'\n\t\tverbose_name = "{label}"')
    f.write(f'\n\t\tverbose_name_plural = "{label}"')

    f.close

    # 在admin.py 中注册字典model
    path = f'.\\{app}\\admin.py'
    f = open(path, 'a')
    f.write(f'\n\nadmin.site.register({model})')
    f.close

    # 在app里创建字典Enum
    write_dictionary_enums(model, dict_data, app)

    return model


def write_icpc_model(obj, app):
    # 从icpc-lists里取icpc表名创建icpc Model
    model = obj['name'].replace(' ', '').capitalize()
    label = obj['label'].replace(' ', '')

    path = f'.\\{app}\\models.py'
    f = open(path, 'a', encoding='utf-8')
    f.write(f'\n\n\nclass {model}(models.Model):')

    # 构造field
    icpc_code = 'icpc_code = models.CharField(max_length=5, blank=True, null=True, verbose_name="icpc码")'
    icode = 'icode = models.CharField(max_length=3, blank=True, null=True, verbose_name="分类码")'
    iname = 'iname = models.CharField(max_length=255, blank=True, null=True, verbose_name="名称")'
    iename = 'iename = models.CharField(max_length=255, blank=True, null=True, verbose_name="English Name")'
    include = 'include = models.CharField(max_length=255, blank=True, null=True, verbose_name="包含")'
    criteria = 'criteria = models.CharField(max_length=255, blank=True, null=True, verbose_name="准则")'
    exclude = 'exclude = models.CharField(max_length=255, blank=True, null=True, verbose_name="排除")'
    consider = 'consider = models.CharField(max_length=255, blank=True, null=True, verbose_name="考虑")'
    icd10 = 'icd10 = models.CharField(max_length=8, blank=True, null=True, verbose_name="ICD10")'
    icpc2 = 'icpc2 = models.CharField(max_length=10, blank=True, null=True, verbose_name="ICPC2")'
    note = 'note = models.CharField(max_length=255, blank=True, null=True, verbose_name="备注")'
    pym = 'pym = models.CharField(max_length=25, blank=True, null=True, verbose_name="拼音码")'


    # 写入fields
    f.write(f'\n\t{icpc_code}')
    f.write(f'\n\t{icode}')
    f.write(f'\n\t{iname}')
    f.write(f'\n\t{iename}')
    f.write(f'\n\t{include}')
    f.write(f'\n\t{criteria}')
    f.write(f'\n\t{exclude}')
    f.write(f'\n\t{consider}')
    f.write(f'\n\t{icd10}')
    f.write(f'\n\t{icpc2}')
    f.write(f'\n\t{note}')
    f.write(f'\n\t{pym}')

    # 实例名称显示为value
    f.write('\n\n\t' + 'def __str__(self):')
    f.write(f'\n\t\treturn self.iname')

    # model名称显示为中文
    f.write('\n\n\t' + 'class Meta:')
    f.write(f'\n\t\tverbose_name = "{label}"')
    f.write(f'\n\t\tverbose_name_plural = "{label}"')

    f.close

    # 向admin.py写入search_fields
    write_admin(model, None, app)

    return model


# Create models.py 
def write_models(obj, app):
    # ***待实现：表单Model与字典Model建立外键关联****
    model = obj['name'].replace(' ', '').capitalize()
    model_label = obj['label'].replace(' ', '')    
    fields = obj['fields']
    title = fields[0]['name'].replace(' ', '').lower()

    path = f'.\\{app}\\models.py'

    f = open(path, 'a', encoding='utf-8')
    f.write(f'\n\n\nclass {model}(models.Model):')
    # 写入每个field
    for field in fields:
        # 构造field参数
        name = field['name'].replace(' ', '').lower()
        label = field['label'].replace(' ', '')
        parameters = field['field_parameters']
        # group = field['group']
        # input_style = field['input_style']
        if 'CharField' in parameters:
            # if field['auxiliary_input'] is not None:
            if field['auxiliary_input']:
                # 获得辅助输入代码表名
                aux_name = field['auxiliary_input']['name'].strip().capitalize()
                parameters = parameters + f'(max_length=60, blank=True, null=True, choices={aux_name}Enum, verbose_name="{label}")'
            elif field['icpc_list']:
                icpc_list = field['icpc_list']['name'].strip().capitalize()
                parameters = f'ForeignKey({icpc_list}, db_column="icpc_code", null=True, on_delete=models.SET_NULL, verbose_name="{label}")'                
                # 外键关系，向admin.py写入autocomplete_fields
                write_admin(model, name, app)
            else:
                parameters = parameters + f'(max_length=60, blank=True, null=True, verbose_name="{label}")'
        elif 'TextField' in parameters:
            parameters = parameters + f'(max_length=1024, blank=True, null=True, verbose_name="{label}")'
        elif 'SmallIntegerField' in parameters:
            parameters = parameters + f'(blank=True, null=True, verbose_name="{label}")'
        elif 'DecimalField' in parameters:
            parameters = parameters + f'(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="{label}")'
        elif 'FloatField' in parameters:
            parameters = parameters + f'(blank=True, null=True, verbose_name="{label}")'
        elif 'Date' in parameters:
            parameters = parameters + f'(blank=True, null=True, default=timezone.now, verbose_name="{label}")'
        # 写入field信息
        f.write(f'\n\t{name} = models.{parameters}')

    
    # 写入slug field
    f.write(f'\n\tslug = models.SlugField(max_length=150, unique=True, blank=True)')
    f.write('\n\n\tdef __str__(self):')
    f.write(f'\n\t\treturn self.{title}')

    # class Meta: model名称显示为中文, 排序
    f.write('\n\n\tclass Meta:')
    f.write(f'\n\t\tverbose_name = "{model_label}"')
    f.write(f'\n\t\tverbose_name_plural = "{model_label}"')
    f.write(f'\n\t\tordering = []')

    # get_absolute_url(self):
    f.write('\n\n\tdef get_absolute_url(self):')
    f.write(f'\n\t\treturn reverse("{model.lower()}_detail_url", kwargs={{"slug":self.slug}})')

    # get_update_url(self):
    f.write('\n\n\tdef get_update_url(self):')
    f.write(f'\n\t\treturn reverse("{model.lower()}_update_url", kwargs={{"slug":self.slug}})')

    # get_delete_url(self):
    f.write('\n\n\tdef get_delete_url(self):')
    f.write(f'\n\t\treturn reverse("{model.lower()}_delete_url", kwargs={{"slug":self.slug}})')

    # save(self, *args, **kwargs):
    f.write('\n\n\tdef save(self, *args, **kwargs):')
    f.write(f'\n\t\tif not self.id:')
    f.write(f'\n\t\t\tself.slug = gen_slug(self._meta.model_name)')
    f.write(f'\n\t\tsuper().save(*args, **kwargs)')

    f.close

    return model


# Create forms.py
def write_forms(obj, app):
    model = obj['name'].replace(' ', '').capitalize()
    fields = obj['fields']
    # 构造fields名称list, widgets
    field_names = []
    widgets = ''
    for field in fields:
        name = field['name'].replace(' ', '').lower()
        field_names.append(name)

        # 如果是char-field,且icpc_list为空，且auxiliary_input非空,根据input_style 构造 widgets={}
        if field['__component'] == 'fields.char-field' and field['icpc_list'] is None and field['auxiliary_input'] is not None:
            if field['input_style'] == 'Dropdown_list':
                widgets = f'{widgets}"{name}": Select(),'
            elif field['input_style'] == 'Single_choice':
                widgets = f'{widgets}"{name}": RadioSelect(),'
            elif field['input_style'] == 'Multi_choice':
                widgets = f'{widgets}"{name}": CheckboxSelectMultiple(),'


    path = f'.\\{app}\\forms.py'

    f = open(path, 'a', encoding='utf-8')
    f.write(f'\n\n\nclass {model}_ModelForm(ModelForm):')
    f.write(f'\n\tclass Meta:')
    f.write(f'\n\t\tmodel = {model}')
    f.write(f'\n\t\tfields = {field_names}')
    f.write(f'\n\t\twidgets = {{{widgets}}}')
    # Also can use: fields = '__all__'

    f.write(f'\n\n\t@property')
    f.write(f'\n\tdef helper(self):')
    f.write(f'\n\t\thelper = FormHelper()')
    f.write(f'\n\t\thelper.layout = Layout(HTML("<hr />"))')
    f.write(f'\n\t\tfor field in self.Meta().fields:')
    f.write(f'\n\t\t\thelper.layout.append(Field(field, wrapper_class="row"))')
    f.write(f'\n\t\thelper.layout.append(Submit("submit", "保存", css_class="btn-success"))')
    f.write(f'\n\t\thelper.field_class = "col-8"')
    f.write(f'\n\t\thelper.label_class = "col-2"')
    f.write(f'\n\t\treturn helper')


    f.write(f'\n\n\tdef clean_slug(self):')
    f.write(f'\n\t\tnew_slug = self.cleaned_data.get("slug").lower()')
    f.write(f'\n\t\tif new_slug == "create":')
    f.write(f'\n\t\t\traise ValidationError("Slug may not be create")')
    f.write(f'\n\t\treturn new_slug')

    f.close

    return model


# Create views.py (Mixin)
def write_views(obj, app):
    model = obj['name'].replace(' ', '').capitalize()
    
    path = f'.\\{app}\\views.py'

    f = open(path, 'a', encoding='utf-8')

    # Create class ModelListView(ListView):
    f.write(f'\n\n\nclass {model}_ListView(ListView):')
    f.write(f'\n\tcontext_object_name = "{model.lower()}s"')
    f.write(f'\n\ttemplate_name = "{model.lower()}_list.html"')
    f.write(f'\n\n\tdef get_queryset(self):')
    f.write(f'\n\t\treturn {model}.objects.all()')
    # Create list url
    write_urls(model, 'list', app)

    # Create class ModelCreateView(SuccessMessageMixin, CreateObjectMixin, CreateView):
    f.write(f'\n\n\nclass {model}_CreateView(SuccessMessageMixin, CreateView):')
    f.write(f'\n\ttemplate_name = "{model.lower()}_edit.html"')
    f.write(f'\n\tform_class = {model}_ModelForm')
    f.write(f'\n\tsuccess_message = "保存成功！"')
    # Create create url
    write_urls(model, 'create', app)

    # Create class ModelDetail(DetailView):
    f.write(f'\n\n\nclass {model}_DetailView(DetailView):')
    f.write(f'\n\tmodel = {model}')
    f.write(f'\n\tcontext_object_name = "{model.lower()}"')
    f.write(f'\n\ttemplate_name = "{model.lower()}_detail.html"')
    f.write(f'\n\n\tdef get_object(self):')
    f.write(f'\n\t\t{model.lower()} = super({model}_DetailView, self).get_object()')
    f.write(f'\n\t\tform = {model}_ModelForm(instance={model.lower()})')
    f.write(f'\n\t\treturn form')
    # Create detail url
    write_urls(model, 'detail', app)

    # Create ModelUpdateView(SuccessMessageMixin, UpdateObjectMixin, UpdateView):
    f.write(f'\n\n\nclass {model}_UpdateView(SuccessMessageMixin, UpdateView):')
    f.write(f'\n\ttemplate_name = "{model.lower()}_edit.html"')
    f.write(f'\n\tform_class = {model}_ModelForm')
    f.write(f'\n\tsuccess_message = "保存成功！"')
    f.write(f'\n\n\tdef get_queryset(self):')
    f.write(f'\n\t\treturn {model}.objects.all()')
    # Create update url
    write_urls(model, 'update', app)

    # Create class ModelDelete(DeleteObjectMixin, View):
    f.write(f'\n\n\nclass {model}_DeleteView(DeleteObjectMixin, View):')
    f.write(f'\n\tmodel = {model}')
    f.write(f'\n\ttemplate = "{model.lower()}_delete.html"')
    f.write(f'\n\tredirect_url = "{model.lower()}_list_url"')
    f.write(f'\n\traise_exception = True')
    # Create delete url
    write_urls(model, 'delete', app)


    f.close

    return model


# Create templates/xxx.html
def write_templates(obj, app):
    model = obj['name'].replace(' ', '').lower()
    label = obj['label'].replace(' ', '')    

    # Create list.html
    path = f'.\\{app}\\templates\\{model}_list.html'
    f = open(path, 'w', encoding='utf-8')
    f.write(f'\n\n{{% extends "base.html" %}}')
    f.write(f'\n\n{{% block content %}}')
    f.write(f'\n\n<h4>{label}</h4>')
    f.write(f'\n\n<a href="{{% url "{model}_create_url" %}}">')
    f.write(f'\n\t\t\t新增')
    f.write(f'\n\t\t</a>')
    f.write(f'\n\n<section class="list-group">')
    f.write(f'\n\t{{% for {model} in {model}s %}}')
    f.write(f'\n\t\t<a class="list-group-item" href="{{% url "{model}_detail_url" {model}.slug %}}">')
    f.write(f'\n\t\t\t{{{{ {model} }}}}')
    f.write(f'\n\t\t</a>')
    f.write(f'\n\t{{% endfor %}}')
    f.write(f'\n</section>')
    f.write(f'\n\n{{% endblock %}}')
    f.close

    # Create edit.html
    path = f'.\\{app}\\templates\\{model}_edit.html'
    f = open(path, 'w', encoding='utf-8')
    f.write(f'\n\n{{% extends "base.html" %}}')
    f.write(f'\n\n{{% load crispy_forms_tags %}}')
    f.write(f'\n\n{{% block content %}}')
    f.write(f'\n\n\t{{% crispy form %}}')
    f.write(f'\n\n{{% endblock %}}')
    f.close

    # Create detail.html
    path = f'.\\{app}\\templates\\{model}_detail.html'
    f = open(path, 'w', encoding='utf-8')
    f.write(f'\n\n{{% extends "base.html" %}}')
    f.write(f'\n\n{{% load crispy_forms_tags %}}')
    f.write(f'\n\n{{% block content %}}')
    f.write(f'\n\n\t{{% crispy {model} %}}')
    f.write(f'\n\n{{% endblock %}}')
    f.close

    # Create delete.html
    path = f'.\\{app}\\templates\\{model}_delete.html'
    f = open(path, 'w', encoding='utf-8')
    f.close

    return


# Create index.html
def write_index_html(models, app):
    path = f'.\\{app}\\templates\\index.html'
    f = open(path, 'w', encoding='utf-8')
    f.write(f'\n\n{{% extends "base.html" %}}')
    f.write(f'\n\n{{% block content %}}')
    f.write(f'\n\n<h4>表单目录</h4>')
    f.write(f'\n\n<section class="list-group">')

    for model in models:
        # model[0]: form name
        # model[1]: form label
        f.write(f'\n\t<a class="list-group-item" href="{{% url "{model[0]}_list_url" %}}">')
        f.write(f'\n\t\t{model[1]}')
        f.write(f'\n\t</a>')

    f.write(f'\n\n</section>')
    f.write(f'\n\n{{% endblock %}}')
    f.close


# Create apps.py
def write_apps():
    pass


# Create init.py
def write_init():
    pass


# Create signals.py
def write_signals():
    pass
