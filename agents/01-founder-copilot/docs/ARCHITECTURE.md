# Founder Copilot - System Architecture

## Overview

Founder Copilot is an autonomous AI startup advisor that performs comprehensive startup analysis in minutes. The system consists of:

- **Frontend**: Next.js 14 SPA with premium UI
- **Backend**: FastAPI with async agents
- **AI Layer**: Provider abstraction (OpenAI, Claude, Gemini)
- **Database**: PostgreSQL for persistence

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                       │
│  Landing → Dashboard → Analysis Form → Workspace → Report   │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────┴──────────────┐
         │                          │
         ▼                          ▼
    API Routes              WebSocket Status
    POST /analyze           GET /analysis/{id}
    GET /report/{id}        GET /history
    GET /analysis/{id}
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend (FastAPI)                         │
├──────────────────────────────────────────────────────────────┤
│  API Layer: routes.py                                        │
│  Orchestrator: orchestrator.py                               │
│  Agents Pipeline:                                            │
│    1. Idea Analysis Agent                                    │
│    2. Competitor Research Agent                              │
│    3. Market Research Agent                                  │
│    4. Customer Persona Agent                                 │
│    5. MVP Planner Agent                                      │
│    6. Pricing Strategy Agent                                 │
│    7. Go-To-Market Agent                                     │
│    8. Execution Roadmap Agent                                │
├──────────────────────────────────────────────────────────────┤
│  AI Layer (Provider Abstraction):                            │
│    - OpenAI Provider (GPT-4)                                 │
│    - Claude Provider (Claude 3 Sonnet)                       │
│    - Gemini Provider (Gemini Pro)                            │
├──────────────────────────────────────────────────────────────┤
│  Data Layer (SQLAlchemy ORM):                                │
│    - Analysis Model                                          │
│    - Report Model                                            │
└──────────────┬───────────────────────────────────────────────┘
               │
               ▼
        ┌─────────────────┐
        │   PostgreSQL    │
        │  (Persistence)  │
        └─────────────────┘
```

## Agent Architecture

Each agent follows the same pattern:

```
Input (startup_idea, industry, problem_statement, website_url)
        ↓
[Agent Prompt Template]
        ↓
[AI Provider (OpenAI/Claude/Gemini)]
        ↓
[JSON Parse Output]
        ↓
Output (structured result)
        ↓
[Database Store]
```

## Data Flow

### 1. User Initiates Analysis

```
User fills form on /analysis/new
         ↓
POST /api/v1/analyze
         ↓
Create Analysis record (status: pending)
         ↓
Return analysis_id to user
         ↓
Redirect to /analysis/{id}
```

### 2. Background Analysis Execution

```
Orchestrator receives analysis_id
         ↓
Update status: in_progress
         ↓
Execute Agents (Sequential with progress updates):
  - Idea Analysis (0-12%)
  - Competitor Research (12-25%)
  - Market Research (25-37%)
  - Customer Personas (37-50%)
  - MVP Planner (50-62%)
  - Pricing Strategy (62-75%)
  - Go-To-Market (75-87%)
  - Execution Roadmap (87-100%)
         ↓
Store all results in database
         ↓
Update status: completed
```

### 3. User Views Report

```
Frontend polls: GET /api/v1/analysis/{id}
         ↓
While status != completed: show progress
         ↓
When completed: GET /api/v1/report/{id}
         ↓
Display full report
         ↓
User can export to PDF
```

## API Endpoints

### Analysis Management

- `POST /api/v1/analyze` - Start new analysis
  - Request: `{startup_idea, industry, problem_statement, website_url?}`
  - Response: `{analysis_id, status, message}`

- `GET /api/v1/analysis/{id}` - Get analysis status
  - Response: `{analysis_id, status, progress, created_at, updated_at}`

- `GET /api/v1/report/{id}` - Get completed report
  - Response: Full analysis results (all agent outputs)

- `GET /api/v1/history` - Get user's analysis history
  - Query: `?limit=20`
  - Response: Array of analyses

## Database Schema

### Analysis Table

```sql
CREATE TABLE analyses (
    id UUID PRIMARY KEY,
    user_id VARCHAR,
    startup_idea VARCHAR NOT NULL,
    industry VARCHAR NOT NULL,
    problem_statement TEXT NOT NULL,
    website_url VARCHAR,
    
    -- Agent Results (JSON)
    idea_analysis JSONB,
    competitor_analysis JSONB,
    market_research JSONB,
    customer_personas JSONB,
    mvp_plan JSONB,
    pricing_strategy JSONB,
    go_to_market JSONB,
    execution_roadmap JSONB,
    
    -- Status
    status VARCHAR (pending, in_progress, completed, failed),
    progress INTEGER,
    error_message TEXT,
    
    -- Timestamps
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    completed_at TIMESTAMP
);
```

## Provider Abstraction

The system supports swapping between AI providers without code changes:

```python
# Get provider based on config
provider = get_provider(
    provider_name="openai",  # or "claude", "gemini"
    api_key="xxx"
)

# Use same interface regardless of provider
result = await provider.generate(prompt)
json_result = await provider.generate_json(prompt, schema)
```

## Performance Considerations

1. **Async Processing**: Backend uses async/await for non-blocking agent execution
2. **Background Tasks**: Analysis runs as background job, doesn't block API
3. **Progress Updates**: Frontend polls status endpoint (can be WebSocket in future)
4. **Caching**: Results cached in database for instant retrieval
5. **Parallel Agents**: Some agents could run in parallel (future optimization)

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Load Balancer                          │
└────────────┬──────────────────────┬────────────────────────┘
             │                      │
      ┌──────▼─────┐         ┌──────▼─────┐
      │  Frontend   │         │  Backend   │
      │  Vercel     │         │  Heroku    │
      └──────┬─────┘         └──────┬─────┘
             │                      │
             └──────────────┬───────┘
                            │
                    ┌───────▼────────┐
                    │   PostgreSQL   │
                    │   (Managed)    │
                    └────────────────┘
```

## Scalability

- Frontend: Serverless via Vercel (auto-scaling)
- Backend: Containerized FastAPI (Docker)
- Database: Managed PostgreSQL with read replicas
- AI Calls: Queued with rate limiting
- Cache: Redis for session/analysis metadata (future)
