import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("app/agaricleanerdb-firebase-adminsdk-fbsvc-b7483c5bb1.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
