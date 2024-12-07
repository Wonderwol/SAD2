import requests
import time

# URL вашего Flask-приложения
url = "http://127.0.0.1:5000/set"

# Заголовки для указания, что это JSON
headers = {'Content-Type': 'application/json'}

# Данные, которые отправляются в POST-запросах
data = '{"key": "name", "value": "example"}'

# Отправка 20 запросов
for i in range(20):
    # Выполнение POST-запроса
    response = requests.post(url, headers=headers, data=data)

    # Выводим код ответа
    print(f"Запрос {i+1}: {response.status_code}")

    # Задержка в 0.1 секунды между запросами
    time.sleep(0.1)
