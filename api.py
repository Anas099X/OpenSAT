import os
import requests, json
from dotenv import load_dotenv
from main import *

# Load environment variables from .env file
load_dotenv()

# JSON database part remains unchanged
response = requests.get('https://api.jsonsilo.com/public/942c3c3b-3a0c-4be3-81c2-12029def19f5')
data = response.json()
#data = json.load(open('local_storage.json'))

def question_objects(section):
    return data.get(section, [])


@rt('/api/questions')
def api_questions(section: str = "english", domain: str = "any",limit: int = None):
    # Fetch questions based on section
    questions = question_objects(section.lower())

    filtered_questions = []

    #filter out domain
    for question in questions:
     if domain.lower().replace('%20',' ') == question['domain'].lower():
        filtered_questions.append(question)

    return JSONResponse(questions) if filtered_questions == [] else JSONResponse(filtered_questions[0:limit])



