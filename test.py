import requests
import random
import time

data = {
    "temperature": round(random.uniform(20.0, 30.0), 2),
    "timestamp": time.time()
}

res = requests.post("http://localhost:5000/data", json=data)

print("Status code:", res.status_code)
print("Response text:", res.text)

# tylko jeśli wiemy, że serwer zwraca JSON
try:
    print("JSON:", res.json())
except Exception as e:
    print("Nie udało się sparsować JSON:", e)
