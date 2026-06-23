# Code Reviewer Agent

## Overview

Code Reviewer Agent is an AI-powered command-line application that reviews source code and provides professional feedback similar to a senior software engineer.

The goal is to help developers identify bugs, improve code quality, reduce technical debt, and learn best practices automatically.

The agent should work with individual files or entire project folders.

---

# Objectives

* Review source code automatically.
* Detect bugs and potential runtime issues.
* Identify code smells and anti-patterns.
* Suggest improvements and refactoring opportunities.
* Generate quality scores and recommendations.
* Provide actionable feedback in a structured format.

---

# Core Features

## 1. File Review

Analyze a single file.

Example:

```bash
python main.py app.py
```

The agent should:

* Read the file
* Understand the code
* Generate a review report

---

## 2. Folder Review

Analyze an entire project folder.

Example:

```bash
python main.py ./src
```

The agent should:

* Scan source files
* Review important modules
* Generate project-wide recommendations

---

## 3. Bug Detection

Identify:

* Potential bugs
* Logic issues
* Runtime risks
* Missing validation
* Edge cases

---

## 4. Code Smell Detection

Detect:

* Duplicate code
* Long functions
* Large classes
* Dead code
* Poor naming conventions
* High complexity sections

---

## 5. Performance Analysis

Provide suggestions for:

* Faster execution
* Better memory usage
* Improved algorithms
* Reduced redundancy

---

## 6. Maintainability Analysis

Evaluate:

* Readability
* Maintainability
* Scalability
* Documentation quality

---

## 7. Refactoring Suggestions

Generate:

* Cleaner implementations
* Better structure
* Modularization opportunities
* Simplified logic

---

# Input

The agent should accept:

### Option 1

Single file path

Example:

```bash
python main.py app.py
```

### Option 2

Folder path

Example:

```bash
python main.py ./project
```

### Option 3

Paste source code directly

Example:

```bash
python main.py
```

Then allow the user to paste code manually.

---

# Output

The terminal report should contain:

## File Information

* File Name
* Language Detected
* Lines of Code

## Quality Scores

* Readability Score
* Maintainability Score
* Performance Score
* Overall Score

## Issues Found

For each issue:

* Severity
* Description
* Location (if available)
* Recommendation

## Improvement Suggestions

* Refactoring Opportunities
* Best Practices
* Optimization Ideas

## Final Summary

* Strengths
* Weaknesses
* Recommended Next Steps

---

# Technical Requirements

## Language

Python 3.12

---

## AI Model

Groq API

Recommended model:

```text
llama-3.3-70b-versatile
```

---

## Libraries

```text
groq
rich
python-dotenv
pathlib
```

Optional:

```text
pydantic
```

---

# Architecture

The project should follow the same structure used by Agent 06 Repo Explainer.

```text
07-code-reviewer/
│
├── prompts/
│   └── system_prompt.md
│
├── main.py
├── groq_client.py
├── code_analyzer.py
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── COMPLETION_REPORT.md
```

---

# Environment Variables

Create:

```env
GROQ_API_KEY=your_api_key_here
MODEL_NAME=llama-3.3-70b-versatile
```

---

# Error Handling

The application must gracefully handle:

* Invalid file paths
* Empty files
* Unsupported file types
* Missing API key
* API failures
* Network errors

Display helpful terminal messages instead of crashing.

---

# CLI Experience

Use Rich for:

* Headers
* Progress indicators
* Tables
* Highlighted warnings
* Final report formatting

The application should feel professional and easy to use.

---

# Deliverables

Required files:

* main.py
* groq_client.py
* code_analyzer.py
* requirements.txt
* .env.example
* prompts/system_prompt.md
* README.md
* COMPLETION_REPORT.md

---

# Verification Requirements

The agent must:

1. Install dependencies successfully.
2. Run without errors.
3. Review at least one Python file.
4. Generate a structured review report.
5. Handle missing API keys gracefully.
6. Generate COMPLETION_REPORT.md.

---

# Success Criteria

The project is considered complete when:

* A user can provide a file or folder path.
* The code is analyzed successfully.
* A structured review is generated.
* Verification passes.
* COMPLETION_REPORT.md is created.

No frontend, database, authentication, deployment, or web interface should be added.

The goal is a working and verified CLI Code Reviewer Agent.
