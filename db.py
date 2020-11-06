import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate("credits/codeforces-coach-firebase-adminsdk-kiuol-13db75b827.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

