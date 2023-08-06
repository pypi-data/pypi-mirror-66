import requests
import json
import pandas 

def volatility(token, ticker, purchase_date, purchase_price): 
    url = "https://spawnerapi.com/volatility/" + ticker + "/" + purchase_date + "/" + purchase_price + "/" + token
    response = requests.get(url).text
    return round(float(response),2)

def expected_return(token, ticker, purchase_date, purchase_price): 
    url = "https://spawnerapi.com/expected_return/" + ticker + "/" + purchase_date + "/" + purchase_price + "/" + token
    response = requests.get(url).text
    return round(float(response),2)

def max_drawdown(token, ticker, purchase_date, purchase_price): 
    url = "https://spawnerapi.com/max_drawdown/" + ticker + "/" + purchase_date + "/" + purchase_price + "/" + token
    response = requests.get(url).text
    return round(float(response),2)

def sharpe(token, ticker, purchase_date, purchase_price): 
    url = "https://spawnerapi.com/sharpe/" + ticker + "/" + purchase_date + "/" + purchase_price + "/" + token
    response = requests.get(url).text
    return round(float(response),2)

def calmar(token, ticker, purchase_date, purchase_price): 
    url = "https://spawnerapi.com/calmar/" + ticker + "/" + purchase_date + "/" + purchase_price + "/" + token
    response = requests.get(url).text
    return round(float(response),2)

def sortino(token, ticker, purchase_date, purchase_price): 
    url = "https://spawnerapi.com/sortino/" + ticker + "/" + purchase_date + "/" + purchase_price + "/" + token
    response = requests.get(url).text
    return round(float(response),2)

def value_at_risk(token, ticker, purchase_date, purchase_price): 
    url = "https://spawnerapi.com/value-at-risk/" + ticker + "/" + purchase_date + "/" + purchase_price + "/" + token
    response = requests.get(url).text
    return round(float(response),2)

def kelly_criterion(token, ticker): 
    url = "https://spawnerapi.com/kelly_criterion/" + ticker + "/" + token
    response = requests.get(url).text
    return round(float(response),2)

def implied_volatility(token, ticker): 
    url = "https://spawnerapi.com/implied_volatility/" + ticker + "/" + token
    response = requests.get(url).text
    return round(float(response),2)