# launcher/Dockerfile
FROM python:3.12-slim AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install uv
RUN pip install -r requirements.txt

COPY install-docker.sh .
RUN ./install-docker.sh

FROM base AS runtime
COPY app.py compose.yaml .env .
COPY ./static ./static
COPY ./searxng ./searxng

#CMD ["python", "launcher/launcher.py"]
CMD ["python", "-u", "app.py"]
