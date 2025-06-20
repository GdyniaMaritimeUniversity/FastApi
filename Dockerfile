# Używamy oficjalnego obrazu Pythona
FROM python:3.11-slim


WORKDIR /app


COPY . /app


RUN pip install --no-cache-dir flask


EXPOSE 5000


CMD ["python", "api.py"]
