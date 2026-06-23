# Job Hunter - Setup Instructions

## Prerequisites

- Python 3.8+
- Node.js 18+
- OpenAI API Key (or Anthropic API Key)

## Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. Run the backend server:
```bash
python main.py
```

The backend will run on `http://localhost:8000`

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.local.example .env.local
```

4. Run the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Enter your target job details (title, skills, experience, location)
3. Paste your resume content
4. Follow the guided workflow to get:
   - Resume match analysis
   - Skill gap identification
   - Personalized cover letter
   - Interview preparation guide

## API Endpoints

- `POST /api/search` - Create new job search
- `GET /api/search/{id}` - Get job search status
- `POST /api/search/{id}/resume` - Upload resume for analysis
- `GET /api/search/{id}/skill-gaps` - Get skill gap analysis
- `GET /api/search/{id}/cover-letter` - Generate cover letter
- `GET /api/search/{id}/interview` - Get interview preparation
- `GET /api/search/{id}/report` - Get complete report
- `GET /api/health` - Health check

## Technology Stack

### Backend
- FastAPI
- SQLAlchemy
- OpenAI/Anthropic APIs

### Frontend
- Next.js 14
- TypeScript
- TailwindCSS
- ShadCN UI
- Radix UI

## Design Theme

- **Colors**: Forest Green, Ivory, Graphite, Muted Gold
- **Typography**: Space Grotesk (headings), Manrope (body)
- **Style**: Professional career platform inspired by LinkedIn Premium, Levels.fyi
