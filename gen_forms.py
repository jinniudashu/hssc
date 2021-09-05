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
    models.append((obj['name'].strip().lower(), obj['label'].strip()))
    #写入models.py & admin.py
    model = write_models(obj, app)
    #写入forms.py
    model = write_forms(obj, app)
    #写入views.py & urls.py
    model = write_views(obj, app)
    #写入templates.html
    model = write_templates(obj, app)

#最后写入index.html
write_index_html(models, app)