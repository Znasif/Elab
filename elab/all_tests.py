import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

CLOUD_SETUP = True

def cloud_setup(folder="Logs/"):
    if CLOUD_SETUP!=True:
        return False
    cred = credentials.Certificate('elabCre.json')
    firebase_admin.initialize_app(cred,  {'storageBucket': 'elab-237906.appspot.com'})
    bucket = storage.bucket()
    for i in os.listdir(folder):
        if up(bucket, folder+i):
            continue
        exit(0)

def up(bucket, filepath):
    if CLOUD_SETUP!=True:
        return False
    print("UP")
    blob = bucket.blob(filepath)
    blob.upload_from_filename(filepath)
    try:
        blob = bucket.blob(filepath)
        blob.upload_from_filename(filepath)
        return True
    except:
        print("BAD")
        return False

cloud_setup()