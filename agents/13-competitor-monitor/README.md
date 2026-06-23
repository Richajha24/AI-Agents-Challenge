# Agent 13 — Competitor Monitor

## Overview

Competitor Monitor is an AI-powered business intelligence agent that analyzes competitors, tracks market positioning, identifies strengths and weaknesses, and generates strategic insights.

The agent helps founders, product managers, marketers, and startup teams understand the competitive landscape and discover opportunities for differentiation.

---

## Features

### Competitor Analysis
- Analyze competitor products and services
- Evaluate positioning and market presence
- Identify strengths and weaknesses

### Market Comparison
- Compare multiple competitors
- Highlight differentiators
- Detect competitive advantages

### Opportunity Discovery
- Identify market gaps
- Suggest positioning opportunities
- Recommend strategic improvements

### Strategic Recommendations
- Growth opportunities
- Product enhancements
- Competitive response strategies

---

## Tech Stack

- Python 3.12
- Groq API
- Rich
- python-dotenv

---

## Project Structure

13-competitor-monitor/
├── prompts/
│ └── system_prompt.md
├── main.py
├── groq_client.py
├── competitor_parser.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── COMPLETION_REPORT.md

---

## Usage

python main.py

or

python main.py competitors.txt

---

## Output

- Competitor Analysis
- Strengths & Weaknesses
- Market Positioning
- Opportunity Areas
- Strategic Recommendations

Output is displayed in terminal and saved to:

competitor_report.md

---

## Future Improvements

- Live competitor tracking
- Web research integration
- Market trend correlation
- Competitive scorecards