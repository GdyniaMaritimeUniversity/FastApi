from flask import Flask, request, jsonify
import redis
import json
from datetime import datetime

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

API_TOKEN = "5R3661N"

REQUIRED_FIELDS = {
    "temperature": float,
    "humidity": float,
    "pressure": float,
    "mac_address": str
}

def validate_alerts(alerts):
    if not isinstance(alerts, list):
        return False
    for alert in alerts:
        if not isinstance(alert, dict):
            return False
        if "alert_name" not in alert or "description" not in alert:
            return False
        if not isinstance(alert["alert_name"], str) or not isinstance(alert["description"], str):
            return False
    return True

@app.route('/api/data', methods=['POST'])
def receive_data():
    # --- WALIDACJA TOKENU ----
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    token = auth_header.split(" ")[1]
    if token != API_TOKEN:
        return jsonify({"error": "Invalid token"}), 403

    # --- WALIDACJA DANYCH ---
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
        if not isinstance(data[field], expected_type):
            return jsonify({"error": f"Invalid type for field '{field}'"}), 400

    if "alerts" in data:
        if not validate_alerts(data["alerts"]):
            return jsonify({"error": "Invalid alerts format"}), 400

    data.setdefault('timestamp', datetime.utcnow().isoformat())
    r.rpush('sensor_data', json.dumps(data))

    return jsonify({"status": "ok", "data": data})

@app.route('/api/data', methods=['GET'])
def get_last_data():
    # Pobierz ostatni element z listy Redis (indeks -1)
    raw_data = r.lindex('sensor_data', -1)
    
    if raw_data is None:
        return jsonify({"message": "No data available"}), 404

    data = json.loads(raw_data)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
