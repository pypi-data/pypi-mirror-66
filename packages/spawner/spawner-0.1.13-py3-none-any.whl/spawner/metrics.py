import requests
import json
import pandas 

def sharpe(token, ticker): 
    url = "https://spawnerapi.com/sharpe/" + token
    response = requests.get(url).text
    return response