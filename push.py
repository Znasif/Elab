import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
from tqdm import tqdm
import threading
import os


cred = credentials.Certificate('elabCre.json')
firebase_admin.initialize_app(cred,  {'storageBucket': 'elab-237906.appspot.com'})
bucket = storage.bucket()

"""
def up(folder):
    for i in os.listdir(folder):
        blob = bucket.blob(folder+i)
        blob.upload_from_filename(folder+i)

up("Data/")

def down(folder):
    for i in os.listdir(folder):
        blob = bucket.blob(folder+i)
        blob.download_to_filename(i)

down("Data/")

"""
#db = firestore.client()

#t = []
# with open("web.json", "r") as f:
#     a = f.read()
#     links = json.loads(a)
#     for i in links:
#         s = i.replace("/", "-")
#         s = s.replace(" ", "_")

#         doc_ref = db.collection(u'webmd').document(s)

#         p = {}
#         for j in links[i]:
#             r = j.replace(" ", "_")
#             p[r] = links[i][j]
#         doc_ref.set(p)
#         break
# print(links[i])
# for j in links[i]:
#     print(j,links[i][j])
# print(links[i])
# break
# a = list(links.keys())
# print((a))

"""
def push_to(i, j):
    doc_ref = db.collection(u'medicine').document(i)
    doc_ref.set(j)

th = []

with open("Data/m.json", "r") as f:
    a = f.read()
    links = json.loads(a)
    for i in links:
        t = threading.Thread(target=push_to, args=(i,links[i],))
        th.append(t)

for i in th:
    i.start()

for i in th:
    i.join()
"""

# with open("disease.json", "r") as f:
#     a = f.read()
#     links = json.loads(a)
#     for i in links:
#         doc_ref = db.collection(u'disease').document(i)
#         doc_ref.set({"condition_array": links[i], "Name": i})


# with open("medicine.json", "r") as f:
#     a = f.read()
#     links = json.loads(a)
#     for i in links:
#         doc_ref = db.collection(u'medicine').document(links[i]["Name"])
#         links[i]["Link"] = i
#         doc_ref.set(links[i])

# users_ref = db.collection(u'disease').document(
#     u'abnormal-gait-(walking)|abnormal-muscle-enlargement-(hypertrophy)|bad-breath|binge-eating')

# users_ref = db.collection(u'activebuildings').where(
#     u'f_array', u'array_contains', u'3oT8eEAlpRYzDPwZWCfA')

# docs = users_ref.get()
# # print(docs.id, docs.to_dict()['b_area'])

# for doc in docs:
#     # print(u'{} => {}'.format(doc.id, doc.to_dict()))
#     i = doc.id
#     j = doc.to_dict()
#     print(i, j['b_area'])
