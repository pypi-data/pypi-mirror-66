import requests
import json
import pandas 


def answer(token, question): 
    url = "https://spawnerapi.com/answer/" + token
    trade_list = {"text": question}
    headers={'Content-type':'application/json'}
    r = requests.post(url, headers=headers, data=json.dumps(trade_list))
    return r