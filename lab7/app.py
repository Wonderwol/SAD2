import json
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Инициализация лимитера для приложения
limiter = Limiter(app)

# Словарь для хранения данных
data = {}

# Загрузка данных из файла при старте приложения
def load_data():
    global data
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

# Сохранение данных в файл после каждого изменения
def save_data():
    with open("data.json", "w") as file:
        json.dump(data, file)

# Инициализация данных при старте
load_data()

# Маршрут для сохранения ключ-значение
@app.route('/set', methods=['POST'])
@limiter.limit("10/minute", key_func=get_remote_address)  # Ограничение 10 запросов в минуту
def set_value():
    key = request.json.get('key')
    value = request.json.get('value')

    # Проверка на наличие обязательных данных
    if not key or value is None:
        return jsonify({"error": "Ключ и значение обязательны"}), 400

    data[key] = value
    save_data()
    return jsonify({"message": "Ключ-значение успешно сохранены"}), 200

# Маршрут для получения значения по ключу
@app.route('/get/<key>', methods=['GET'])
@limiter.limit("100/day", key_func=get_remote_address)  # Ограничение 100 запросов в сутки
def get_value(key):
    if key not in data:
        return jsonify({"error": "Ключ не найден"}), 404
    return jsonify({"key": key, "value": data[key]}), 200

# Маршрут для удаления ключа
@app.route('/delete/<key>', methods=['DELETE'])
@limiter.limit("10/minute", key_func=get_remote_address)  # Ограничение 10 запросов в минуту
def delete_key(key):
    if key not in data:
        return jsonify({"error": "Ключ не найден"}), 404

    del data[key]
    save_data()
    return jsonify({"message": "Ключ успешно удалён"}), 200

# Маршрут для проверки существования ключа
@app.route('/exists/<key>', methods=['GET'])
@limiter.limit("100/day", key_func=get_remote_address)  # Ограничение 100 запросов в сутки
def exists_key(key):
    exists = key in data
    return jsonify({"exists": exists}), 200
