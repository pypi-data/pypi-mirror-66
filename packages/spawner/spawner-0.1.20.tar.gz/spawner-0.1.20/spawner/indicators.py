import requests
import json
import pandas 

def health(token, ticker): 
    url = "https://spawnerapi.com/health/" + ticker + "/" + token
    response = requests.get(url).json()
    return response

def fundamentals(token): 
    url = "https://spawnerapi.com/fundamentals/" + token
    response = requests.get(url).json()
    return response.read_json()

def macro(token): 
    url = "https://spawnerapi.com/macro/" + token
    response = requests.get(url).json()
    return response

def rsi(token, ticker): 
    url = "https://spawnerapi.com/rsi/" + token
    response = requests.get(url).json()
    return response

def stochastic(token, ticker): 
    url = "https://spawnerapi.com/stochastic/" + token
    response = requests.get(url).json()
    return response

def kaufman(token): 
    url = "https://spawnerapi.com/kaufman/" + token
    response = requests.get(url).json()
    return response

def momentum(token): 
    url = "https://spawnerapi.com/momentum/" + ticker + "/" + token
    response = requests.get(url).text
    return response
                