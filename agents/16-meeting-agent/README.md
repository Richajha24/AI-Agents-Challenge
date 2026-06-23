# Agent 16 — Meeting Agent

## Overview

Meeting Agent is an AI-powered assistant that generates agendas, meeting briefs, discussion points, action items, and summaries.

It helps teams conduct productive meetings and maintain clear documentation.

---

## Features

### Agenda Generation
- Meeting objectives
- Discussion topics
- Suggested structure

### Meeting Preparation
- Key talking points
- Risks and blockers
- Important questions

### Summary Generation
- Meeting notes
- Decisions made
- Action items

### Follow-up Support
- Next steps
- Responsibilities
- Deadlines

---

## Tech Stack

- Python 3.12
- Groq API
- Rich
- python-dotenv

---

## Project Structure

16-meeting-agent/
├── prompts/
│ └── system_prompt.md
├── main.py
├── groq_client.py
├── meeting_parser.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── COMPLETION_REPORT.md

---

## Usage

python main.py

or

python main.py meeting_context.txt

---

## Output

- Meeting Agenda
- Discussion Points
- Risks
- Action Items
- Follow-up Recommendations

Output saved as:

meeting_report.md

---

## Future Improvements

- Calendar integration
- Meeting transcript analysis
- Team collaboration features