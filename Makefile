# AI Automation Empire - Makefile for common commands

.PHONY: help install start stop restart logs clean test build

help:
	@echo "🤖 AI Automation Empire - Commands"
	@echo "=================================="
	@echo ""
	@echo "  make install    - Install and setup the entire system"
	@echo "  make start      - Start all services"
	@echo "  make stop       - Stop all services"
	@echo "  make restart    - Restart all services"
	@echo "  make logs       - View logs from all services"
	@echo "  make clean      - Stop and remove all containers and volumes"
	@echo "  make test       - Run tests"
	@echo "  make build      - Build Docker images"
	@echo "  make admin      - Create admin user"
	@echo "  make shell      - Open backend shell"
	@echo ""

install:
	@echo "🚀 Installing AI Automation Empire..."
	@./install.sh

start:
	@echo "▶️  Starting services..."
	@docker-compose up -d
	@echo "✅ Services started!"
	@echo "   Dashboard: http://localhost:3000"
	@echo "   API: http://localhost:8000/docs"

stop:
	@echo "⏹️  Stopping services..."
	@docker-compose down
	@echo "✅ Services stopped!"

restart:
	@echo "🔄 Restarting services..."
	@docker-compose restart
	@echo "✅ Services restarted!"

logs:
	@docker-compose logs -f

clean:
	@echo "🧹 Cleaning up..."
	@docker-compose down -v
	@echo "✅ Cleanup complete!"

test:
	@echo "🧪 Running tests..."
	@docker-compose exec api pytest
	@echo "✅ Tests complete!"

build:
	@echo "🏗️  Building Docker images..."
	@docker-compose build
	@echo "✅ Build complete!"

admin:
	@echo "👤 Creating admin user..."
	@docker-compose exec api python scripts/create_admin.py

shell:
	@docker-compose exec api /bin/bash

db-shell:
	@docker-compose exec postgres psql -U automation_user -d ai_automation_empire

redis-shell:
	@docker-compose exec redis redis-cli

flower:
	@echo "Opening Flower monitoring..."
	@open http://localhost:5555 || xdg-open http://localhost:5555

dashboard:
	@echo "Opening dashboard..."
	@open http://localhost:3000 || xdg-open http://localhost:3000

api-docs:
	@echo "Opening API docs..."
	@open http://localhost:8000/docs || xdg-open http://localhost:8000/docs
