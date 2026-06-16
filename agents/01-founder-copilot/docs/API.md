# Founder Copilot - API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

Currently no authentication. Add JWT auth in production.

## Endpoints

### 1. Create Analysis

**POST** `/api/v1/analyze`

Start a new startup analysis.

#### Request

```json
{
  "startup_idea": "AI platform that helps students find internships",
  "industry": "EdTech",
  "problem_statement": "Students struggle to find relevant internship opportunities that match their skills and interests",
  "website_url": "https://example.com" // optional
}
```

#### Response (200)

```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Analysis started. Check status for updates."
}
```

---

### 2. Get Analysis Status

**GET** `/api/v1/analysis/{analysis_id}`

Get current status and progress of an analysis.

#### Response (200)

```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "in_progress",
  "progress": 45,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:32:00Z"
}
```

#### Status Values

- `pending` - Waiting to start
- `in_progress` - Currently analyzing
- `completed` - Analysis finished successfully
- `failed` - Analysis failed

#### Progress

Progress is a percentage 0-100 indicating which agents have completed.

---

### 3. Get Analysis Report

**GET** `/api/v1/report/{analysis_id}`

Get completed analysis report with all results.

#### Response (200)

```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 100,
  "startup_idea": "AI platform that helps students find internships",
  "industry": "EdTech",
  "created_at": "2024-01-15T10:30:00Z",
  "completed_at": "2024-01-15T10:35:00Z",
  
  "idea_analysis": {
    "problem_summary": "...",
    "opportunity_assessment": "...",
    "market_attractiveness_score": 85,
    "risk_assessment": "...",
    "key_insights": [...]
  },
  
  "competitor_analysis": {
    "direct_competitors": [...],
    "indirect_competitors": [...],
    "comparison_table": {...},
    "differentiation_opportunities": [...]
  },
  
  "market_research": {
    "tam": "$50 billion",
    "sam": "$5 billion",
    "som": "$50 million",
    "market_size_estimate": "...",
    "industry_trends": [...],
    "growth_opportunities": [...]
  },
  
  "customer_personas": {
    "personas": [...],
    "primary_pain_points": [...],
    "buying_motivations": [...],
    "behavioral_patterns": [...]
  },
  
  "mvp_plan": {
    "core_features": [...],
    "nice_to_have_features": [...],
    "development_priorities": [...],
    "estimated_timeline": "8-10 weeks"
  },
  
  "pricing_strategy": {
    "subscription_models": [...],
    "freemium_option": {...},
    "enterprise_pricing": {...},
    "recommended_pricing": "..."
  },
  
  "go_to_market": {
    "launch_strategy": "...",
    "acquisition_channels": [...],
    "content_strategy": [...],
    "distribution_strategy": "..."
  },
  
  "execution_roadmap": {
    "thirty_day_plan": {...},
    "sixty_day_plan": {...},
    "ninety_day_plan": {...},
    "six_month_plan": {...},
    "one_year_plan": {...}
  }
}
```

#### Errors

- `404` - Analysis not found
- `400` - Analysis not completed yet

---

### 4. Get Analysis History

**GET** `/api/v1/history`

Get user's previous analyses.

#### Query Parameters

- `limit` (optional, default: 20) - Number of results to return

#### Response (200)

```json
[
  {
    "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
    "startup_idea": "AI platform that helps students find internships",
    "industry": "EdTech",
    "status": "completed",
    "created_at": "2024-01-15T10:30:00Z",
    "completed_at": "2024-01-15T10:35:00Z"
  },
  {
    "analysis_id": "660e8400-e29b-41d4-a716-446655440001",
    "startup_idea": "Fintech lending platform",
    "industry": "FinTech",
    "status": "in_progress",
    "created_at": "2024-01-15T11:00:00Z",
    "completed_at": null
  }
]
```

---

### 5. Health Check

**GET** `/health`

Check API health status.

#### Response (200)

```json
{
  "status": "healthy",
  "service": "founder-copilot-api"
}
```

---

## Error Responses

### Standard Error Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Errors

| Status | Error | Reason |
|--------|-------|--------|
| 400 | `Analysis not completed. Current status: in_progress` | Report requested before analysis finished |
| 404 | `Analysis not found` | Invalid analysis_id |
| 500 | `Server error` | Backend error |

---

## Example Usage

### Workflow

```bash
# 1. Create analysis
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "startup_idea": "AI platform for code review",
    "industry": "SaaS",
    "problem_statement": "Developers waste time on manual code reviews"
  }'

# Returns: {"analysis_id": "550e8400..."}

# 2. Poll status
curl http://localhost:8000/api/v1/analysis/550e8400...

# Returns: {"status": "in_progress", "progress": 45}

# 3. Once completed, get report
curl http://localhost:8000/api/v1/report/550e8400...

# Returns: Full analysis report
```

---

## Rate Limiting

Not implemented in v1. Add in production.

---

## Future Enhancements

- WebSocket for real-time progress updates
- Batch analysis endpoint
- Export formats (PDF, Word, Markdown)
- Custom agent configurations
- Comparison between multiple analyses
