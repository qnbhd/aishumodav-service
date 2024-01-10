FROM python:3.10

WORKDIR /app

RUN apt update && apt install -y ffmpeg

ENV PYTHONUNBUFFERED=1
COPY requirements.txt requirements.txt
COPY requirements-torch.txt requirements-torch.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-torch.txt
COPY service service
COPY config.yaml config.yaml

ENV SERVICE_HOST 0.0.0.0
ENV SERVICE_PORT 5000
ENV PYTHONPATH /app

WORKDIR /app/service

CMD uvicorn server:app --host $SERVICE_HOST --port $SERVICE_PORT
