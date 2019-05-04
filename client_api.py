import requests
import random

#msg = {'33724': [['syncope', 'vertigo'], 'incontinence'], '33725': [['polyuria', 'polydypsia'], 'diabetes'], '33726': [['tremor', 'intoxication'], 'decubitus ulcer']}
#msg_ = {'33724': ['syncope', 'vertigo'] , '33725': ['polyuria', 'polydypsia'], '33726': ['tremor', 'intoxication']}
files = {'file': open('client_api.py','rb')}
auth=('admin', 'admin12345')
#url = "https://elab-ai.herokuapp.com"
url = "http://192.168.0.162:8080"

def rand_(num):
    s = ""
    for i in range(random.randint(1, 5)):
        s += str(random.randint(1, num))+","
    return s[:-1]
    
res = requests.get(url+'/diag/')
if res.ok:
    print("GET Diag")
    nm = len(res.json())
else:
    print(res)

msg_ = {"symptomid": rand_(nm), "age": "40", "gender": "male"}

res = requests.post(url+'/diag/', json=msg_)

if res.ok:
    print("POST", res.json())
    # msg_ = {"symptomid": rand_(nm), "age": "40", "gender": "male"}
    # res = requests.post(url+'/diag/', json=msg_)
else:
    print(res)



res = requests.get(url+'/train/')
if res.ok:
    pat = res.json()["Data Count"]
    print(pat)
else:
    print(res)


msg = {}
for i in range(random.randint(1, 5)):
    msg[str(pat+i)] = {"symptomid": rand_(nm), "age": "40", "gender": "male", "diagnosis":random.randint(0, 20)}

# print(msg)
res = requests.post(url+'/train/', json=msg)

if res.ok:
    print("POST", res.json())
else:
    print(res)
"""
# res = requests.post(url+'/', files=files)

# if res.ok:
#     print("POST", res.json())
# else:
#     print(res)
"""