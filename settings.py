import os
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dotenv import load_dotenv
from fasthtml.common import *


main_style = (Style('''
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

/* Base Styles */
body {
    margin: 0;
    padding: 0;
    font-family: 'Poppins', sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow-x: hidden;
}

/* Background */
@keyframes waveAnimation {
    0% {
        background-position: 0 center;
    }
    100% {
        background-position: -400px center;
    }
}

body::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    background-image: url("data:image/svg+xml;utf8,%3Csvg width=%223000%22 height=%221400%22 xmlns=%22http:%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cdefs%3E%3ClinearGradient id=%22a%22 gradientTransform=%22rotate(90)%22%3E%3Cstop offset=%225%25%22 stop-color=%22%23f38a8a%22%2F%3E%3Cstop offset=%2295%25%22 stop-color=%22%23f6a7a7%22%2F%3E%3C%2FlinearGradient%3E%3C%2Fdefs%3E%3Cpath fill=%22%23f1edd0%22 d=%22M0 0h3000v1400H0z%22%2F%3E%3Cpath d=%22M0 700c101.95 15.812 203.9 31.623 278 53s120.348 48.318 205-4 207.706-183.897 296-238c88.294-54.103 141.827-30.732 212 8s156.984 92.825 243 71c86.016-21.825 171.235-119.568 265-99 93.765 20.568 196.076 159.448 281 214 84.924 54.552 152.462 24.776 260-5 107.538-29.776 175.076 0 260 54.552 84.924 54.552 187.235 193.432 281 214 93.765 20.568 179.984-77.175 266-99s148.173-46.103 236.5 8c88.327 54.103 184.348 189.318 269 211s176.05 37.188 278 53l-40 700H0Z%22 fill=%22url(%23a)%22%2F%3E%3C%2Fsvg%3E");
    background-size: 150% 100%;
    background-position: 0 center;
    background-repeat: repeat;
    animation: waveAnimation 15s ease-in-out infinite alternate;
}

/* Typography */
.text-primary-500 { color: #fc9d9a; }
.decoration-wavy { text-decoration: underline wavy; }

/* Buttons */
.btn {
    padding: 6px 12px;
    border-radius: 15px;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    font-weight: 600;
    font-size: 0.8rem;
    transition: all 0.3s ease;
    box-shadow: 0 2px 2px rgba(0, 0, 0, 0.25);
}
.btn-primary { background-color: #fc9d9a; color: white; }
.btn-secondary { background-color: #f1edd0; color: black; }
.btn-filter {
    background-color: #f1edd0;
    margin-bottom: 10px;
    font-size:1em;
    color: #000;
    box-shadow: 0 3px 3px rgba(0, 0, 0, 0.35);
  
}
.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
}

/* Layout Components */
.container {
    background-color: #f1edd0;
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    margin: 20px auto;
}

.filter-container {
    transition: all 0.3s ease;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
    text-decoration: none;
    gap: 10px;
    padding: 20px;
    background-color: #f1edd0;
    border-radius: 20px;
    max-height:43vh;
    max-width:92vh;
    align-items: center;
    font-size:12px;
}

.list-content {
    display: flex;
    flex-direction: row;
    justify-content: center;
    flex-wrap: wrap;
    align-content: center;
    text-decoration: none;
    width:150vh;
    gap: 0.6em;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    width: 100%;
    box-sizing: border-box;
    background-color: #f1edd0;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1000;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.logo {
    display: flex;
    align-items: center;
    gap: 5px;
}

.logo h1 {
    font-size: 1.2rem;
    margin: 0;
}

.nav {
    display: flex;
    gap: 10px;
}

main {
    flex-grow: 1;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    padding: 80px 20px 20px;
    margin-top: 60px;
}

/* Scrollbar Styles */
::-webkit-scrollbar {
    width: 20px;
}

::-webkit-scrollbar-track {
    background: #f1edd0;
}

::-webkit-scrollbar-thumb {
    background-color: #fc9d9a;
    border-radius: 20px;
    border: 12px solid #f1edd0;
}

* {
    scrollbar-width: thin;
    scrollbar-color: #fc9d9a #f1edd0;
}

/* For Internet Explorer and Edge */
body {
    -ms-overflow-style: none;
}

/* Profile Card Container */
.profile-card {
    display: flex;
    flex-direction: column;
    background: #f1edd0;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    width: 300px;
    max-width: 100%;
    position: relative;
    color: #333;
}

/* Avatar Section */
.avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: #ff8a80;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 20px;
    color: #fff;
    font-weight: bold;
    margin-bottom: 10px;
}

/* Info Section */
.info {
    font-size: 1.2rem;
    font-weight: bold;
    color: #ff6f61;
    margin-bottom: 5px;
}

.status {
    font-size: 0.75rem;
    color: #4caf50;
    gap-top:-10px;
}

.description {
    font-size: 1.1rem;
    color: #333;
    font-weight: bold;
    margin-bottom: 10px;
}

.email {
    display: flex;
    align-items: center;
    font-size: 0.8rem;
    color: #888;
    margin-bottom: 10px;
}

.email i {
    margin-right: 8px;
}

.location {
    display: flex;
    align-items: center;
    font-size: 0.8rem;
    color: #888;
    margin-bottom: 10px;
}

.location img {
    margin-right: 8px;
}

/* Contact Button */
.contact-btn {
    background-color: #fc9d9a;
    color: #333;
    font-weight: bold;
    border-radius: 10px;
    text-align: center;
    padding: 10px;
    cursor: pointer;
    transition: background-color 0.3s;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}

.contact-btn:hover {

    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
    
}

.contact-btn i {
    margin-right: 5px;
}



/* explore cards */
.card {
    display: grid;
    grid-template-columns: auto 1fr;
    grid-template-rows: auto auto;
    transition: all 0.3s ease;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
    text-decoration: none;
    gap: 10px;
    padding: 20px;
    background-color: #f1edd0;
    border-radius: 20px;
    height:13vh;
    width:42vh;
    align-items: center;
}

.card:hover {
    background-color: rgba(241, 237, 208, 0.5);
    
    
}

.icon {
    grid-row: span 2;
    font-size: 24px;
    color: #fc9d9a;
}

.question-number {
    font-size: 18px;
    color: #000;
    font-weight: bold;
}

.category {
    color: #fc9d9a;
    font-size: 14px;
    padding: 0px 5px;
    border-radius: 5px;
    display: inline-block;
    text-align: right;
    font-size: 1em;
    font-weight: bold;
}
'''))

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