FROM python:3.10

WORKDIR /app

ENV PYTHONUNBUFFERED=1
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY service service

ENV SERVICE_HOST 0.0.0.0
ENV SERVICE_PORT 5000
ENV PYTHONPATH /app

WORKDIR /app/service

CMD uvicorn server:app --host $SERVICE_HOST --port $SERVICE_PORT
