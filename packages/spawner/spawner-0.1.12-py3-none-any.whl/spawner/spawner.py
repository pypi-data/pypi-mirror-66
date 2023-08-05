import requests
import json

def fundamentals(token): 
    url = "https://spawnerapi.com/fundamentals/" + token
    response = requests.get(url)
    return response.json()

def sharpe(token, ticker, time_purchased):
    url = "https://spawnerapi.com/sharpe/" + ticker + "/" + time_purchased + "/" + token
    response = requests.get(url)
    return response.text

def kelly_criterion(token, ticker):
    url = "https://spawnerapi.com/kelly-criterion/" + ticker + "/" + token
    response = requests.get(url)
    return response.text

def limit_order(token, identifier, key, ticker, quantity, side, limit_price):
    url = "https://spawnerapi.com/limit/" + identifier + "/" + key + "/" + ticker + "/" + quantity + "/" + side + "/"  + limit_price + "/" + token
    response = requests.get(url)
    return response.text
