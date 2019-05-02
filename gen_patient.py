import json

with open("Data/patient.json", "r") as f:
    a = f.read()
    patient = json.loads(a)

with open("Data/u.json", "r") as f:
    a = f.read()
    lab = json.loads(a)

with open("Data/m.json", "r") as f:
    a = f.read()
    med = json.loads(a)

