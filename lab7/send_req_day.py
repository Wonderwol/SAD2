import requests
import time

# URL вашего Flask-приложения
url = "http://127.0.0.1:5000/get/"

# Данные для ключа, который вы хотите получить
key = "name"

# Заголовки для указания, что это JSON (хотя для GET-запросов это не обязательно)
headers = {'Content-Type': 'application/json'}

# Отправка 120 GET-запросов для получения значения
for i in range(120):
    # Формируем полный URL с ключом
    full_url = url + key

    # Выполнение GET-запроса
    response = requests.get(full_url, headers=headers)

    # Проверяем, если ответ пустой или не является JSON
    if response.status_code == 200:
        try:
            response_json = response.json()  # пытаемся распарсить JSON
            print(f"Запрос {i+1}: {response.status_code} - {response_json}")
        except requests.exceptions.JSONDecodeError:
            print(f"Запрос {i+1}: {response.status_code} - Ошибка при декодировании JSON.")
    else:
        print(f"Запрос {i+1}: {response.status_code} - {response.text}")

    time.sleep(0.1)
