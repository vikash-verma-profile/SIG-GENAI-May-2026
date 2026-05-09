# Lab 8: AI-Powered ETL Monitoring API

**Domain:** Airline Reservation System

## Objective

Create **monitoring APIs** for ETL jobs using **FastAPI**, with AI help for scaffolding and documentation.

## What you need

```bash
pip install fastapi uvicorn
```

## Steps

### 1. Create the project folder

```bash
mkdir airline-monitor-api
cd airline-monitor-api
```

### 2. Install packages

```bash
pip install fastapi uvicorn
```

### 3. Generate the API with AI

Prompt your assistant to build FastAPI endpoints for ETL monitoring, for example:

- Pipeline status (per job or list)  
- Failure alerts  
- SLA-related metrics (e.g. duration vs. threshold)  

Place the result in `main.py` (and extra modules if needed).

### 4. Run the API

```bash
uvicorn main:app --reload
```

### 5. Test with Swagger UI

Open `http://127.0.0.1:8000/docs` and exercise each endpoint.

## Deliverables

- ETL monitoring API (runnable locally)  
- Swagger/OpenAPI available at `/docs`  

## Learning outcomes

- AI-generated monitoring APIs  
- Practical FastAPI patterns for operational endpoints  

## Tips

- Return consistent JSON shapes (e.g. always `{"pipelines": [...]}`) so clients are easier to build.  
- Document assumptions about job IDs and timestamps in your README.  
