# 🤖 AI Automation Empire

> **The Ultimate Web Scraping & Automation Platform** - Production-ready system for freelancers, entrepreneurs, and automation businesses.

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Features

### 🕷️ **Intelligent Web Scraping**
- Multi-platform scraping (Upwork, Freelancer, LinkedIn, Indeed, and more)
- Playwright-based browser automation with anti-bot protection
- Rotating proxies and captcha solving
- Automatic pagination and infinite scroll handling
- Headless and visible browser modes

### 🧠 **AI-Powered Processing**
- Opportunity classification and scoring
- Automatic keyword extraction
- Pain point detection
- Sentiment analysis
- Budget and difficulty estimation
- Skill requirement extraction

### ✍️ **Automated Proposal Generation**
- AI-generated personalized proposals
- Multiple writing styles (professional, casual, enthusiastic)
- Context-aware content
- Follow-up message generation
- Template customization

### 📧 **Multi-Channel Outreach**
- **Email**: SendGrid integration
- **WhatsApp**: Twilio API
- **LinkedIn**: Browser automation
- **Telegram**: Bot API
- **SMS**: Twilio integration

### 🤖 **Autonomous Agent**
- 24/7 automated operation loop:
  1. Scrape opportunities
  2. Analyze with AI
  3. Generate proposals
  4. Auto-contact clients
  5. Follow-up sequences
  6. Log everything

### 📊 **Real-Time Dashboard**
- Next.js 14 with Tailwind CSS
- Live statistics and analytics
- Campaign management
- Scraping job control
- Proposal editor
- Performance metrics

### 💼 **SaaS-Ready Features**
- Multi-tenancy support
- Stripe payment integration
- Usage tracking and limits
- API rate limiting
- Role-based access control
- Webhook support

## 🏗️ Architecture

```
AI Automation Empire/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Configuration & security
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   │   ├── scrapers/   # Scraping engines
│   │   │   ├── ai/         # AI processing
│   │   │   └── outreach/   # Communication
│   │   └── workers/        # Celery tasks
│   └── requirements.txt
├── frontend/               # Next.js Frontend
│   ├── app/
│   ├── components/
│   └── package.json
├── docker-compose.yml      # Full stack orchestration
├── .env.example           # Environment variables template
└── install.sh             # One-command installer

Services:
- PostgreSQL (Database)
- Redis (Cache & Celery broker)
- FastAPI (API Server)
- Celery Worker (Async tasks)
- Celery Beat (Scheduler)
- Flower (Task monitoring)
- Next.js (Frontend)
```

## ⚡ Quick Start (One Command)

```bash
curl -fsSL https://raw.githubusercontent.com/yourusername/ai-automation-empire/main/install.sh | bash
```

Or manually:

```bash
git clone https://github.com/yourusername/ai-automation-empire.git
cd ai-automation-empire
chmod +x install.sh
./install.sh
```

The installer will:
1. Check system requirements
2. Install dependencies
3. Set up environment variables
4. Initialize database
5. Start all services with Docker Compose
6. Open the dashboard in your browser

## 📦 Manual Installation

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 20+
- PostgreSQL 15+
- Redis 7+

### Step 1: Clone & Setup

```bash
git clone https://github.com/yourusername/ai-automation-empire.git
cd ai-automation-empire
```

### Step 2: Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys and credentials
nano .env
```

### Step 3: Start Services

```bash
docker-compose up -d
```

### Step 4: Initialize Database

```bash
docker-compose exec api alembic upgrade head
```

### Step 5: Access the System

- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Flower (Celery Monitor)**: http://localhost:5555

## 🔧 Configuration

### Required API Keys

1. **AI Models** (choose at least one):
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/
   - Groq: https://console.groq.com/

2. **Email** (optional):
   - SendGrid: https://sendgrid.com/

3. **SMS/WhatsApp** (optional):
   - Twilio: https://www.twilio.com/

4. **Payments** (for SaaS mode):
   - Stripe: https://stripe.com/

### Environment Variables

See `.env.example` for all configuration options.

## 📚 Usage Examples

### Create a Scraping Job

```bash
curl -X POST http://localhost:8000/api/v1/scraping/jobs \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python Developer Jobs",
    "platform": "upwork",
    "keywords": ["python", "fastapi", "django"],
    "max_pages": 5
  }'
```

### List Opportunities

```bash
curl http://localhost:8000/api/v1/opportunities?min_score=70 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Generate Proposal

```python
from app.services.ai.proposal_generator import ProposalGenerator

generator = ProposalGenerator(model_provider="openai")

proposal = await generator.generate_proposal(
    opportunity={"title": "Python API Development", "description": "..."},
    user_profile={"name": "John Doe", "skills": ["Python", "FastAPI"]},
    style="professional"
)

print(proposal["content"])
```

## 🔄 Autonomous Agent

The system includes an autonomous agent that runs continuously:

```python
# Automatically triggered every hour via Celery Beat
from app.workers.tasks import autonomous_agent_loop

# Manual trigger
autonomous_agent_loop.delay()
```

The agent:
1. Finds new opportunities from active scraping jobs
2. Analyzes and scores each opportunity
3. Generates proposals for high-quality opportunities (score > 70)
4. Sends outreach messages via configured channels
5. Schedules follow-ups
6. Logs all activities

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# Integration tests
docker-compose -f docker-compose.test.yml up
```

## 📈 Monitoring

### Flower (Celery Tasks)
Access Flower at http://localhost:5555 to monitor:
- Active workers
- Task queues
- Task history
- Success/failure rates

### Application Logs

```bash
# API logs
docker-compose logs -f api

# Worker logs
docker-compose logs -f celery_worker

# All services
docker-compose logs -f
```

## 🔒 Security

- JWT-based authentication
- Password hashing with bcrypt
- SQL injection protection via SQLAlchemy ORM
- CORS configuration
- Rate limiting (configurable)
- Environment variable secrets
- Docker container isolation

## 🚀 Deployment

### Production Checklist

- [ ] Change `SECRET_KEY` in `.env`
- [ ] Set `DEBUG=false`
- [ ] Configure production database
- [ ] Set up SSL/TLS certificates
- [ ] Configure firewall rules
- [ ] Set up monitoring (Sentry, etc.)
- [ ] Configure backups
- [ ] Set up CI/CD pipeline
- [ ] Review security settings

### Deploy to AWS/GCP/Azure

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Push to registry
docker-compose -f docker-compose.prod.yml push

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Credits

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [Playwright](https://playwright.dev/) - Browser automation
- [OpenAI](https://openai.com/) - AI models
- [Next.js](https://nextjs.org/) - Frontend framework
- [Celery](https://docs.celeryproject.org/) - Distributed task queue
- [PostgreSQL](https://www.postgresql.org/) - Database
- [Redis](https://redis.io/) - Cache & message broker

## 📞 Support

- 📧 Email: support@aiautomationempire.com
- 💬 Discord: [Join our community](https://discord.gg/automation)
- 📖 Docs: [Full Documentation](https://docs.aiautomationempire.com)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/ai-automation-empire/issues)

## 🎯 Roadmap

- [ ] Chrome extension for one-click scraping
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] CRM integration (Salesforce, HubSpot)
- [ ] Voice message generation
- [ ] Video proposal generation
- [ ] Blockchain-based verification
- [ ] Decentralized proxy network

---

**Built with ❤️ for the freelance and automation community**

⭐ Star this repo if you find it useful!
