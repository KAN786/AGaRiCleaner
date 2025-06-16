# import firebase_admin
# from firebase_admin import credentials, firestore

# cred = credentials.Certificate("app/agaricleanerdb-firebase-adminsdk-fbsvc-b7483c5bb1.json")
# firebase_admin.initialize_app(cred)

# db = firestore.client()
# do the above for local

import os
import json
import firebase_admin
from firebase_admin import credentials, firestore


firebase_key_dict = json.loads(os.environ["FIREBASE_ADMIN_KEY"])
cred = credentials.Certificate(firebase_key_dict)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)


db = firestore.client()

