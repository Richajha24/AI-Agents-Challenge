# Founder Copilot 
# Founder Copilot

## Vision

Founder Copilot is an autonomous AI startup advisor that helps founders validate ideas, research markets, analyze competitors, identify opportunities, generate MVP plans, and create execution roadmaps.

The goal is not to create another chatbot.

The goal is to create an AI system that behaves like an experienced startup advisor.

A user should be able to enter a startup idea and receive a complete startup analysis report within minutes.

---

# Problem

Most founders spend weeks performing:

* Market research
* Competitor analysis
* Customer discovery
* Feature prioritization
* Pricing strategy
* MVP planning

Founder Copilot automates these workflows.

---

# Core User Flow

User enters:

* Startup idea
* Problem statement
* Industry
* Optional website

Example:

"I want to build an AI platform that helps students find internships."

The system automatically performs:

1. Market analysis
2. Competitor research
3. Customer persona generation
4. SWOT analysis
5. MVP planning
6. Pricing suggestions
7. Go-to-market strategy
8. Execution roadmap

The final result should feel like a mini-consulting report.

---

# Core Features

## 1. Startup Idea Analysis

Inputs:

* Startup idea
* Industry

Outputs:

* Problem summary
* Opportunity assessment
* Market attractiveness score
* Risk assessment

---

## 2. Competitor Research Agent

Research competitors automatically.

Find:

* Direct competitors
* Indirect competitors
* Key features
* Pricing models
* Differentiation opportunities

Output:

Competitor comparison table.

---

## 3. Market Research Agent

Generate:

* TAM
* SAM
* SOM

Estimate:

* Market size
* Industry trends
* Growth opportunities

---

## 4. Customer Persona Agent

Generate:

* Primary users
* Pain points
* Buying motivations
* Behavioral patterns

Output:

Detailed personas.

---

## 5. MVP Planner

Generate:

* Core features
* Nice-to-have features
* Development priorities

Output:

MVP roadmap.

---

## 6. Pricing Strategy Agent

Suggest:

* Subscription models
* Freemium options
* Enterprise pricing

Output:

Recommended pricing structure.

---

## 7. Go-To-Market Agent

Generate:

* Launch strategy
* Acquisition channels
* Content strategy
* Distribution strategy

---

## 8. Execution Roadmap Agent

Generate:

30 Day Plan

60 Day Plan

90 Day Plan

6 Month Plan

1 Year Plan

---

# Technical Architecture

## Frontend

Next.js

TypeScript

TailwindCSS

ShadCN

---

## Backend

FastAPI

Python

---

## AI Layer

OpenAI

Claude

Gemini

Use provider abstraction so models can be swapped easily.

---

## Data Layer

PostgreSQL

---

## Optional

LangGraph

CrewAI

PydanticAI

Only if useful.

Avoid unnecessary complexity.

---

# UI Requirements

IMPORTANT:

Do NOT create another generic AI SaaS interface.

Avoid:

* Neon blue
* Neon purple
* Generic ChatGPT clones
* Cyberpunk gradients
* Glassmorphism everywhere

The product should look like a premium consulting platform.

---

# Design Direction

Theme:

"Modern Venture Capital Firm"

or

"Premium Strategy Consultancy"

Think:

* McKinsey
* Sequoia
* Andreessen Horowitz
* Notion

Not:

* Crypto dashboard
* AI chatbot clone

---

# Color Palette

Preferred:

* Deep forest green
* Warm ivory
* Dark graphite
* Muted gold accents
* Soft beige backgrounds

Alternative:

* Burgundy
* Cream
* Charcoal

Avoid:

* Neon colors
* Bright gradients
* RGB aesthetics

---

# Typography

Avoid:

* Inter
* Poppins
* Generic startup fonts

Use more distinctive premium fonts.

Suggestions:

Headings:

* Space Grotesk
* Sora
* Clash Display
* Cabinet Grotesk

Body:

* Manrope
* IBM Plex Sans
* Source Sans Pro

The interface should feel unique and memorable.

---

# Main Screens

## Landing Page

Sections:

* Hero
* Features
* Demo workflow
* Testimonials (mock)
* CTA

---

## Dashboard

Cards:

* Idea Analysis
* Market Research
* Competitors
* Pricing
* Roadmap

---

## Analysis Workspace

Displays:

* Progress indicators
* Agent execution logs
* Final reports

---

## Report Page

Professional report layout.

Export:

* PDF
* Markdown

---

# Deliverables

Version 1

Must include:

* Working frontend
* Working backend
* Idea analysis
* Competitor analysis
* MVP planner
* Report generation

Deploy publicly.

---

# Success Criteria

A founder should be able to:

1. Enter an idea
2. Wait 1-2 minutes
3. Receive a professional startup report

without manually researching anything.

The final experience should feel like receiving advice from a startup consultant rather than chatting with a generic AI assistant.
