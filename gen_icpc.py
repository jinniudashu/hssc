import requests
from genlib import write_icpc_model

# ***Create ICPC***
app = 'icpc'
url = 'https://hssc-rcms.herokuapp.com/icpc-lists'
res = requests.get(url)
res_json = res.json()
for obj in res_json:
    # 写入 icpc model
    dictionary = write_icpc_model(obj, app)