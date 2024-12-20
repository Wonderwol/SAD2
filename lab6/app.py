from flask import Flask, jsonify
import sys

app = Flask(__name__)

instance_id = None


@app.route('/health')
def health():
    return jsonify({"status": "healthy"})


@app.route('/process')
def process():
    return jsonify({"instance_id": instance_id})


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)

    instance_id = sys.argv[1]

    app.run(port=5000 + int(instance_id))
