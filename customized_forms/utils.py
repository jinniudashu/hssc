# 被customized_forms.admin调用
def export_scripts(modeladmin, request, queryset):

    # output_path = '.\\customized_forms\\output\\'   # views.py urls.py 导出路径
    output_path = '.\\forms\\'   # views.py urls.py 导出路径

    def write_to_file(file_name, content, mode='w'):
        f = open(f'{output_path}{file_name}', mode, encoding='utf-8')
        f.write(content)
        f.close
        return f

    # views.py文件头
    vsh = f'''from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.forms import modelformset_factory, inlineformset_factory
from core.models import Operation_proc

from forms.models import *
from forms.forms import *

class Index_view(ListView):
	model = Operation_proc
	template_name = 'index.html'

	# def get(self, request, *args, **kwargs):
	# 	self.object = self.get_object(queryset=Operation_proc.objects.exclude(state=4))

	def get_context_data(self, **kwargs):
		procs = Operation_proc.objects.exclude(state=4)
		todos = []
		for proc in procs:
			todo = {{}}
			todo['operation'] = proc.operation.label
			todo['url'] = f'{{proc.operation.name}}_update_url'
			todo['slug'] = proc.entry
			todos.append(todo)
		context = super().get_context_data(**kwargs)
		context['todos'] = todos
		return context

'''

    # urls.py文件头
    ush = f'''
from django.urls import path
from .views import *

urlpatterns = [
	path('', Index_view.as_view(), name='index'),
	path('index/', Index_view.as_view(), name='index'),'''

    # index.html文件头
    ihsh = f'''{{% extends "base.html" %}}

{{% block content %}}

<br>

<h4>当前任务</h4>
	<section class="list-group">
	{{% for todo in todos %}}
		<a class="list-group-item" href="{{% url todo.url todo.slug %}}">
		{{{{ todo.operation }}}}
		</a>
	{{% endfor %}}
	</section>

<br>

<hr>

<br>

<h4>表单目录</h4>

<section class="list-group">
'''

    views_script = urls_script = index_html_script = ''

    for obj in queryset:
        # Insert into core.models.Form (Auto generate corresponding operation)

        # create views.py, template.html, urls.py
        inquire_forms = [(f['name'], f['style'], f['label']) for f in list(obj.inquire_forms.all().values())]
        mutate_forms = [(f['name'], f['style'], f['label']) for f in list(obj.mutate_forms.all().values())]

        s = CreateScripts(obj.name, obj.label, obj.axis_field, inquire_forms, mutate_forms)
        vs, hs, us, ihs = s.create_script()

        # construct views script
        views_script = views_script + vs
        # construct urls script
        urls_script = urls_script + us
        # create template.html
        write_to_file(f'templates\\{obj.name}_edit.html', hs)
        # construct index.html script
        index_html_script = index_html_script + ihs

    # add header to views.py
    views_script = vsh + views_script
    # add header to urls.py
    urls_script = ush + urls_script + '\n]'
    # add header to index.html
    index_html_script = ihsh + index_html_script + '\n</section>\n{% endblock %}'

    # 写入views.py
    write_to_file('views.py', views_script)
    # 写入urls.py
    write_to_file('urls.py', urls_script)
    # 写入index.html
    write_to_file('templates\\index.html', index_html_script)

    # 写入作业库

export_scripts.short_description = '生成脚本'


class CreateScripts:
    operand_name = ''
    operand_label = ''
    axis_field = ''
    inquire_forms = []
    mutate_forms = []

    view_name = ''
    template_name = ''
    success_url = ''
    form_class = ''

    def __init__(self, operand_name, operand_label, axis_field, inquire_forms, mutate_forms):
        self.operand_name = operand_name
        self.operand_label = operand_label
        self.axis_field = axis_field
        self.inquire_forms = inquire_forms
        self.mutate_forms = mutate_forms

        self.view_name = operand_name.capitalize() + '_CreateView'
        self.template_name = operand_name + '_edit.html'
        self.success_url = '/'
        self.form_class = mutate_forms[0][0].capitalize() + '_ModelForm'

        self.url = self.operand_name + '_create_url'

    def create_script(self):

        vs, hs = self.__iterate_forms()

        # views.py
        view_script = self.__construct_view_script(vs)

        # .html
        html_script = self.__construct_html_script(hs)

        # urls.py
        url_script = self.__construct_url_script()

        # index.html
        index_html_script = self.__construct_index_html_script()

        return view_script, html_script, url_script, index_html_script


    def __iterate_forms(self):
        i = 0       # count forms

        # 把view分为6个部分
        s0 = ''     # inquire_forms
        s1 = ''     # mutate_formsets
        s2 = ''     # POST mutate_forms
        s3 = ''     # GET mutate_forms
        s4 = ''     # context
        s5 = ''     # form_valid

        s6 = ''     # template scripts

        # Iterate inquire_forms
        for form in self.inquire_forms:
            s = c = h = ''
            if form[1] == 'detail':
                s = f'''
        form{i} = {form[0].capitalize()}_ModelForm(instance=self.customer, prefix="form{i}")'''
                c = f'''
        context['form{i}'] = form{i}'''
                h = f'''
        <h5>{form[2]}</h5>
        {{{{ form{i}.as_p }}}}
        <hr>'''

            else:
                s = f'''
        Formset{i} = modelformset_factory({form[0].capitalize()}, form={form[0].capitalize()}_ModelForm, extra=2)
        # formset{i} = Formset{i}(queryset=self.customer.{form[0].lower()}.all(), prefix="formset{i}")
        formset{i} = Formset{i}(prefix="formset{i}")'''
                c = f'''
        context['formset{i}'] = formset{i}'''
                h = f'''
        <h5>{form[2]}</h5>
        {{{{ formset{i}.as_p }}}}
        <hr>'''

            s0 = s0 + s
            s4 = s4 + c
            s6 = s6 + h
            i += 1
        
        # Iterate mutate_formsets
        for form in self.mutate_forms:
            s_1=s_2=s_3=c=s_5= h =''

            if form[1] == 'detail':
                s_2 = f'''
            form{i} = {form[0].capitalize()}_ModelForm(self.request.POST, prefix="form{i}")'''
                s_3 = f'''
            form{i} = {form[0].capitalize()}_ModelForm(prefix="form{i}")'''
                c = f'''
        context['form{i}'] = form{i}'''
                s_5 = f'''
        f = context['form{i}'].save(commit=False)
        f.customer = self.customer
        f.operator = self.operator
        f.save()
                '''
                h = f'''
        <h5>{form[2]}</h5>
        {{{{ form{i}.as_p }}}}
        <hr>'''

            else:
                s_1 = f'''
        Formset{i} = modelformset_factory({form[0].capitalize()}, form={form[0].capitalize()}_ModelForm, extra=2)'''
                s_2 = f'''
            formset{i} = Formset{i}(self.request.POST, prefix="formset{i}")'''
                s_3 = f'''
            formset{i} = Formset{i}(prefix="formset{i}")'''
                c = f'''
        context['formset{i}'] = formset{i}'''
                s_5 = f'''
        for form in context['formset{i}']:
            f = form.save(commit=False)
            f.customer = self.customer
            f.operator = self.operator
            f.save()
                '''
                h = f'''
        <h5>{form[2]}</h5>
        {{{{ formset{i}.as_p }}}}
        <hr>'''

            s1 = s1 + s_1
            s2 = s2 + s_2
            s3 = s3 + s_3
            s4 = s4 + c
            s5 = s5 + s_5

            s6 = s6 + h

            i += 1

        vs = [s0, s1, s2, s3, s4, s5]
        
        return vs, s6


    def __construct_view_script(self, vs):

        script_head = f'''
class {self.view_name}(CreateView):
    template_name = '{self.template_name}'
    success_url = '{self.success_url}'
    form_class = {self.form_class}

    user = User.objects.get(id=1)
    customer = Customer.objects.get(user=user)
    operator = Staff.objects.get(user=user)

    def get_context_data(self, **kwargs):
        context = super({self.view_name}, self).get_context_data(**kwargs)
        '''

        script_body = f'''
        # inquire_forms''' + vs[0] + f'''
        # mutate_formsets''' + vs[1] + f'''
        # mutate_forms
        if self.request.method == 'POST':'''+ vs[2] + f'''
        else:''' + vs[3] + f'''
        # context''' + vs[4] + f'''

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # form_valid''' + vs[5]
        
        script_foot = f'''
        return super({self.view_name}, self).form_valid(form)

        '''

        s = f'{script_head}{script_body}{script_foot}'
        return s

    def __construct_html_script(self, hs):
        script_head = f'''{{% extends "base.html" %}}

{{% load crispy_forms_tags %}}

{{% block content %}}
'''

        script_body = f'''
	<form action={{% url '{self.url}' %}} method='POST' enctype='multipart/form-data'> 
		{{% csrf_token %}}
            ''' + hs

        script_foot = f'''
		<input type="submit" value="提交" /> 
	</form>

{{% endblock %}}
'''

        s = f'{script_head}{script_body}{script_foot}'
        return s

    
    def __construct_url_script(self):
        return f'''
    path('{self.operand_name}', {self.view_name}.as_view(), name='{self.url}'),'''


    def __construct_index_html_script(self):
        return f'''<a class='list-group-item' href='{{% url "{self.url}" %}}'>
		{self.operand_label}
	</a>
        '''