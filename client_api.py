import requests
import random

#msg = {'33724': [['syncope', 'vertigo'], 'incontinence'], '33725': [['polyuria', 'polydypsia'], 'diabetes'], '33726': [['tremor', 'intoxication'], 'decubitus ulcer']}
#msg_ = {'33724': ['syncope', 'vertigo'] , '33725': ['polyuria', 'polydypsia'], '33726': ['tremor', 'intoxication']}

res = requests.get('http://192.168.0.109:5000/diag/')
if res.ok:
    print("GET")


def rand_():
    s = ""
    for i in range(random.randint(1, 5)):
        s += str(random.randint(1, 401))+","
    return s[:-1]

msg_ = {"symptomid": rand_(), "age": "40", "gender": "male"}
print(msg_)
res = requests.post('http://192.168.0.109:5000/train/', json=msg_)

if res.ok:
    print("POST", res.json())
else:
    print(res)

msg_ = {"symptomid": rand_(), "age": "40", "gender": "male"}
res = requests.post('http://192.168.0.109:5000/diag/', json=msg_)

if res.ok:
    print("POST", res.json())
else:
    print(res)

res = requests.get('http://192.168.0.109:5000/diag/')
if res.ok:
    print("GET")