# Sensor Data API

## Overview

This project is a simple API built with Python Flask and Redis. It receives JSON data (e.g., temperature and timestamp) via HTTP POST and stores it in a Redis database. There is also a test script that simulates sending sensor data to the API.

---

## Project Structure

- **api.py** — Flask API server that accepts data and saves it to Redis.
- **test.py** — Script that generates random temperature data and sends it to the API, then prints the response.

---

## Requirements

- Python 3.8 or higher
- Redis (running locally on port 6379)
- Python libraries:
  - Flask
  - redis
  - requests

---

## How to Run

1. Start Redis (for example, using Docker):
'docker run -p 6379:6379 redis'


2. Run the API server:
'python api.py'
The server will be accessible at `http://localhost:5000`

3. Run the test script to send sample data:
'python test.py'

---

## What the Project Does

- `api.py` listens for POST requests at `/data` and expects JSON data.
- It saves incoming data into a Redis list named `sensor_data`.
- `test.py` generates random temperature values with current timestamps and sends them to the API.
- It prints the HTTP response status and JSON response from the API.

---

## Example JSON Data Sent to the API

```json
{
"temperature": 25.43,
"timestamp": 1748272139.7082446
}
