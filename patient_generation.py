import numpy as np
import random as rn
import json

# Randomize sampling so that anomalous behaviour of the model can be rectified

with open("Data/new.json", "r") as f:
    a = f.read()
    diag = json.loads(a)

patient = {}
num = 0

for i in diag:
    j, k = diag[i]
    n = len(j)
    j = np.array(j)
    for r in range(k):
        p = rn.randint(n//2, n)
        c = rn.sample(range(n), p)
        patient[num] = [list(j[c]), i]
        num += 1

with open("patient.json", 'w+') as f:
   json.dump(patient, f)