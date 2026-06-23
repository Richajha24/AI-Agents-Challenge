# Repo Explainer Agent

## Overview

Repo Explainer is an AI-powered command-line tool that analyzes GitHub repositories and explains them in simple language.

The goal is to help developers, recruiters, students, and founders quickly understand unfamiliar codebases.

---

## Core Features

### Repository Understanding

* Analyze GitHub repository URLs
* Detect project purpose
* Identify tech stack
* Explain architecture

### Codebase Insights

* Identify entry points
* Explain folder structure
* Highlight important files
* Detect frameworks and libraries

### Recommendations

* Improvement suggestions
* Maintainability observations
* Learning roadmap for beginners

---

## Input

GitHub repository URL

Example:

https://github.com/user/project

---

## Output

* Project Summary
* Tech Stack
* Architecture Overview
* Key Files
* Folder Structure Explanation
* Recommendations

---

## Tech Stack

* Python 3.12
* Groq API
* Requests
* Rich
* python-dotenv

CLI only.

No frontend.

No database.

---

## Deliverables

* main.py
* requirements.txt
* .env.example
* prompts/system_prompt.md
* README.md
* COMPLETION_REPORT.md

---

## Setup

1. Use Python 3.12.
2. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and set your Groq API key:

```bash
copy .env.example .env
```

## Usage

Run the CLI with a public GitHub repository URL:

```bash
python main.py https://github.com/psf/requests
```

Or run interactively:

```bash
python main.py
```

Optional environment variables:

* `GROQ_API_KEY` — required
* `GITHUB_TOKEN` — optional, increases GitHub API rate limits
* `GROQ_MODEL` — optional, defaults to `llama-3.3-70b-versatile`

## Verification

Analyze at least one public GitHub repository successfully.
