from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json

app = Flask(__name__)

limiter = Limiter(get_remote_address, app=app)

data = {}


def load_data():
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_data():
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


data = load_data()


@app.route('/set', methods=['POST'])
@limiter.limit("10 per minute")  # Лимит 10 запросов в минуту для /set
def set_key_value():
    content = request.get_json()
    key = content.get('key')
    value = content.get('value')

    if not key or not value:
        return jsonify({"message": "Both 'key' and 'value' are required"}), 400

    data[key] = value
    save_data()
    return jsonify({"message": "Ключ-значение успешно сохранены"}), 200


@app.route('/get/<key>', methods=['GET'])
@limiter.limit("100 per day")  # Лимит 100 запросов в сутки для /get
def get_value(key):
    if key in data:
        return jsonify({key: data[key]}), 200
    return jsonify({"message": "Key not found"}), 404


@app.route('/delete/<key>', methods=['DELETE'])
@limiter.limit("10 per minute")  # Лимит 10 запросов в минуту для /delete
def delete_key(key):
    if key in data:
        del data[key]
        save_data()
        return jsonify({"message": f"Key '{key}' deleted"}), 200
    return jsonify({"message": "Key not found"}), 404


@app.route('/exists/<key>', methods=['GET'])
@limiter.limit("100 per day")  # Лимит 100 запросов в сутки для /exists
def exists_key(key):
    if key in data:
        return jsonify({"exists": True}), 200
    return jsonify({"exists": False}), 200
