from flask import Flask, jsonify, request, render_template
import requests
import threading
import time

app = Flask(__name__)

# Список инстансов
instances = [
    {"url": "http://127.0.0.1:5001", "status": "unknown"},
    {"url": "http://127.0.0.1:5002", "status": "unknown"},
    {"url": "http://127.0.0.1:5003", "status": "unknown"}
]

# Индекс текущего инстанса для Round Robin
current_instance_index = 0


# Функция проверки состояния инстансов
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


# Алгоритм Round Robin
def get_instance_round_robin():
    global current_instance_index, instances
    healthy_instances = [i for i in instances if i['status'] == 'healthy']
    if not healthy_instances:
        return None
    instance = healthy_instances[current_instance_index % len(healthy_instances)]
    current_instance_index = (current_instance_index + 1) % len(healthy_instances)
    return instance


@app.route('/')
def index():
    # Возвращение HTML-шаблона с информацией об инстансах
    return render_template('index.html', instances=instances)


@app.route('/process', methods=['POST'])
def process_request():
    instance = get_instance_round_robin()
    if not instance:
        return jsonify({"error": "No healthy instances available"}), 503

    try:
        # Перенаправление запроса на выбранный инстанс
        response = requests.post(instance['url'], json=request.json, timeout=5)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({"error": "Failed to forward request"}), 500


@app.route('/add_instance', methods=['POST'])
def add_instance():
    ip = request.form.get('ip')
    port = request.form.get('port')
    if ip and port:
        instance_url = f"http://{ip}:{port}"
        if not any(instance['url'] == instance_url for instance in instances):
            instances.append({"url": instance_url, "status": "unknown"})
            return jsonify({"message": f"Instance {instance_url} added"}), 200
        else:
            return jsonify({"error": "Instance already exists"}), 400
    return jsonify({"error": "IP and port are required"}), 400


@app.route('/remove_instance', methods=['POST'])
def remove_instance():
    index = request.form.get('index')
    if index and index.isdigit():
        index = int(index)
        if 0 <= index < len(instances):
            removed_instance = instances.pop(index)
            return jsonify({"message": f"Instance {removed_instance['url']} removed"}), 200
        else:
            return jsonify({"error": "Invalid index"}), 400
    return jsonify({"error": "Index is required"}), 400


if __name__ == '__main__':
    # Запуск потока проверки состояния
    thread = threading.Thread(target=health_check)
    thread.daemon = True
    thread.start()

    app.run(port=5000)
