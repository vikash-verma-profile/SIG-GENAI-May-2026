# Lab 2: FastAPI Metadata Service

**Domain:** Banking Operations

## Objective

Use AI to scaffold a **FastAPI** application that exposes **pipeline metadata** APIs, with automatic **OpenAPI / Swagger** documentation.

## Architecture

```
Metadata Store → FastAPI → Swagger UI
```

*(You can start with in-memory Python data or a JSON file; extend later to a real store.)*

## What you need

- Python 3.x  
- FastAPI, Uvicorn  
- VS Code or Cursor  
- AI assistant (e.g. Claude Code)  

Install:

```bash
pip install fastapi uvicorn
```

## Steps

### 1. Create the project

```bash
mkdir banking-api
cd banking-api
```

### 2. Use an AI prompt

Ask your assistant to generate a FastAPI app for pipeline metadata. Include:

- `GET /pipelines` — list or retrieve pipeline metadata  
- `GET /health` — health check  
- `POST /alerts` — create or record an alert (define a sensible request body)  
- Automatic Swagger / OpenAPI docs  

### 3. Create `main.py` (starter)

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "healthy"}
```

Expand this with your AI-generated endpoints and models.

### 4. Run the API

```bash
uvicorn main:app --reload
```

### 5. Open Swagger UI

In the browser:

`http://127.0.0.1:8000/docs`

Try each endpoint from the interactive docs.

## Deliverables

- Runnable FastAPI application  
- Working Swagger documentation  
- GitHub repository with clear README  

## Learning outcomes

- FastAPI project structure  
- AI-generated API scaffolding  
- Using Swagger for API exploration  

## Tips

- Use Pydantic models for request/response bodies so `/docs` stays accurate.  
- Keep sample data in a module or JSON file for easy resets during demos.  
