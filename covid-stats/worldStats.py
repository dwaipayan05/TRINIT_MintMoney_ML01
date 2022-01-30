import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('RAPID_API_KEY')

url = "https://covid-19-data.p.rapidapi.com/totals"

headers = {
    'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
    'x-rapidapi-key': {api_key}
}

response = requests.request("GET", url, headers=headers)
print(response.json())
