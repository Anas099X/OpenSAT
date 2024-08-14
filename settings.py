import os
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# JSON database part remains unchanged
response = requests.get('https://api.jsonsilo.com/public/942c3c3b-3a0c-4be3-81c2-12029def19f5')
data = response.json()

def question_objects(section):
    return data.get(section, [])

# Firebase configuration
firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID")
}

# Initialize Firebase
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN")
})

firebase_admin.initialize_app(cred, {
    'projectId': firebase_config['projectId'],
    'storageBucket': firebase_config['storageBucket'],
})

# Get a reference to the Firestore database
db = firestore.client()

# Example: Add a document to a collection
# def add_document(collection_name, document_data):
#     doc_ref = db.collection(collection_name).add(document_data)
#     print(f"Document added with ID: {doc_ref[1].id}")