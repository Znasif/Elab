import requests

res = requests.post('http://127.0.0.1:5000/diag/', json={"60000":["syncope", "vertigo"]})
if res.ok:
    print(res.json())