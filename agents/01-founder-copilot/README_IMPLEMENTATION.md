# Founder Copilot

An autonomous AI startup advisor that provides complete business analysis for your startup idea in minutes.

## Features

✨ **Comprehensive Analysis** - Get market research, competitor analysis, customer personas, MVP planning, pricing strategies, go-to-market strategies, and execution roadmaps - all in one place.

🚀 **AI-Powered Agents** - Multiple specialized AI agents work together to analyze different aspects of your startup.

📊 **Professional Reports** - Export beautiful, consulting-grade reports in PDF or Markdown.

⚡ **Fast Results** - Get a complete analysis in 2-3 minutes without manual research.

🎨 **Premium Design** - Modern, professional interface inspired by leading venture capital firms.

## What You Get

When you analyze a startup idea, Founder Copilot provides:

1. **Idea Analysis** - Problem summary, opportunity assessment, market attractiveness score, risk assessment
2. **Competitor Research** - Direct competitors, indirect competitors, feature comparison, differentiation opportunities
3. **Market Research** - TAM, SAM, SOM, market size estimates, industry trends, growth opportunities
4. **Customer Personas** - Detailed customer profiles, pain points, buying motivations, behavioral patterns
5. **MVP Planning** - Core features, nice-to-have features, development priorities, timeline
6. **Pricing Strategy** - Subscription models, freemium options, enterprise pricing
7. **Go-To-Market Strategy** - Launch strategy, acquisition channels, content strategy, distribution
8. **Execution Roadmap** - 30-day, 60-day, 90-day, 6-month, and 1-year plans

## Tech Stack

- **Frontend**: Next.js 14, TypeScript, TailwindCSS, ShadCN UI
- **Backend**: FastAPI, Python, async/await
- **AI**: OpenAI, Claude, Google Gemini (provider abstraction)
- **Database**: PostgreSQL
- **Deployment**: Vercel (frontend), Heroku (backend)

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 12+

### Quick Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys and database URL
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF
npm run dev
```

Visit `http://localhost:3000`

For detailed setup instructions, see [docs/SETUP.md](docs/SETUP.md)

## Project Structure

```
agents/01-founder-copilot/
├── frontend/               # Next.js application
├── backend/               # FastAPI application
├── docs/                  # Documentation
│   ├── ARCHITECTURE.md    # System architecture
│   ├── API.md            # API documentation
│   ├── SETUP.md          # Setup instructions
│   ├── AGENTS.md         # Agent specifications
│   └── DEPLOYMENT.md     # Deployment guide
├── prompts/              # Agent prompt templates
└── PROJECT_PLAN.md       # Implementation plan
```

## Documentation

- **[Architecture](docs/ARCHITECTURE.md)** - System design and data flow
- **[API Documentation](docs/API.md)** - Complete API reference
- **[Setup Guide](docs/SETUP.md)** - Installation and configuration
- **[Agent Specifications](docs/AGENTS.md)** - Details of each agent
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment

## API Endpoints

- `POST /api/v1/analyze` - Start analysis
- `GET /api/v1/analysis/{id}` - Get status and progress
- `GET /api/v1/report/{id}` - Get completed report
- `GET /api/v1/history` - Get analysis history

See [API.md](docs/API.md) for complete documentation.

## Usage

1. Visit the landing page
2. Click "Start Analysis"
3. Enter your startup idea, industry, and problem statement
4. Wait 2-3 minutes while AI agents analyze your idea
5. View comprehensive report with all analysis
6. Export to PDF for presentations or sharing

## Design Philosophy

Founder Copilot is built on these principles:

- **Not Another ChatBot** - Structured analysis, not conversational
- **Consulting Quality** - Professional insights like a real advisor would provide
- **Fast & Efficient** - Minutes instead of weeks of research
- **Premium Experience** - Modern design inspired by leading VC firms
- **Practical Output** - Actionable insights you can use immediately

## Success Criteria

A user should be able to:

1. Enter a startup idea
2. Wait 1-2 minutes
3. Receive a professional startup report

...without manually researching anything.

The final experience should feel like receiving advice from a startup consultant rather than chatting with an AI assistant.

## Future Enhancements

- WebSocket for real-time progress updates
- Multi-idea comparison
- Custom agent configurations
- Team collaboration features
- Historical analysis tracking
- Investor pitch deck generation
- Financial modeling tools
- Customer acquisition calculator

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check documentation in `/docs`
- Review API documentation

## Roadmap

**Phase 1** (Current)
- Core analysis functionality
- 8 specialized agents
- Professional report generation
- Basic authentication

**Phase 2**
- WebSocket real-time updates
- Financial modeling
- Team collaboration
- Premium features

**Phase 3**
- API for third-party integrations
- Custom agent creation
- Advanced analytics
- Enterprise features

---

Built with ❤️ for founders who want to validate ideas faster.
