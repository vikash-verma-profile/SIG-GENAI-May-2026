# tracking-service

Minimal package tracking microservice used for **Lab 4** documentation generation.

## Quickstart

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## API

- `GET /health`
- `POST /tracking`
- `GET /tracking/<tracking_id>`

## Docker

```bash
docker build -t tracking-service:latest .
docker run -p 8000:8000 tracking-service:latest
```

## Kubernetes

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

