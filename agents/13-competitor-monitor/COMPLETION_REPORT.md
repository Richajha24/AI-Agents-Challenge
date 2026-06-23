# Completion Report — Agent 13 (Competitor Monitor)

## What was implemented
- `app.py`: CLI runner that loads the system prompt, parses competitors, calls Groq, and writes `competitor_report.md`.
- `groq_client.py`: Groq API wrapper (`generate()`), reading `GROQ_API_KEY` from `.env`.
- `competitor_parser.py`: Lightweight parser for competitor lists (supports `Name`, `Name | url`, `Name, url`).
- `prompts/system_prompt.md`: Filled-in system prompt with required output structure.
- `.env.example` and `requirements.txt`: Completed for runnable setup.

## How to run
From `agents/13-competitor-monitor`:

```bash
pip install -r requirements.txt
python app.py competitors.txt --output competitor_report.md
```

Or without a file:

```bash
python app.py
```

