# FROM python:3.10-slim

# WORKDIR /app

# COPY . /app

# RUN pip install --no-cache-dir -r requirements.txt

# CMD ["python", "run.py"]

FROM python:3.9

WORKDIR /app

COPY . .

# ✅ Set the path to your GCP service account JSON key
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/smart-pride-456601-t3-9225d179d815.json

RUN pip install -r requirements.txt

CMD ["python", "test_app.py"]