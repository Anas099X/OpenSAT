from fasthtml import FastHTML
from fasthtml.common import *
import requests

app = FastHTML()

response = requests.get('https://api.jsonsilo.com/public/942c3c3b-3a0c-4be3-81c2-12029def19f5')


# Parse the JSON response
data = response.json()

# Access the 'math' array
def question_objects(section):
 return data.get(section, [])



