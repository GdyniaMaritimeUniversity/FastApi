import requests
import random
import time

data = {
  "timestamp": "2025-06-02T16:03:11.012345",
  "temperature": 52.8,
  "humidity": 93.5,
  "pressure": 1055.4,
  "mac_address": "00:16:3e:00:00:05",
  "alerts": [
    {
      "alert_name": "High Temperature",
      "description": "Temperature exceeded 50°C: 52.8°C"
    },
    {
      "alert_name": "High Humidity",
      "description": "Humidity exceeded 90%: 93.5%"
    },
    {
      "alert_name": "High Pressure",
      "description": "Pressure exceeded 1050 hPa: 1055.4 hPa"
    }
  ]
}
headers = {
    "Authorization": "Bearer 5R3661N"
}

res = requests.post("http://localhost:5000/api/data", json=data, headers=headers)

print("Status code:", res.status_code)
print("Response text:", res.text)


try:
    print("JSON:", res.json())
except Exception as e:
    print("Nie udało się sparsować JSON:", e)
