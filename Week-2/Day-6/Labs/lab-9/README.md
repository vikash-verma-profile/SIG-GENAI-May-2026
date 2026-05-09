# Lab 9: AI-Generated Dashboard with Claude Code

**Domain:** Smart City Analytics

## Objective

Use **Claude Code** (or equivalent AI coding agent) to build a **smart city operational dashboard** in Streamlit focused on traffic analytics.

## What you need

- Python 3.x, Streamlit  
- Claude Code (or similar agent in your environment)  

```bash
pip install streamlit pandas
```

## Steps

### 1. Create the prompt

Example:

> Create a Streamlit dashboard for smart city traffic analytics with: traffic KPI cards, sensor alerts, and congestion-style visualizations (e.g. heatmap or chart placeholders with sample data).

### 2. Generate the application

Use Claude Code to implement `app.py` and any data helpers. Use **sample data** if you do not have real feeds.

### 3. Run the dashboard

```bash
streamlit run app.py
```

### 4. Validate the output

Check:

- Layout hierarchy  
- Charts render without errors  
- Alerts or warnings are visible where intended  

### 5. Add enhancements

Add at least a few of:

- Search  
- Filters (time range, zone, etc.)  
- Export buttons (e.g. CSV download via Streamlit)  

## Deliverables

- Operational dashboard (running locally)  
- Source code  
- GitHub repository  

## Learning outcomes

- Agent-driven Streamlit development  
- Customizing AI-generated dashboards  

## Tips

- Keep sample data in `data/` or generated in code so reviewers can run one command.  
- If heatmaps need extra libraries, add them to `requirements.txt`.  
