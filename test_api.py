import requests

print(requests.get('http://127.0.0.1:8000/fertility?files='+
                   'C:/Users/mym/Projects/python/fertility_count/sample.txt').json())
