# Founder Copilot - Deployment Guide

## Deployment Overview

Founder Copilot is designed to deploy on modern cloud platforms:

- **Frontend**: Vercel (Next.js optimized)
- **Backend**: Heroku, Railway, or Fly.io
- **Database**: Managed PostgreSQL (Heroku, AWS RDS, or DigitalOcean)
- **Optional Storage**: S3 for PDF exports

## Prerequisites

- GitHub account for code
- Vercel account (free tier available)
- Heroku or alternative backend hosting account
- PostgreSQL database (managed or self-hosted)
- API keys for OpenAI/Claude/Gemini

## Step 1: Prepare Code for Deployment

### Backend Preparation

1. Create `Procfile` for Heroku:

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. Create `runtime.txt`:

```
python-3.10.13
```

3. Ensure `.env` variables are documented in `requirements.txt`

### Frontend Preparation

1. Create `.env.production`:

```
NEXT_PUBLIC_API_URL=https://your-backend.herokuapp.com
```

2. Build verification:

```bash
npm run build
npm start
```

## Step 2: Deploy Backend to Heroku

### Option A: Using Heroku CLI

```bash
# Login to Heroku
heroku login

# Create app
heroku create founder-copilot-api

# Set environment variables
heroku config:set DATABASE_URL="postgresql://..."
heroku config:set OPENAI_API_KEY="sk-..."
heroku config:set DEFAULT_PROVIDER="openai"
heroku config:set FRONTEND_URL="https://your-frontend.vercel.app"

# Deploy
git push heroku main

# Check logs
heroku logs --tail
```

### Option B: Using Heroku Dashboard

1. Connect GitHub repository
2. Enable automatic deploys from main branch
3. Set config vars in Settings tab
4. Manual deploy first build

### Database Setup

```bash
# Create PostgreSQL add-on
heroku addons:create heroku-postgresql:standard-0 -a founder-copilot-api

# Get DATABASE_URL (automatic via config var)
heroku config -a founder-copilot-api
```

## Step 3: Deploy Frontend to Vercel

### Option A: Using Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### Option B: Using Vercel Dashboard

1. Go to https://vercel.com/new
2. Import GitHub repository
3. Select "Next.js" framework
4. Add environment variables:
   - `NEXT_PUBLIC_API_URL`: Your backend URL
5. Deploy

### Automatic Deployments

Vercel automatically deploys on:
- Push to `main` branch
- Pull requests (preview deployments)

Configure in `vercel.json`:

```json
{
  "env": {
    "NEXT_PUBLIC_API_URL": "@api_url"
  },
  "buildCommand": "npm run build",
  "outputDirectory": ".next"
}
```

## Step 4: Configure Custom Domain (Optional)

### Frontend Domain

```bash
# In Vercel Dashboard
Settings → Domains → Add domain
```

### Backend Domain

```bash
# For Heroku
heroku domains:add api.example.com
```

Then configure DNS CNAME to Heroku/backend provider.

## Step 5: Set Up Monitoring

### Backend Monitoring

```bash
# Heroku logs
heroku logs --tail -a founder-copilot-api

# Or use Papertrail add-on
heroku addons:create papertrail -a founder-copilot-api
```

### Frontend Monitoring

Vercel provides built-in analytics and error tracking.

## Environment Variables Checklist

### Backend (.env or Heroku config)

- [ ] `DATABASE_URL`: PostgreSQL connection string
- [ ] `OPENAI_API_KEY`: OpenAI API key (if using OpenAI)
- [ ] `ANTHROPIC_API_KEY`: Anthropic API key (if using Claude)
- [ ] `GOOGLE_API_KEY`: Google API key (if using Gemini)
- [ ] `DEFAULT_PROVIDER`: Which AI provider to use
- [ ] `FRONTEND_URL`: Frontend URL for CORS

### Frontend (.env.production)

- [ ] `NEXT_PUBLIC_API_URL`: Backend API URL

## Database Migrations (If Needed)

```bash
# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head

# Or via Heroku
heroku run "python -m app.main" -a founder-copilot-api
```

## Testing Deployment

### Backend Health Check

```bash
curl https://your-backend.herokuapp.com/health
```

Expected response:
```json
{"status": "healthy", "service": "founder-copilot-api"}
```

### Frontend Health Check

1. Visit https://your-frontend.vercel.app
2. Should see landing page
3. Navigate to /dashboard (should work)
4. Try creating an analysis

### End-to-End Test

```bash
# 1. Visit frontend
open https://your-frontend.vercel.app

# 2. Click "Start Analysis"
# 3. Fill form and submit
# 4. Monitor /api/v1/analysis endpoint
# 5. Should complete in 2-3 minutes
# 6. View report
```

## Scaling Considerations

### Database

- Start: Heroku Postgres Standard (0) 
- As grows: Upgrade to Premium/Production tier
- 1M+ users: Consider AWS RDS or DigitalOcean managed DB

### Backend

- Start: Hobby dyno on Heroku (free)
- As grows: Standard dyno ($7/mo)
- High load: Scale to multiple dynos or use container orchestration

### Frontend

- Vercel handles auto-scaling
- No action needed unless advanced customization

## Cost Estimation

### Small Deployment

- Frontend (Vercel): Free
- Backend (Heroku): $7/mo (Standard dyno)
- Database (Heroku Postgres): $9/mo (Standard 0)
- **Total: ~$16/mo**

### Production Deployment

- Frontend (Vercel): $20/mo (Pro plan)
- Backend: $25+/mo (multiple dynos or alternative)
- Database: $50+/mo (Premium PostgreSQL)
- SSL Certificate: Included in most platforms
- **Total: $95+/mo**

## Continuous Deployment Setup

### GitHub Actions for Backend

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Backend

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: heroku/deploy-action@v3
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: "founder-copilot-api"
          heroku_email: ${{ secrets.HEROKU_EMAIL }}
```

### GitHub Actions for Frontend

Vercel handles this automatically when connected to GitHub.

## Rollback Procedures

### Backend

```bash
# View deployment history
heroku releases -a founder-copilot-api

# Rollback to previous version
heroku releases:rollback -a founder-copilot-api
```

### Frontend

```bash
# Vercel automatically keeps deployment history
# Rollback via Vercel Dashboard → Deployments → Redeploy
```

## Troubleshooting

### Backend won't start

```bash
# Check logs
heroku logs --tail -a founder-copilot-api

# Common issue: Missing DATABASE_URL
heroku config -a founder-copilot-api
```

### API calls failing from frontend

Check:
- `NEXT_PUBLIC_API_URL` is correct
- CORS configured correctly in backend
- Backend is running (health check)

### Database connection errors

```bash
# Test connection
heroku pg:info -a founder-copilot-api

# Reset database (CAUTION)
heroku pg:reset DATABASE -a founder-copilot-api --confirm founder-copilot-api
```

## Security Checklist

- [ ] CORS properly configured for frontend domain
- [ ] API keys stored in environment variables (not hardcoded)
- [ ] HTTPS enabled for all connections
- [ ] Database user has minimum permissions needed
- [ ] SQL injection protection (SQLAlchemy ORM handles this)
- [ ] Rate limiting configured (future)
- [ ] Input validation on all endpoints
- [ ] Error messages don't leak sensitive info

## Maintenance

### Regular Tasks

- Monitor application logs
- Check error rates in Sentry (if setup)
- Review database usage
- Update dependencies monthly
- Backup database regularly

### Database Backups

```bash
# Automatic backups on Heroku
heroku pg:backups:capture -a founder-copilot-api

# Download backup
heroku pg:backups:download -a founder-copilot-api
```

## Next Steps

1. Deploy backend first and test API
2. Deploy frontend and test UI
3. Run end-to-end test with real analysis
4. Monitor logs for 24 hours
5. Set up monitoring and alerting
6. Plan scaling if needed
