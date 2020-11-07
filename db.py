import firebase_admin
import os, json
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate(json.loads(os.environ.get('FIREBASECREDITS')))
firebase_admin.initialize_app(cred)
db = firestore.client()

