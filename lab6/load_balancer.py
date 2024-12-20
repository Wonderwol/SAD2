from flask import Flask, jsonify, request, render_template
import requests
import threading
import time

app = Flask(__name__)

# Изначальные инстансы
instances = [
    {"url": "http://127.0.0.1:5001", "status": "unknown"},
    {"url": "http://127.0.0.1:5002", "status": "unknown"},
    {"url": "http://127.0.0.1:5003", "status": "unknown"}
]

current_instance_index = 0


# Проверка состояния инстансов
def health_check():
    global instances
    while True:
        for instance in instances:
            try:
                response = requests.get(f"{instance['url']}/health", timeout=2)
                if response.status_code == 200:
                    instance['status'] = 'healthy'
                else:
                    instance['status'] = 'unhealthy'
            except requests.exceptions.RequestException:
                instance['status'] = 'unhealthy'
        time.sleep(5)


@app.route('/')
def index():
    print("Главная страница загружена")  # Для отладки
    return render_template('index.html', instances=instances)


@app.route('/health')
def health():
    print("Проверка состояния здоровья")  # Для отладки
    return jsonify({"status": "healthy", "instances": instances})


@app.route('/instance_list')
def instance_list():
    print("Запрашивается список инстансов")  # Для отладки
    return jsonify({"instances": instances})


@app.route('/add_instance', methods=['POST'])
def add_instance():
    ip = request.form['ip']
    port = request.form['port']
    if ip and port:
        instance_url = f"http://{ip}:{port}"
        if not any(instance['url'] == instance_url for instance in instances):
            instance = {"url": instance_url, "status": "unknown"}
            instances.append(instance)
            print(f"Добавлен новый инстанс: {instance_url}")
    return jsonify({"message": "Instance added"}), 200


@app.route('/remove_instance', methods=['POST'])
def remove_instance():
    index = int(request.form['index'])
    if 0 <= index < len(instances):
        removed_instance = instances.pop(index)
        print(f"Удален инстанс: {removed_instance['url']}")
        return jsonify({"message": "Instance removed"}), 200
    return jsonify({"error": "Invalid index"}), 400


if __name__ == '__main__':
    # Стартуем поток проверки состояния
    thread = threading.Thread(target=health_check)
    thread.daemon = True
    thread.start()

    app.run(port=5000)
