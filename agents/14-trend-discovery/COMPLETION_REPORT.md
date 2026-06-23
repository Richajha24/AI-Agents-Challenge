Agent 14 — Trend Discovery completed.

What was implemented:
- Streamlit UI (agents/14-trend-discovery/app.py)
- Groq client wrapper (agents/14-trend-discovery/groq_client.py)
- System prompt template (agents/14-trend-discovery/prompts/system_prompt.md)
- requirements.txt
- (Optional) .env.example usage described in README

How to run:
1) cd agents/14-trend-discovery
2) pip install -r requirements.txt
3) copy .env.example .env (add GROQ_API_KEY)
4) streamlit run app.py

Outputs:
- Saves generated markdown report to trend_report.md

