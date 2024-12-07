import requests
import time

url = "http://127.0.0.1:5000/set"

headers = {'Content-Type': 'application/json'}

data = '{"key": "name", "value": "example"}'

for i in range(20):
    response = requests.post(url, headers=headers, data=data)

    print(f"Запрос {i+1}: {response.status_code}")

    time.sleep(0.1)
