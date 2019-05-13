import json
import collections

s = [chr(i) for i in range(ord("a"), ord("z")+1)]
t = [chr(i) for i in range(ord("A"), ord("Z")+1)]
nums = [str(i) for i in range(10)]

def all_s(nm):
    nm_ = nm.lower().split(" ")
    s_ = ""
    p_ = []
    for i in nm_[::-1]:
        s_ = i+" "+s_
        for j in range(1, len(s_)):
            p_.append(s_[:j])
    return p_

def repl(i):
    r = i.replace(" ", "_")
    j = ""
    for k in r:
        j += k if k in s+t+nums+["_"] else ""
    return j

# symptom_name_to_id = {}
# symptom_id_to_name = {}
# count_in_patient = {}

# with open("Data/patient.json", "r") as f:
#     a = f.read()
#     patient = json.loads(a)

# with open("Data/symptom_pattern.json", "r") as f:
#     a = f.read()
#     symptom_pattern = json.loads(a)

# for j, i in enumerate(symptom_pattern):
#     symptom_id_to_name[j] = i
#     symptom_name_to_id[i] = j
#     count_in_patient[i] = 0

# for i in patient:
#     for j in patient[i][0]:
#         count_in_patient[j] += 1

# for i in count_in_patient:
#     print(i, count_in_patient[i])

# def sort_dict(x):
#     sorted_x = sorted(x.items(), key=lambda kv: kv[1])[::-1]
#     return collections.OrderedDict(sorted_x)


# common_symptoms = {}
# sorted_dict = sort_dict(count_in_patient)

# for i in sorted_dict:
#     j = repl(i)
#     common_symptoms[j if j!="" else "null"] = {"name":i, "id":symptom_name_to_id[i], "count":sorted_dict[i], "search": all_s(i)}

# with open("Data/common.json", 'w+') as f:
#     json.dump(common_symptoms, f)
"""
l_ = {}

with open("Data/labtest.json", "r") as f:
    a = f.read()
    labtests = json.loads(a)

for i in labtests:
    j = labtests[i]["link"].split("https://labtestsonline.org/tests/")[1].replace("-", "_")
    if j not in l_:
        l_[j] = {"name": [], "search": []}
        for k in labtests[i]:
            l_[j][repl(k)] = labtests[i][k]
    l_[j]["name"].append(i)
    l_[j]["search"] += all_s(i)
    l_[j]["search"] = list(set(l_[j]["search"]))

with open("Data/up_lab.json", 'w+') as f:
    json.dump(l_, f)
"""
l_ = {}

with open("extras/medicine.json", "r") as f:
    a = f.read()
    med = json.loads(a)

for i in med:
    j = i.split("/")[-1].replace("-", "_")
    l_[j] = {"link":i}
    for k in med[i]:
        k_ = k.replace("&", "and")
        l_[j][repl(k_)] = med[i][k]
    l_[j]["search"] = all_s(med[i]["Name"])

with open("Data/med.json", 'w+') as f:
    json.dump(l_, f)