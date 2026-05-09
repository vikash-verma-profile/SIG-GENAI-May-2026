# Lab 6: AI-Assisted Peer Review

**Domain:** Insurance Data Platform

## Objective

Practice **structured peer review** of AI-generated applications (layout, logic, security, and maintainability).

## What you need

- Git  
- Access to a peer’s repository URL (your instructor or team will provide `<repo-url>`)  
- GitHub (or similar) for pull requests  

## Steps

### 1. Clone the peer repository

```bash
git clone <repo-url>
cd <repo-folder>
```

Use the real URL your class provides.

### 2. Review the Streamlit (or assigned) app

Inspect:

- Dashboard layout and clarity  
- Code readability (names, structure, duplication)  
- KPI and metric logic (does it match the domain story?)  

### 3. Use a review checklist

Validate where relevant:

- **Security** — secrets, unsafe inputs, file paths  
- **Performance** — large data loads, unnecessary recomputation  
- **Testing** — any tests; edge cases  
- **Documentation** — README, how to run  

### 4. Write review comments

Be specific and constructive, for example:

> Add exception handling when `metadata.json` is missing or invalid.

### 5. Submit a pull request review

On GitHub: open or comment on the peer’s PR — **approve** or **request changes** with a short summary.

## Deliverables

- Written peer review comments (inline or summarized)  
- PR review summary (what you checked, main findings)  

## Learning outcomes

- Structured code review habits  
- Validation of AI-generated applications  

## Tips

- Separate “must fix” from “nice to have.”  
- Reference files and line numbers when commenting on GitHub.  
