import requests
from genlib import *

# GraphQl style ===================
# query = """query {
#   forms {
#     name
#   	label
#     fid
#   }
# }"""
# url = 'https://hssc-rcms.herokuapp.com/graphql'
# res = requests.post(url, json={'query': query})


# ***Create dictionarires***
app = 'dictionaries'
url = 'https://hssc-rcms.herokuapp.com/dictionaries'
res = requests.get(url)
res_json = res.json()
for obj in res_json:
    # 写入字典model
    dictionary = write_dictionary_model(obj, app)


# ***Create ICPC***
app = 'icpc'
url = 'https://hssc-rcms.herokuapp.com/icpc-lists'
res = requests.get(url)
res_json = res.json()
for obj in res_json:
    # 写入 icpc model
    dictionary = write_icpc_model(obj, app)


# ***Create forms***
app = 'forms'
url = 'https://hssc-rcms.herokuapp.com/forms'
res = requests.get(url)
# print(res.status_code)
# print(res.text)
res_json = res.json()
models = []
for obj in res_json:
    models.append((obj['name'].strip().lower(), obj['label'].strip()))
    #写入models.py
    model = write_models(obj, app)
    #写入forms.py
    model = write_forms(obj, app)
    #写入views.py&urls.py
    model = write_views(obj, app)
    #写入templates.html
    model = write_templates(obj, app)

#最后写入index.html
write_index_html(models, app)
