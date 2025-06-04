import redis
import psycopg2
import json
from datetime import datetime
from dotenv import load_dotenv
import os
import time
import uuid
import random

load_dotenv()

# Połączenie z Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Połączenie z bazą PostgreSQL / TimescaleDB
def connect_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode=os.getenv("DB_SSLMODE")
    )

def get_sensor_id_by_mac(conn, mac_address):
    with conn.cursor() as cursor:
        cursor.execute("SELECT sensor_id FROM sensor WHERE mac_address = %s", (mac_address,))
        result = cursor.fetchone()
        return result[0] if result else None

def create_random_sensor(conn, mac_address):
    sensor_id = str(uuid.uuid4())
    user_id = get_random_user_id(conn)

    name = f"Sensor-{mac_address[-5:].replace(':', '')}"
    location = random.choice(["Gdynia", "Gdańsk", "Sopot", "Warszawa"])
    sensor_type = random.choice(["temperature", "weather", "environment"])
    status = "active"
    created_at = datetime.utcnow()
    last_seen = created_at

    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO sensor (sensor_id, user_id, name, location, type, mac_address, status, created_at, last_seen)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            sensor_id, user_id, name, location, sensor_type, mac_address, status, created_at, last_seen
        ))
        conn.commit()
    print(f"➕ Utworzono nowy sensor: {name} ({mac_address})")
    return sensor_id

def get_random_user_id(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT user_id FROM users ORDER BY RANDOM() LIMIT 1")
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            raise Exception("Brak dostępnych użytkowników w tabeli users")

def insert_sensor_data(conn, sensor_id, data):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO sensor_data (sensor_id, date_time, temperature, humidity, pressure)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            sensor_id,
            datetime.fromisoformat(data["timestamp"]),
            data["temperature"],
            data["humidity"],
            data["pressure"]
        ))
        conn.commit()

def main():
    conn = connect_db()
    print("🟢 Daemon running. Waiting for sensor data from Redis...")

    while True:
        raw_data = r.lpop("sensor_data")
        if raw_data is None:
            time.sleep(1)
            continue

        try:
            data = json.loads(raw_data)
            mac = data.get("mac_address")

            if not mac:
                print("⚠️  Brak adresu MAC w danych. Pomijam.")
                continue

            sensor_id = get_sensor_id_by_mac(conn, mac)
            if not sensor_id:
                sensor_id = create_random_sensor(conn, mac)

            insert_sensor_data(conn, sensor_id, data)
            print(f"✅ Dodano dane do bazy dla sensora {mac}")

        except Exception as e:
            print(f"❌ Błąd przetwarzania danych: {e}")
            continue

if __name__ == "__main__":
    main()
