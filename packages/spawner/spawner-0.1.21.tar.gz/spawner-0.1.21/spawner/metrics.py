import requests
import json
import pandas 

def sharpe(token, ticker, date): 
    url = "https://spawnerapi.com/sharpe/" + ticker + "/" + date + "/" + token
    response = requests.get(url).text
    return round(float(response),2)

def volatility(token, ticker, date): 
    url = "https://spawnerapi.com/volatility/" + ticker + "/" + date + "/" + token
    response = requests.get(url).text
    return round(float(response), 2)

def expected_return(token, ticker, date): 
    url = "https://spawnerapi.com/expected-return/" + ticker + "/" + date + "/" + token
    response = requests.get(url).text
    return round(float(response),2)

def kelly_criterion(token, ticker): 
    url = "https://spawnerapi.com/kelly-criterion/" + ticker + "/" + token
    response = requests.get(url).text
    return round(float(response),2)

