# 🚀 Quick Start Guide

Get AI Automation Empire running in 5 minutes!

## Prerequisites

- Docker & Docker Compose installed
- At least one AI API key (OpenAI, Anthropic, or Groq)

## Installation

### Option 1: One-Command Install (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/yourusername/ai-automation-empire/main/install.sh | bash
```

### Option 2: Manual Install

```bash
# Clone repository
git clone https://github.com/yourusername/ai-automation-empire.git
cd ai-automation-empire

# Run installer
chmod +x install.sh
./install.sh
```

## Configuration

1. **Edit environment variables:**

```bash
nano .env
```

2. **Add your API keys** (minimum required):

```env
SECRET_KEY=your-generated-secret-key  # Already set by installer
OPENAI_API_KEY=sk-your-openai-key     # Add your key here
```

3. **Restart services:**

```bash
docker-compose restart
```

## First Steps

### 1. Access the Dashboard

Open your browser: http://localhost:3000

### 2. Register an Account

Go to the API docs: http://localhost:8000/docs

Click on `/auth/register` and fill in:
```json
{
  "email": "your@email.com",
  "username": "yourname",
  "password": "secure_password",
  "full_name": "Your Name"
}
```

### 3. Login and Get Token

Click on `/auth/login`:
```json
{
  "email": "your@email.com",
  "password": "secure_password"
}
```

Copy the `access_token` from the response.

### 4. Authorize API Requests

In Swagger UI:
1. Click the 🔓 "Authorize" button at the top
2. Paste your token in the format: `Bearer YOUR_TOKEN`
3. Click "Authorize"

### 5. Create Your First Scraping Job

Go to `/scraping/jobs` POST endpoint:
```json
{
  "name": "Python Jobs on Upwork",
  "platform": "upwork",
  "keywords": ["python", "fastapi"],
  "max_pages": 3,
  "max_items": 50
}
```

### 6. Run the Scraping Job

Use `/scraping/jobs/{job_id}/run` endpoint with your job ID.

### 7. View Opportunities

Check `/opportunities` endpoint to see scraped jobs.

## Common Commands

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View Celery tasks
# Open http://localhost:5555 in browser

# Create admin user
docker-compose exec api python scripts/create_admin.py
```

## Using Makefile (Shortcut)

```bash
# Start services
make start

# Stop services
make stop

# View logs
make logs

# Create admin
make admin

# Open dashboard
make dashboard

# Open API docs
make api-docs
```

## Testing the AI Features

### 1. Test Opportunity Classification

```python
# In the API docs, go to your opportunity and it will have AI scores
```

### 2. Test Proposal Generation

The system will automatically generate proposals for opportunities with score > 70.

Or manually via API:
```bash
POST /api/v1/proposals/generate
{
  "opportunity_id": 1
}
```

## Enable Outreach (Optional)

### Email via SendGrid

1. Get API key from https://sendgrid.com/
2. Add to `.env`:
```env
SENDGRID_API_KEY=SG.your-key
EMAIL_FROM=noreply@yourdomain.com
```

### WhatsApp via Twilio

1. Get credentials from https://www.twilio.com/
2. Add to `.env`:
```env
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890
```

## Troubleshooting

### Port Already in Use

```bash
# Check what's using the port
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Database Connection Error

```bash
# Check if PostgreSQL is running
docker-compose ps

# Restart PostgreSQL
docker-compose restart postgres
```

### Can't Scrape Websites

- Make sure you have internet connection
- Some sites block scrapers - use proxies
- Check if site requires login

## Next Steps

1. Configure additional AI providers (Anthropic, Groq)
2. Set up outreach channels (Email, WhatsApp)
3. Create multiple scraping jobs for different platforms
4. Customize proposal templates
5. Set up automated campaigns

## Need Help?

- 📖 Read full documentation: [README.md](README.md)
- 🏗️ Architecture details: [ARCHITECTURE.md](ARCHITECTURE.md)
- 🐛 Report issues: GitHub Issues
- 💬 Join community: Discord

## Pro Tips

1. **Start small**: Test with 1-2 pages first
2. **Monitor Flower**: Watch task execution at http://localhost:5555
3. **Use rate limiting**: Don't scrape too fast to avoid blocks
4. **Rotate proxies**: If scraping frequently
5. **Check logs**: `docker-compose logs -f` is your friend

Happy automating! 🤖
