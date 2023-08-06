import requests
import json
import pandas as pd

def health(token, ticker): 
    url = "https://spawnerapi.com/health/" + ticker + "/" + token
    response = requests.get(url).json()
    df = pd.DataFrame(response)
    return df

def fundamentals(token): 
    url = "https://spawnerapi.com/fundamentals/" + token
    response = requests.get(url).json()
    df = pd.DataFrame(response)
    return df

def macro(token): 
    url = "https://spawnerapi.com/macro/" + token
    response = requests.get(url).json()
    df = pd.DataFrame(response)
    return df

def value(token, ticker): 
    url = "https://spawnerapi.com/value/" + ticker + "/" + token
    response = requests.get(url).json()
    df = pd.DataFrame(response)
    return df

def momentum(token, ticker): 
    url = "https://spawnerapi.com/momentum/" + ticker + "/" + token
    response = requests.get(url).text
    return response

def rsi(token, ticker): 
    url = "https://spawnerapi.com/rsi/" + ticker + "/" + token
    response = requests.get(url).json()
    return response

def tsi(token, ticker): 
    url = "https://spawnerapi.com/tsi/" + ticker + "/" + token
    response = requests.get(url).json()
    return response

def uo(token, ticker): 
    url = "https://spawnerapi.com/uo/" + ticker + "/" + token
    response = requests.get(url).json()
    return response

def stochastic(token, ticker): 
    url = "https://spawnerapi.com/stochastic/" + ticker + "/" + token
    response = requests.get(url).json()
    return response

def kaufman(token, ticker): 
    url = "https://spawnerapi.com/kaufman/" + ticker + "/" + token
    response = requests.get(url).json()
    return response

def macd(token, ticker): 
    url = "https://spawnerapi.com/macd/" + ticker + "/" + token
    response = requests.get(url).json()
    return response

def vortex(token, ticker): 
    url = "https://spawnerapi.com/vortex/" + ticker + "/" + token
    response = requests.get(url).json()
    return response

def kst(token, ticker): 
    url = "https://spawnerapi.com/kst/" + ticker + "/" + token
    response = requests.get(url).json()
    return response

def ichimoku(token, ticker): 
    url = "https://spawnerapi.com/ichimoku/" + ticker + "/" + token
    response = requests.get(url).json()
    return response

def keltner(token, ticker): 
    url = "https://spawnerapi.com/keltner/" + ticker + "/" + token
    response = requests.get(url).json()
    return response

def bollinger(token, ticker): 
    url = "https://spawnerapi.com/bollinger/" + ticker + "/" + token
    response = requests.get(url).json()
    return response
