# 🏗️ System Architecture

## Overview

AI Automation Empire is a microservices-based architecture designed for scalability, reliability, and performance.

## System Components

```
┌─────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                          │
│                                                              │
│    ┌──────────────────────────────────────────────┐         │
│    │         Next.js Dashboard (Port 3000)        │         │
│    │    - React 18 + TypeScript                   │         │
│    │    - Tailwind CSS + Shadcn UI                │         │
│    │    - Real-time updates via WebSocket         │         │
│    └──────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      API LAYER                               │
│                                                              │
│    ┌──────────────────────────────────────────────┐         │
│    │         FastAPI Backend (Port 8000)          │         │
│    │    - RESTful API                             │         │
│    │    - JWT Authentication                       │         │
│    │    - OpenAPI/Swagger Docs                    │         │
│    │    - Rate Limiting & CORS                    │         │
│    └──────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                       │
│                                                              │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐  │
│  │   Scrapers     │  │   AI Services  │  │  Outreach    │  │
│  │                │  │                │  │              │  │
│  │ - Playwright   │  │ - Classifier   │  │ - Email      │  │
│  │ - Selenium     │  │ - Generator    │  │ - WhatsApp   │  │
│  │ - Anti-bot     │  │ - Analyzer     │  │ - LinkedIn   │  │
│  │ - Proxies      │  │ - AI Agent     │  │ - Telegram   │  │
│  └────────────────┘  └────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   ASYNC TASK PROCESSING                      │
│                                                              │
│    ┌──────────────────────────────────────────────┐         │
│    │         Celery Workers + Beat                │         │
│    │    - Scraping tasks                          │         │
│    │    - AI processing                           │         │
│    │    - Outreach automation                     │         │
│    │    - Scheduled jobs                          │         │
│    │                                              │         │
│    │    Flower (Port 5555) - Monitoring          │         │
│    └──────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                │
│                                                              │
│  ┌────────────────────────┐  ┌───────────────────────────┐  │
│  │  PostgreSQL (Port 5432) │  │  Redis (Port 6379)       │  │
│  │                         │  │                           │  │
│  │  - Users                │  │  - Session cache          │  │
│  │  - Opportunities        │  │  - Celery broker          │  │
│  │  - Proposals            │  │  - Task results           │  │
│  │  - Clients              │  │  - Rate limiting          │  │
│  │  - Campaigns            │  │                           │  │
│  │  - Scraping jobs        │  │                           │  │
│  └────────────────────────┘  └───────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 EXTERNAL SERVICES                            │
│                                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │ OpenAI   │ │ Anthropic│ │ SendGrid │ │  Twilio  │      │
│  │   GPT    │ │  Claude  │ │  Email   │ │ WhatsApp │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
│                                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │  Groq    │ │  Stripe  │ │ 2Captcha │ │  Proxies │      │
│  │ Mixtral  │ │ Payment  │ │  Solver  │ │ Rotation │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Scraping Pipeline

```
User creates scraping job
    ↓
Job queued in Celery
    ↓
Celery worker picks up task
    ↓
Playwright/Selenium scraper starts
    ↓
Anti-bot measures applied (proxies, delays, headers)
    ↓
Data extracted from target site
    ↓
Raw data saved to database
    ↓
AI processing task queued
    ↓
AI classifies and scores opportunities
    ↓
High-quality opportunities flagged
    ↓
Proposal generation triggered (if enabled)
```

### 2. Autonomous Agent Loop

```
Celery Beat scheduler (every hour)
    ↓
Autonomous agent task starts
    ↓
Find unprocessed opportunities
    ↓
For each opportunity:
    - AI analysis and scoring
    - Pain point extraction
    - Keyword identification
    - Budget analysis
    ↓
If score > threshold:
    - Generate personalized proposal
    - Determine outreach channel
    - Queue outreach task
    ↓
Outreach task:
    - Send via Email/WhatsApp/LinkedIn
    - Log interaction
    - Schedule follow-up
```

### 3. API Request Flow

```
Client request → CORS middleware
    ↓
Authentication middleware (JWT)
    ↓
Rate limiting check
    ↓
Route handler
    ↓
Database query (SQLAlchemy ORM)
    ↓
Response serialization (Pydantic)
    ↓
JSON response to client
```

## Database Schema

### Core Tables

- **users**: User accounts and authentication
- **opportunities**: Scraped job opportunities
- **clients**: Client/company information
- **proposals**: Generated proposals
- **outreach_logs**: Communication tracking
- **outreach_campaigns**: Campaign management
- **scraping_jobs**: Scraping job configurations
- **scraping_logs**: Scraping execution logs
- **subscriptions**: User subscription info
- **usage_logs**: Usage tracking for billing

### Relationships

```
User 1:N Opportunities
User 1:N ScrapingJobs
User 1:N Proposals
User 1:N Campaigns
User 1:1 Subscription

Opportunity N:1 Client
Opportunity 1:N Proposals

Campaign 1:N OutreachLogs
Client 1:N OutreachLogs

ScrapingJob 1:N ScrapingLogs
```

## Security Architecture

### Authentication
- JWT tokens with configurable expiration
- Bcrypt password hashing (12 rounds)
- Token refresh mechanism
- Secure cookie storage

### Authorization
- Role-based access control (RBAC)
- User roles: admin, premium, user
- Endpoint-level permissions
- Resource ownership validation

### Data Protection
- SQL injection prevention via ORM
- XSS prevention via output sanitization
- CSRF tokens for state-changing operations
- Environment variable secrets
- Docker container isolation

## Scalability

### Horizontal Scaling
- Stateless API servers (can run multiple instances)
- Redis for shared session state
- PostgreSQL with read replicas
- Celery workers (add more as needed)

### Vertical Scaling
- Database connection pooling
- Redis connection pooling
- Async I/O for scraping
- Efficient database indexing

### Caching Strategy
- Redis cache for frequently accessed data
- Database query result caching
- API response caching
- Browser cache headers

## Monitoring & Observability

### Application Monitoring
- Flower for Celery task monitoring
- FastAPI automatic request logging
- Database query logging
- Error tracking with Sentry (optional)

### System Metrics
- Docker container stats
- Database connection pool metrics
- Redis memory usage
- Celery queue lengths

### Alerting
- Failed task notifications
- High error rate alerts
- Resource usage alerts
- Scraping failure notifications

## Deployment Architecture

### Development
```
Single machine (Docker Compose)
- All services on localhost
- Shared volumes for hot reload
- Debug mode enabled
```

### Production
```
Load Balancer
    ↓
API Servers (3+ instances)
    ↓
Database Cluster (Primary + Replicas)
    ↓
Redis Cluster (Sentinel/Cluster mode)
    ↓
Celery Workers (Auto-scaling group)
```

## Technology Stack Summary

### Backend
- **Language**: Python 3.11
- **Framework**: FastAPI 0.109
- **ORM**: SQLAlchemy 2.0
- **Task Queue**: Celery 5.3 + Redis
- **Scraping**: Playwright, Selenium
- **AI**: OpenAI, Anthropic, Groq

### Frontend
- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Components**: Shadcn UI
- **State**: Zustand
- **API Client**: Axios + React Query

### Infrastructure
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Containerization**: Docker + Docker Compose
- **Orchestration**: Kubernetes (optional)
- **CI/CD**: GitHub Actions (optional)

### External Services
- **AI Models**: OpenAI, Anthropic, Groq
- **Email**: SendGrid
- **SMS/WhatsApp**: Twilio
- **Payments**: Stripe
- **Monitoring**: Sentry, Flower

## Performance Benchmarks

### Expected Performance
- **API Response Time**: < 100ms (P95)
- **Scraping Speed**: 100-500 items/minute
- **AI Processing**: 2-5 seconds per opportunity
- **Concurrent Users**: 1000+ (with proper scaling)
- **Database Queries**: < 50ms (P95)
- **Task Queue Throughput**: 1000+ tasks/minute

### Optimization Strategies
- Database query optimization with indexes
- Async I/O for all external calls
- Connection pooling for database and Redis
- Celery result caching
- CDN for static assets
- Gzip compression for API responses

## Disaster Recovery

### Backup Strategy
- Daily database backups
- Point-in-time recovery enabled
- Configuration backups
- Docker image versioning

### High Availability
- Database replicas for failover
- Redis Sentinel for automatic failover
- Multiple API server instances
- Health checks and auto-restart
