import requests
from genlib import write_dictionary_model

# ***Create dictionarires***
app = 'dictionaries'
url = 'https://hssc-rcms.herokuapp.com/dictionaries?_publicationState=preview'
res = requests.get(url)
res_json = res.json()
for obj in res_json:
    # 写入字典model
    dictionary = write_dictionary_model(obj, app)