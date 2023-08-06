import requests
import json
import pandas 

def correlation(token, list1, list2): 
    list1 = ",".join([str(item) for item in list1])
    list2 = ",".join([str(item) for item in list1])
    url = "https://spawnerapi.com/correlation/" + list1 + "/" + list2 + "/" + token
    response = requests.get(url).text
    return response
