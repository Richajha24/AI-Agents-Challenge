# Documentation Generator Agent

## Overview

Documentation Generator automatically creates professional documentation from project descriptions.

The goal is to save developers hours of manual documentation work.

---

## Core Features

### README Generation

* Project Overview
* Features
* Installation
* Usage

### API Documentation

* Endpoint descriptions
* Request examples
* Response examples

### Architecture Notes

* Folder structure explanation
* Workflow description
* Technical summary

---

## Input

Project description.

Example:

Build an AI-powered internship finder.

---

## Output

* README.md
* API Documentation
* Architecture Summary
* Setup Instructions

---

## Tech Stack

* Python 3.12
* Groq API
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

## Verification

Generate documentation for at least one sample project.
