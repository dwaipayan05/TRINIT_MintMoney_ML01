from urllib import response
import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('RAPID_API_KEY')
url = "https://covid-19-data.p.rapidapi.com/country"



headers = {
    'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
    'x-rapidapi-key': {api_key}
}

def get_StatsbyCountry(countryName):
    querystring = {"name": {countryName}}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    return data

if __name__ == "__main__":
    get_StatsbyCountry("india")

