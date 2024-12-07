import requests
import time

url = "http://127.0.0.1:5000/get/"

key = "name"

headers = {'Content-Type': 'application/json'}

for i in range(120):
    # Формируем полный URL с ключом
    full_url = url + key

    # Выполнение GET-запроса
    response = requests.get(full_url, headers=headers)

    # Проверяем, если ответ пустой или не является JSON
    if response.status_code == 200:
        try:
            response_json = response.json()
            print(f"Запрос {i+1}: {response.status_code} - {response_json}")
        except requests.exceptions.JSONDecodeError:
            print(f"""Запрос {i+1}: {response.status_code} -
                  Ошибка при декодировании JSON.""")
            break  # Прерываем цикл при ошибке декодирования JSON
    else:
        print(f"Запрос {i+1}: {response.status_code} - {response.text}")
        break  # Прерываем цикл, если статус код не 200

    time.sleep(0.1)
