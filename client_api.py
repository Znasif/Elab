import requests
import random

#msg = {'33724': [['syncope', 'vertigo'], 'incontinence'], '33725': [['polyuria', 'polydypsia'], 'diabetes'], '33726': [['tremor', 'intoxication'], 'decubitus ulcer']}
#msg_ = {'33724': ['syncope', 'vertigo'] , '33725': ['polyuria', 'polydypsia'], '33726': ['tremor', 'intoxication']}
files = {'file': open('client_api.py','rb')}
auth=('admin', 'admin12345')
url = "https://elab-ai.herokuapp.com"

res = requests.get(url+'/diag/')
if res.ok:
    print("GET")


def rand_():
    s = ""
    for i in range(random.randint(1, 5)):
        s += str(random.randint(1, 401))+","
    return s[:-1]

msg_ = {"symptomid": rand_(), "age": "40", "gender": "male"}
print(msg_)
res = requests.post(url+'/train/', json=msg_)

if res.ok:
    print("POST", res.json())
else:
    print(res)

res = requests.post(url+'/', files=files)

if res.ok:
    print("POST", res.json())
else:
    print(res)

res = requests.get(url+'/diag/')
if res.ok:
    print("GET")