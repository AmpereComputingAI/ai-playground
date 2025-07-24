# launcher/Dockerfile
FROM python:3.12-slim AS base

WORKDIR /app
RUN pip install uv
RUN uv pip install --system docker gradio

#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt

COPY 02-install-docker.sh .
RUN ./02-install-docker.sh

FROM base AS runtime
COPY app.py compose.yaml 02-install-docker.sh .

#CMD ["python", "launcher/launcher.py"]
CMD ["python", "-u", "app.py"]
