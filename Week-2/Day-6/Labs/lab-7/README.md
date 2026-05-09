# Lab 7: AI-Generated DataOps Portal

**Domain:** Manufacturing IoT

## Objective

Generate a **DataOps admin portal** with AI: pipeline monitoring, device-oriented metrics, and alerts.

## What you need

- Python 3.x, Streamlit  
- AI assistant (Claude Code, Copilot, Cursor)  

```bash
pip install streamlit pandas
```

*(Add other packages if your generated app needs them.)*

## Steps

### 1. Define requirements

The portal should reflect:

- Pipeline monitoring  
- Device metrics  
- Alert management  

### 2. Use an AI prompt

Example:

> Generate a Streamlit DataOps portal for IoT monitoring with: device metrics, pipeline health, alert management, and trend charts.

### 3. Generate the application

Use your AI tool to create `app.py` and any helper modules or sample data files.

### 4. Run the app

```bash
streamlit run app.py
```

### 5. Improve the UI

Add at least a few of:

- Sidebar filters  
- Search  
- KPI metrics at the top  

## Deliverables

- Runnable DataOps portal  
- Screenshots of main dashboard views  

## Learning outcomes

- Rapid portal generation with AI  
- Iterating on prototypes for operational tooling  

## Tips

- Use fake but realistic IoT device names and metric ranges for demos.  
- If charts are empty, ensure your sample dataframe is created before `st.line_chart`.  
