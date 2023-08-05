import requests
import json
import pandas 

def health(token, ticker): 
    url = "https://spawnerapi.com/health/" + token
    response = requests.get(url).json()
    return response.read_json()

def fundamentals(token): 
    url = "https://spawnerapi.com/fundamentals/" + token
    response = requests.get(url).json()
    return response.read_json()

def macro(token): 
    url = "https://spawnerapi.com/macro/" + token
    response = requests.get(url).json()
    return response.read_json()

def rsi(token, ticker): 
    url = "https://spawnerapi.com/rsi/" + token
    response = requests.get(url).json()
    return response.read_json()

def stochastic(token, ticker): 
    url = "https://spawnerapi.com/stochastic/" + token
    response = requests.get(url).json()
    return response.read_json()

def kaufman(token): 
    url = "https://spawnerapi.com/kaufman/" + token
    response = requests.get(url).json()
    return response.read_json()
                