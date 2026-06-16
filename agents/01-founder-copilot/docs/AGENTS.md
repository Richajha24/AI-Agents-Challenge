# Founder Copilot - Agent Specifications

## Agent Design Pattern

All agents follow the same execution pattern:

```
Input Parameters → Prompt Template → AI Provider → JSON Output → Validation → Storage
```

## Agent Details

### 1. Idea Analysis Agent

**Purpose**: Validate startup idea and assess market opportunity

**Inputs**:
- `startup_idea`: Core idea/product concept
- `industry`: Market/industry focus
- `problem_statement`: Problem being solved

**Output JSON**:
```json
{
  "problem_summary": "string (2-3 sentences)",
  "opportunity_assessment": "string (detailed assessment)",
  "market_attractiveness_score": "number (1-100)",
  "risk_assessment": "string (key risks)",
  "key_insights": "array of strings"
}
```

**Metrics to Validate**:
- Market size alignment with TAM/SAM analysis
- Risk score impacts viability
- Problem-solution fit clarity
- Competitive positioning

---

### 2. Competitor Research Agent

**Purpose**: Identify and analyze competition

**Inputs**:
- `startup_idea`: Idea being analyzed
- `industry`: Market context

**Output JSON**:
```json
{
  "direct_competitors": "array of competitor objects",
  "indirect_competitors": "array of alternative solutions",
  "comparison_table": "features comparison across competitors",
  "differentiation_opportunities": "array of differentiators"
}
```

**Key Outputs**:
- 3-5 direct competitors with features/pricing
- 2-3 indirect competitors with threat level
- Specific differentiation gaps identified

**Validation**:
- Competitors should be real and current
- Feature differences should be accurate
- Differentiation should be defensible

---

### 3. Market Research Agent

**Purpose**: Size market and identify trends

**Inputs**:
- `startup_idea`: Idea being analyzed
- `industry`: Market context

**Output JSON**:
```json
{
  "tam": "string (Total Addressable Market)",
  "sam": "string (Serviceable Available Market)",
  "som": "string (Serviceable Obtainable Market)",
  "market_size_estimate": "string (with numbers)",
  "industry_trends": "array of trend descriptions",
  "growth_opportunities": "array of expansion opportunities"
}
```

**Key Outputs**:
- TAM: $1B+ (global addressable market)
- SAM: 10-20% of TAM (realistic initial focus)
- SOM: 2-5% of SAM (3-5 year goal)
- 3-5 relevant industry trends
- 3-5 growth expansion areas

---

### 4. Customer Persona Agent

**Purpose**: Define target users and their motivations

**Inputs**:
- `startup_idea`: Idea being analyzed
- `industry`: Market context
- `problem_statement`: Problem definition

**Output JSON**:
```json
{
  "personas": "array of 2-3 detailed personas",
  "primary_pain_points": "array of 4-5 pain points",
  "buying_motivations": "array of 4-5 motivations",
  "behavioral_patterns": "array of behavioral insights"
}
```

**Persona Structure**:
```json
{
  "name": "string",
  "role": "string (job title)",
  "demographics": "string",
  "goals": "array",
  "challenges": "array",
  "how_they_work": "string (current workflow)"
}
```

---

### 5. MVP Planner Agent

**Purpose**: Prioritize features for minimum viable product

**Inputs**:
- `startup_idea`: Idea being analyzed
- `industry`: Market context

**Output JSON**:
```json
{
  "core_features": "array of 5-7 essential features",
  "nice_to_have_features": "array of nice-to-haves",
  "development_priorities": "array of phases with timeline",
  "estimated_timeline": "string (e.g., '6-8 weeks')",
  "success_metrics": "array of metrics to track"
}
```

**Core Feature Criteria**:
- Solves primary pain point
- Validates core value proposition
- Enables first user acquisition
- Differentiated from competitors

**Timeline Estimates**:
- MVP build: 4-12 weeks depending on complexity
- Phase 1: 2-3 weeks (minimal feature set)
- Phase 2: 2-3 weeks (core workflows)
- Total: 6-10 weeks typical

---

### 6. Pricing Strategy Agent

**Purpose**: Recommend pricing models and tiers

**Inputs**:
- `startup_idea`: Idea being analyzed
- `industry`: Market context

**Output JSON**:
```json
{
  "subscription_models": "array of 2-3 pricing tiers",
  "freemium_option": "object with free tier details",
  "enterprise_pricing": "object with enterprise approach",
  "recommended_pricing": "string with rationale",
  "comparable_pricing": "string (competitor benchmarks)",
  "payment_frequency": "string (monthly/annual)",
  "churn_prevention": "array of retention strategies"
}
```

**Tier Structure**:
- Starter: $29-99/month (for individual users/SMBs)
- Pro: $99-299/month (for growing teams)
- Enterprise: Custom/contact sales

**Annual Discount**: Typically 15-20% off monthly × 12

---

### 7. Go-To-Market Agent

**Purpose**: Develop customer acquisition strategy

**Inputs**:
- `startup_idea`: Idea being analyzed
- `industry`: Market context

**Output JSON**:
```json
{
  "launch_strategy": "string (approach and timing)",
  "acquisition_channels": "array of 5-7 channels",
  "content_strategy": "array of content types and topics",
  "distribution_strategy": "string (sales/self-serve/marketplace)",
  "first_users_strategy": "string (how to get first 100)",
  "partnership_opportunities": "array of partnership types",
  "messaging": "string (value prop and positioning)",
  "positioning": "string (vs. competitors)",
  "target_first_market": "string (niche to focus on)"
}
```

**Acquisition Channels** (priority order):
1. Direct outreach to ICP (Ideal Customer Profile)
2. Content marketing & SEO
3. Product Hunt / communities
4. Partnerships & integrations
5. Word-of-mouth referral
6. Paid advertising (if unit economics allow)

---

### 8. Execution Roadmap Agent

**Purpose**: Create detailed 12-month execution plan

**Inputs**:
- `startup_idea`: Idea being analyzed
- `industry`: Market context

**Output JSON**:
```json
{
  "thirty_day_plan": "object with focus and milestones",
  "sixty_day_plan": "object with focus and milestones",
  "ninety_day_plan": "object with focus and milestones",
  "six_month_plan": "object with strategic focus",
  "one_year_plan": "object with vision and targets",
  "critical_path": "array of dependencies",
  "risk_mitigation": "array of risks and mitigations"
}
```

**Phase Breakdown**:

**30 Days**: Foundation
- MVP development continues
- Initial user interviews
- Preliminary marketing setup
- Seed funding preparation

**60 Days**: Beta Launch
- Closed beta with 20-50 users
- Product refinement from feedback
- Metrics tracking setup
- Content marketing begins

**90 Days**: Public Launch
- Public launch / Product Hunt
- First paying users acquired
- Founder-led sales outreach
- $50k-100k MRR target

**6 Months**: Early Growth
- Product market fit validation
- Team hiring begins
- Funding round (Seed/Series A)
- $200k-500k MRR target

**1 Year**: Scaled Growth
- Product expansion
- Team building (5-10 people)
- Series A or Series B funding
- $1M+ ARR target

---

## Agent Coordination

Agents run sequentially in this order:

1. **Idea Analysis** → Validates opportunity
2. **Competitor Research** → Understands landscape
3. **Market Research** → Sizes opportunity
4. **Customer Personas** → Defines users
5. **MVP Planner** → Plans product
6. **Pricing Strategy** → Monetization approach
7. **Go-To-Market** → Distribution plan
8. **Execution Roadmap** → Implementation timeline

Each agent receives context from previous agents (via `{startup_idea}`, `{industry}`, `{problem_statement}`)

---

## Output Validation

Each agent output is validated for:

1. **Structural Validity**: Valid JSON with required fields
2. **Data Types**: Strings, numbers, arrays are correct types
3. **Completeness**: All required fields populated
4. **Reasonableness**: Numbers and estimates are realistic
5. **Consistency**: Outputs align with previous agents

---

## Error Handling

If agent fails:
1. Log error with agent name and attempt count
2. Retry with simplified prompt (if retry < 3)
3. If persistent failure, mark analysis as "failed"
4. Return error message to user

---

## Future Enhancements

- Add team composition recommendations
- Include fundraising strategy details
- Add competitive intelligence source citations
- Include customer discovery script templates
- Add go-to-market budget allocations
- Include hiring plan recommendations
- Add technology stack recommendations
