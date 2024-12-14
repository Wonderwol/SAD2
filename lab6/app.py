from flask import Flask, jsonify, render_template
import threading
import time
import requests

app = Flask(__name__)

instance_id = None


@app.route('/health')
def health():
    return jsonify({"status": "healthy"})


@app.route('/process')
def process():
    return jsonify({"instance_id": instance_id})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/instance_list')
def instance_list():
    try:
        response = requests.get('http://127.0.0.1:5000/instance_list')
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Request to load balancer failed: {e}")
        return jsonify({"error": "Failed to fetch instance list"}), 500


def background_task():
    while True:
        try:
            health_response = requests.get(f'http://127.0.0.1:{5000 + int(instance_id)}/health', timeout=2)
            print(f"Health check response: {health_response.json()}")

            process_response = requests.get(f'http://127.0.0.1:{5000 + int(instance_id)}/process', timeout=2)
            print(f"Process response: {process_response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        time.sleep(5)


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        sys.exit(1)

    instance_id = sys.argv[1]

    thread = threading.Thread(target=background_task)
    thread.daemon = True
    thread.start()

    app.run(port=5000 + int(instance_id))
