import firebase_admin
from firebase_admin import credentials, db
from config.settings import DATABASE_URL, SERVICE_ACCOUNT_KEY

# Initialize Firebase Admin SDK
cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
firebase_admin.initialize_app(cred, {
    "databaseURL": DATABASE_URL
})

# Get a reference to the Realtime Database
firebase_db = db.reference()
