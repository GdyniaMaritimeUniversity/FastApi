# Sensor Data API

## Overview

 This project is a Python-based system for collecting, storing, and processing sensor data. It includes:

- A Flask API that receives JSON sensor data and stores it in Redis.

- A daemon script that processes data from Redis and inserts it into a PostgreSQL/TimescaleDB.

- A test script that simulates sensor data transmission.
---

## Project Structure

- **api.py** — Flask API server that accepts data and saves it to Redis.
- **daemon.py** — Continuously reads Redis data, validates sensors (by MAC address), and saves them to PostgreSQL.
- **test.py** — Script that generates random temperature data and sends it to the API, then prints the response.

---

## Requirements

- Python 3.8 or higher
- Redis (running locally on port 6379)
- Python libraries:
  - Flask
  - redis
  - requests
  - psycopg2
  - python-dotenv

```bash
pip install -r requirements.txt
```
---

## How to Run

1. Start Redis (for example, using Docker):
```bash
docker run -p 6379:6379 redis
```
2. PostgreSQL/TimescaleDB: Ensure your database is up and running and the following tables exist:
```bash
CREATE TABLE sensor (
  sensor_id UUID PRIMARY KEY,
  user_id UUID,
  name TEXT,
  location TEXT,
  type TEXT,
  mac_address TEXT,
  status TEXT,
  created_at TIMESTAMP,
  last_seen TIMESTAMP
);

CREATE TABLE sensor_data (
  sensor_id UUID,
  date_time TIMESTAMP,
  temperature REAL,
  humidity REAL,
  pressure REAL
);
```
3. Create .env file in the project root:
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db_name
DB_USER=your_user
DB_PASSWORD=your_password
DB_SSLMODE=prefer

4. Run the API server:
```bash
'python api.py'
The server will be accessible at `http://localhost:5000`
```
5. Start the daemon:
```bash
py daemon.py
```
6. Run the test script to send sample data:
'python test.py'

---

## What the Project Does

- `api.py` listens for POST requests at `/data` and expects JSON data.
- It saves incoming data into a Redis list named `sensor_data`.
- `test.py` generates random temperature values with current timestamps and sends them to the API.
- It prints the HTTP response status and JSON response from the API.
- `daemon.py` reads data from Redis, verifies if the sensor exists in the DB (using MAC address), creates one if needed, then inserts the data into the sensor_data table.
---

## Example JSON Data Sent to the API

```json
{
  "temperature": 23.5,
  "humidity": 60.2,
  "pressure": 1012.3,
  "mac_address": "AA:BB:CC:DD:EE:FF",
  "alerts": [
    {
      "alert_name": "Overheat",
      "description": "Temperature exceeded safe limit"
    }
  ]
}