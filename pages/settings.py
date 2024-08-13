import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore



#>> json database
  
response = requests.get('https://api.jsonsilo.com/public/942c3c3b-3a0c-4be3-81c2-12029def19f5')
# Parse the JSON response
data = response.json()

# Access the question array
def question_objects(section):
 return data.get(section, [])


#>> firebase

# Firebase configuration
firebase_config = {
  "apiKey": "AIzaSyDnbLx28r3PbTTWBUb1RwwfVe3xKFS6crY",
  "authDomain": "crucial-study-390519.firebaseapp.com",
  "projectId": "crucial-study-390519",
  "storageBucket": "crucial-study-390519.appspot.com",
  "messagingSenderId": "1048701385145",
  "appId": "1:1048701385145:web:531265aff5615610901e68"
}

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'projectId': firebase_config['projectId'],
    'storageBucket': firebase_config['storageBucket'],
})

# Get a reference to the Firestore database
db = firestore.client()

# Example: Add a document to a collection
# def add_document(collection_name, document_data):
   # doc_ref = db.collection(collection_name).add(document_data)
   # print(f"Document added with ID: {doc_ref[1].id}")

       

