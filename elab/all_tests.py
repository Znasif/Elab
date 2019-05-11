import os
import json
import collections
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
# from firebase_admin import storage

# CLOUD_SETUP = True

# def cloud_setup(folder="Logs/"):
#     if CLOUD_SETUP!=True:
#         return False
#     cred = credentials.Certificate('elabCre.json')
#     firebase_admin.initialize_app(cred,  {'storageBucket': 'elab-237906.appspot.com'})
#     bucket = storage.bucket()
#     for i in os.listdir(folder):
#         if up(bucket, folder+i):
#             continue
#         exit(0)

# def up(bucket, filepath):
#     if CLOUD_SETUP!=True:
#         return False
#     print("UP")
#     blob = bucket.blob(filepath)
#     blob.upload_from_filename(filepath)
#     try:
#         blob = bucket.blob(filepath)
#         blob.upload_from_filename(filepath)
#         return True
#     except:
#         print("BAD")
#         return False

# cloud_setup()

def read_data():
    with open("Data/m.json", "r") as f:
        a = f.read()
        med = json.loads(a)
    with open("Data/u.json", "r") as f:
        a = f.read()
        lab = json.loads(a)
    return med, lab

def write_data(med, lab):
    with open("Data/m.json", 'w+') as f:
        json.dump(med, f)
    with open("Data/u.json", 'w+') as f:
        json.dump(lab, f)

c = {}
a, b = read_data()

with open("Data/data_med.json", "r") as f:
    a = f.read()
    d = json.loads(a)

def sort_dict(x):
    sorted_x = sorted(x.items(), key=lambda kv: kv[1])[::-1]
    return dict(collections.OrderedDict(sorted_x))

for i in 