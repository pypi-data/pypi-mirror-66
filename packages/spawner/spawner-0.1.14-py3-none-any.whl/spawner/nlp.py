import requests
import json
import pandas 


def answer(token, question): 
    url = "https://spawnerapi.com/answer/" + token
    trade_list = {"text": question}
    headers={'Content-type':'application/json'}
    r = requests.post(url, headers=headers, data=json.dumps(trade_list))
    return r.text

print(answer('sp_9707ef6621247144d05dd55f5fbb2ae8', 'what is the p/e ratio of apple?'))