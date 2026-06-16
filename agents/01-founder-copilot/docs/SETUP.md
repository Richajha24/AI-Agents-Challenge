# Founder Copilot - Setup Instructions

## Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 12+
- Git

## Backend Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and fill in:
- `DATABASE_URL`: PostgreSQL connection string
- `DEFAULT_PROVIDER`: openai, claude, or gemini
- `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`: API keys

### 4. Initialize Database

```bash
python -m app.main
# Database tables will be created automatically
```

### 5. Run Backend Server

```bash
python main.py
```

Server runs on `http://localhost:8000`

API docs available at `http://localhost:8000/docs`

---

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

```bash
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF
```

### 3. Run Development Server

```bash
npm run dev
```

Application available at `http://localhost:3000`

### 4. Build for Production

```bash
npm run build
npm start
```

---

## Database Setup

### Using PostgreSQL

```bash
# Create database
createdb founder_copilot

# Connect
psql founder_copilot

# Verify tables created
\dt
```

### Database URL Format

```
postgresql://username:password@localhost:5432/founder_copilot
```

---

## API Keys Setup

### OpenAI

1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Add to `.env`: `OPENAI_API_KEY=sk-...`

### Claude (Anthropic)

1. Go to https://console.anthropic.com/
2. Create new API key
3. Add to `.env`: `ANTHROPIC_API_KEY=sk-...`

### Google Gemini

1. Go to https://makersuite.google.com/app/apikey
2. Create new API key
3. Add to `.env`: `GOOGLE_API_KEY=...`

---

## Testing the System

### 1. Health Check

```bash
curl http://localhost:8000/health
```

### 2. Create Analysis

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "startup_idea": "AI-powered code review platform",
    "industry": "SaaS",
    "problem_statement": "Developers spend hours on manual code reviews"
  }'
```

### 3. Check Status

```bash
curl http://localhost:8000/api/v1/analysis/{analysis_id}
```

### 4. Get Report

```bash
curl http://localhost:8000/api/v1/report/{analysis_id}
```

---

## Docker Setup (Optional)

### Backend Container

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

### Frontend Container

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json .
RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: founder_copilot
      POSTGRES_USER: founder
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://founder:password@postgres:5432/founder_copilot
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    ports:
      - "8000:8000"
    depends_on:
      - postgres

  frontend:
    build: ./frontend
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

Run with:

```bash
docker-compose up
```

---

## Troubleshooting

### Database Connection Error

```
psycopg2.OperationalError: could not connect to server
```

Check:
- PostgreSQL is running
- DATABASE_URL is correct
- Credentials are valid

### API Key Errors

```
AuthenticationError: Invalid API key
```

Check:
- API key is set in .env
- API key is not expired
- API key has necessary permissions

### CORS Errors

If frontend can't reach backend:
- Ensure `CORS_ORIGINS` includes frontend URL
- Check backend is running
- Check `NEXT_PUBLIC_API_URL` is correct

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Find process using port 3000
lsof -i :3000
```

---

## Development Tips

1. Use `DEBUG=true` in `.env` for verbose logging
2. Check `/docs` for interactive API documentation
3. Use browser DevTools for frontend debugging
4. Monitor database with `psql -l` to see tables
5. Use `curl` to test API endpoints manually

---

## Next Steps

1. Read ARCHITECTURE.md for system design
2. Read AGENTS.md for agent specifications
3. Check API.md for endpoint details
4. Deploy to Vercel (frontend) and Heroku (backend)
