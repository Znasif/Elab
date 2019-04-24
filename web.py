import json
import threading

mat = {}
'''
with open("extras/web.json", "r") as f:
    a = f.read()
    links = json.loads(a)
    for i in links:
        mat[links[i][-1]] = i

symptoms_of_diseases = {}

def do_this(l):
    r = links[l]
    for i in r:
        p = i.split("symptoms=")[1]
        q, r = p.split("&symptomids=")
        r = r.split("&locations=")[0]
        symptoms_of_diseases[mat[l]] = {"ids":r, "symptoms":q}

threads = []

with open("extras/level4.json", "r") as f:
    a = f.read()
    links = json.loads(a)
    print(len(links))
    for i in links:
        t = threading.Thread(target=do_this, args=(i,))
        threads.append(t)

for i in threads:
    i.start()

for i in threads:
    i.join()

with open("symptoms_of_diseases.json", 'w+') as f:
    json.dump(symptoms_of_diseases, f)

'''
dis = {}
with open("extras/syms.json", "r") as f:
    a = f.read()
    syms = json.loads(a)
    for i in syms:
        s = syms[i]["ids"]
        if s not in dis:
            dis[s] = []
        dis[s].append(i)

with open("extras/disease.json", 'w+') as f:
    json.dump(dis, f)