# Agent 19 — Sales Agent (Streamlit)

## Overview
AI-powered sales assistant and outreach generator.

## Features
- Generate B2B outreach content in markdown:
  - Cold Email
  - LinkedIn Message
  - Follow-up Email
  - Sales Pitch Script
- Rich personalization using: Product/Service, Target Customer, Pain Point, Outreach Type, Tone.

## Tech Stack
- Python 3.12
- Streamlit
- Groq API
- python-dotenv

## Setup
```bat
cd agents\19-sales-agent
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Add your `GROQ_API_KEY` to `.env`.

## Run
```bat
streamlit run app.py
```

Open the shown local URL in your browser.

## Output
- The generated content is shown as markdown in the UI.
- A download button saves it as `Sales_generated.md`.

