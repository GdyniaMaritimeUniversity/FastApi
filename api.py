from flask import Flask, request, jsonify
import redis
import json
from datetime import datetime

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    data.setdefault('timestamp', datetime.utcnow().isoformat())

    r.rpush('sensor_data', json.dumps(data))

    return jsonify({"status": "ok", "data": data})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
