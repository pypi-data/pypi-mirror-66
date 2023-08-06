import requests
import json
import pandas as pd

# return answer as dataframe 
def answer(question): 
    try: 
        url = "https://spawnerapi.com/answer"
        trade_list = {"text": question}
        headers={'Content-type':'application/json'}
        r = requests.post(url, headers=headers, data=json.dumps(trade_list))
        content = r.text
        df = pd.read_json(content, orient='records')
        df = df.drop(columns=['chart_type', 'condensed_data', 'data'])
        return df
    except: 
        return 'I am not smart enough to answer that question. Try again.'