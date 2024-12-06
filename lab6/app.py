from flask import Flask, request, jsonify, render_template, redirect, url_for
import threading
import time
import requests

app = Flask(__name__)

# Глобальные переменные
instances = [{"ip": "127.0.0.1", "port": 5001},
             {"ip": "127.0.0.1", "port": 5002},
             {"ip": "127.0.0.1", "port": 5003}]
inactive_instances = []
current_index = 0
lock = threading.Lock()


# Фоновая проверка здоровья
def health_check():
    while True:
        with lock:
            for instance in instances[:]:
                try:
                    url = f"http://{instance['ip']}:{instance['port']}/health"
                    requests.get(url, timeout=2)
                except requests.RequestException:
                    instances.remove(instance)
                    inactive_instances.append(instance)

            for instance in inactive_instances[:]:
                try:
                    url = f"http://{instance['ip']}:{instance['port']}/health"
                    requests.get(url, timeout=2)
                    inactive_instances.remove(instance)
                    instances.append(instance)
                except requests.RequestException:
                    pass
        time.sleep(5)


# Round Robin обработка запросов
@app.route("/process", methods=["GET", "POST"])
def process():
    global current_index
    with lock:
        if not instances:
            return jsonify({"error": "No active instances"}), 503
        instance = instances[current_index]
        current_index = (current_index + 1) % len(instances)

    try:
        # Обработка запроса к инстансу с корректным URL
        url = f"http://{instance['ip']}:{instance['port']}{request.full_path}"
        response = requests.request(
            method=request.method,
            url=url,
            headers=request.headers,
            data=request.get_data()
        )
        return response.text, response.status_code, response.headers.items()
    except requests.RequestException:
        return jsonify({"error": "Failed to connect to instance"}), 500


# Проверка состояния инстансов
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"active": instances, "inactive": inactive_instances})


# Добавление инстанса
@app.route("/add_instance", methods=["POST"])
def add_instance():
    data = request.json
    ip, port = data.get("ip"), data.get("port")
    if ip and port:
        instance = {"ip": ip, "port": int(port)}
        with lock:
            if instance not in instances and \
               instance not in inactive_instances:
                instances.append(instance)
                return jsonify({"message": "Instance added"}), 201
    return jsonify({"error": "Invalid instance data"}), 400


# Удаление инстанса по индексу
@app.route("/remove_instance/<int:index>", methods=["POST"])
def remove_instance(index):
    with lock:
        if 0 <= index < len(instances):
            instances.pop(index)
            return redirect(url_for("index"))
    return jsonify({"error": "Index out of range"}), 404


# Web UI для управления пулом
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ip = request.form.get("ip")
        port = request.form.get("port")
        if ip and port:
            instance = {"ip": ip, "port": int(port)}
            with lock:
                if instance not in instances and instance not in inactive_instances:
                    instances.append(instance)
        return redirect(url_for("index"))

    with lock:
        return render_template("index.html",
                               active_instances=instances,
                               inactive_instances=inactive_instances)


# Универсальный маршрут
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def forward(path):
    return process()


# Фоновая проверка здоровья
threading.Thread(target=health_check, daemon=True).start()


app.run(host="0.0.0.0", port=8000)
