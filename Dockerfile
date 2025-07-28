# launcher/Dockerfile
FROM python:3.12-slim AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install uv
RUN pip install -r requirements.txt

COPY 02-install-docker.sh .
RUN ./02-install-docker.sh

FROM base AS runtime
COPY compose.yaml app.py app-2.py 02-install-docker.sh .

#CMD ["python", "launcher/launcher.py"]
CMD ["python", "-u", "app-2.py"]
