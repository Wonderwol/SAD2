from flask import Flask, jsonify, request, redirect, url_for
import requests
import threading
import time

app = Flask(__name__)

instances = []
current_instance_index = 0


def health_check():
    global instances
    while True:
        for instance in instances:
            try:
                response = requests.get(f"{instance['url']}/health", timeout=2)
                if response.status_code == 200:
                    instance['status'] = 'healthy'
                    print(f"Instance {instance['url']} is healthy")
                else:
                    instance['status'] = 'unhealthy'
                    print(f"Instance {instance['url']} is unhealthy")
            except requests.exceptions.RequestException as e:
                instance['status'] = 'unhealthy'
                print(f"Instance {instance['url']} is unhealthy: {e}")
        time.sleep(5)


@app.route('/')
def index():
    global current_instance_index
    if not instances:
        print("No instances available")
        return jsonify({"error": "No available instances"}), 503

    for _ in range(len(instances)):
        instance = instances[current_instance_index]
        current_instance_index = (current_instance_index + 1) % len(instances)
        if instance['status'] == 'healthy':
            return redirect(f"{instance['url']}")

    print("No healthy instances available")
    return jsonify({"error": "No healthy instances available"}), 503


@app.route('/health')
def health():
    return jsonify({"status": "healthy", "instances": instances})


@app.route('/instance_list')
def instance_list():
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
            print(f"Added instance: {instance['url']}")
        else:
            print(f"Instance {instance_url} already exists")
    return redirect(url_for('index'))


@app.route('/remove_instance', methods=['POST'])
def remove_instance():
    index = int(request.form['index'])
    if 0 <= index < len(instances):
        removed_instance = instances.pop(index)
        print(f"Removed instance: {removed_instance['url']}")
        return redirect(url_for('index'))
    else:
        return jsonify({"error": "Invalid index"}), 400


@app.route('/<path:path>', methods=['GET'])
def catch_all(path):
    global current_instance_index
    if not instances:
        print("No instances available")
        return jsonify({"error": "No available instances"}), 503

    for _ in range(len(instances)):
        instance = instances[current_instance_index]
        current_instance_index = (current_instance_index + 1) % len(instances)
        if instance['status'] == 'healthy':
            try:
                # Перенаправление без лишнего запроса
                return redirect(f"{instance['url']}/{path}")
            except requests.exceptions.RequestException as e:
                print(f"Request to {instance['url']}/{path} failed: {e}")
                continue

    print("No healthy instances available")
    return jsonify({"error": "No healthy instances available"}), 503


if __name__ == '__main__':
    instances.append({"url": "http://127.0.0.1:5001", "status": "unknown"})
    instances.append({"url": "http://127.0.0.1:5002", "status": "unknown"})
    instances.append({"url": "http://127.0.0.1:5003", "status": "unknown"})

    thread = threading.Thread(target=health_check)
    thread.daemon = True
    thread.start()

    app.run(port=5000)
