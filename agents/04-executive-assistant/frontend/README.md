# Executive Assistant - Frontend

Next.js + Tailwind frontend for Agent 04.

## Setup
From this folder:

```bash
npm install
```

## Run
```bash
npm run dev -- --port 3000
```

## API Base URL
Configure the backend URL via env var:

- `NEXT_PUBLIC_API_BASE_URL` (default: `http://localhost:8000`)

Example (Windows PowerShell):

```powershell
$env:NEXT_PUBLIC_API_BASE_URL="http://localhost:8000"
npm run dev -- --port 3000
```

## Notes
MVP pages are wired next:
- `/workspace` - background workspace report orchestration + polling
- `/tasks` - priority analysis
- `/meetings` - meeting preparation
- `/decisions` - decision support + history

