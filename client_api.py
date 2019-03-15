import requests

msg = {'33724': [['syncope', 'vertigo'], 'incontinence'], '33725': [['polyuria', 'polydypsia'], 'diabetes'], '33726': [['tremor', 'intoxication'], 'decubitus ulcer']}
msg_ = {'33724': ['syncope', 'vertigo'] , '33725': ['polyuria', 'polydypsia'], '33726': ['tremor', 'intoxication']}
# res = requests.post('http://192.168.0.109:8080/diag/', json=msg)
res = requests.get('http://192.168.0.109:8080/diag/')
if res.ok:
    print(res.json())