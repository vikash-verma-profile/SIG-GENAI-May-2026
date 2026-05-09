# Lab 10: AI Coding Risk Analysis

**Domain:** Financial Services

## Objective

**Evaluate risks** in AI-generated code: security, validation, and design—then **document findings** and **improve** the application.

## What you need

- AI assistant to generate an initial app  
- Editor / reviewer mindset  
- Optional: peer for discussion  

## Steps

### 1. Generate a banking-style API or app

Use a prompt such as:

> Generate a small FastAPI or Flask banking demo API with accounts and transfers (use fake data only).

**Important:** Use **synthetic** data only; never real credentials or customer information.

Alternatively, run the provided intentional-review starter: `pip install -r requirements.txt` then `uvicorn starter_before_review:app --reload` and review **`starter_before_review.py`** (look for `LAB_ISSUE` comments).

### 2. Review the generated code

Look for:

- Security flaws (injection, unsafe deserialization, path traversal)  
- Hardcoded secrets or API keys  
- SQL injection if raw SQL is used  
- Missing authentication / authorization for sensitive operations  

### 3. Perform a structured review

Also consider:

- Architecture (separation of concerns)  
- Input validation  
- Scalability (blocking calls, unbounded loops)  

### 4. Document findings

Create a short **risk report** with:

- Issue description  
- Severity (e.g. high / medium / low)  
- Suggested fix  

### 5. Refactor the application

Apply:

- Security fixes  
- Clearer structure where needed  
- Validation logic (e.g. Pydantic models, amount bounds)  

## Deliverables

- Security / risk review report  
- Improved application (second iteration)  
- Peer review notes if your class requires exchange  

## Learning outcomes

- Awareness of AI-generated code risks  
- Secure coding habits  
- Critical judgment when shipping AI-assisted software  

## Tips

- Treat AI output as **untrusted** until reviewed.  
- For demos, use environment variables for any configurable secrets, never literals in code.  
