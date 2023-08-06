import requests
import json
import pandas 

def correlation(token, list1, list2): 
    list1 = ",".join([str(item) for item in list1])
    list2 = ",".join([str(item) for item in list1])
    url = "https://spawnerapi.com/correlation/" + list1 + "/" + list2 + "/" + token
    response = requests.get(url).text
    return response

a = [1,2,3]
b = [4,5,6]
print(correlation('sp_9707ef6621247144d05dd55f5fbb2ae8', a, b))