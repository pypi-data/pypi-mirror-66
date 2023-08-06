import requests
import json
import pandas 

def sharpe(token, ticker, date): 
    url = "https://spawnerapi.com/sharpe/" + ticker + "/" + date + "/" + token
    response = requests.get(url).text
    return response

def volatility(token, ticker, date): 
    url = "https://spawnerapi.com/sharpe/" + ticker + "/" + date + "/" + token
    response = requests.get(url).text
    return response

def expected_return(token, ticker, date): 
    url = "https://spawnerapi.com/sharpe/" + ticker + "/" + date + "/" + token
    response = requests.get(url).text
    return response

def kelly_criterion(token, ticker, date): 
    url = "https://spawnerapi.com/sharpe/" + ticker + "/" + date + "/" + token
    response = requests.get(url).text
    return response


