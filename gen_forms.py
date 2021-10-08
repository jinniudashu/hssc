import requests
from genlib import *

# ***Create forms***
app = 'forms'
url = 'https://hssc-rcms.herokuapp.com/forms?_publicationState=preview'
res = requests.get(url)
# print(res.status_code)
# print(res.text)
res_json = res.json()
models = []
for obj in res_json:
    
    model_name = obj['name'].replace(' ', '').lower()   # 表单名称
    model_label = obj['label'].replace(' ', '')         # 显示名称
    if obj['style']=='List':                            # 输入风格
        model_style = 1
    else:
        model_style = 0

    models.append((model_name, model_label, model_style))

    #写入models.py & admin.py
    model = write_models(obj, app)
    #写入forms.py
    model = write_forms(obj, app)
    #写入views.py & urls.py
    model = write_views(obj, app)
    #写入templates.html
    model = write_templates(obj, app)


#写入form_list.py
f = open(f'.\\{app}\\form_list.py', 'w', encoding='utf-8')
f.write(f'form_list={models}')
f.close

#最后写入index.html
write_index_html(models, app)