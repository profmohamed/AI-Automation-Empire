#!/bin/bash

# AI Automation Empire - One-Command Installer
# This script sets up the entire system with a single command

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║         🤖  AI AUTOMATION EMPIRE  🤖                      ║"
echo "║                                                           ║"
echo "║     The Ultimate Web Scraping & Automation Platform      ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_warning "Please don't run this script as root/sudo"
    exit 1
fi

# Check system requirements
print_info "Checking system requirements..."

# Check Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi
print_success "Docker is installed"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first"
    exit 1
fi
print_success "Docker Compose is installed"

# Check if ports are available
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        return 1
    else
        return 0
    fi
}

print_info "Checking if required ports are available..."
PORTS=(3000 5432 5555 6379 8000)
for port in "${PORTS[@]}"; do
    if check_port $port; then
        print_success "Port $port is available"
    else
        print_error "Port $port is already in use. Please free up this port first."
        exit 1
    fi
done

# Setup environment variables
print_info "Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    print_success "Created .env file from template"
    print_warning "IMPORTANT: Edit .env file and add your API keys before starting the system"

    # Generate a random secret key
    SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || python3 -c "import secrets; print(secrets.token_hex(32))")

    # Update SECRET_KEY in .env
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/your-super-secret-key-change-this-in-production/$SECRET_KEY/" .env
    else
        sed -i "s/your-super-secret-key-change-this-in-production/$SECRET_KEY/" .env
    fi

    print_success "Generated secure SECRET_KEY"
else
    print_warning ".env file already exists, skipping..."
fi

# Pull Docker images
print_info "Pulling Docker images (this may take a few minutes)..."
if docker-compose pull; then
    print_success "Docker images pulled successfully"
else
    print_error "Failed to pull Docker images"
    exit 1
fi

# Build Docker images
print_info "Building Docker images (this may take a few minutes)..."
if docker-compose build; then
    print_success "Docker images built successfully"
else
    print_error "Failed to build Docker images"
    exit 1
fi

# Start services
print_info "Starting all services..."
if docker-compose up -d; then
    print_success "All services started successfully"
else
    print_error "Failed to start services"
    exit 1
fi

# Wait for services to be healthy
print_info "Waiting for services to be ready..."
sleep 10

# Check if PostgreSQL is ready
print_info "Checking PostgreSQL..."
for i in {1..30}; do
    if docker-compose exec -T postgres pg_isready -U automation_user &> /dev/null; then
        print_success "PostgreSQL is ready"
        break
    fi

    if [ $i -eq 30 ]; then
        print_error "PostgreSQL failed to start"
        exit 1
    fi

    sleep 2
done

# Check if Redis is ready
print_info "Checking Redis..."
if docker-compose exec -T redis redis-cli ping &> /dev/null; then
    print_success "Redis is ready"
else
    print_warning "Redis might not be fully ready yet"
fi

# Initialize database (create tables)
print_info "Initializing database..."
if docker-compose exec -T api python -c "from app.db.base import Base, engine; Base.metadata.create_all(bind=engine)" 2>/dev/null; then
    print_success "Database initialized"
else
    print_warning "Database initialization had some issues, but continuing..."
fi

# Print success message and instructions
echo ""
echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║         🎉  INSTALLATION COMPLETE!  🎉                    ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

print_info "Access your AI Automation Empire:"
echo ""
echo -e "  ${BLUE}🌐 Dashboard:${NC}        http://localhost:3000"
echo -e "  ${BLUE}📚 API Docs:${NC}         http://localhost:8000/docs"
echo -e "  ${BLUE}🌺 Flower Monitor:${NC}   http://localhost:5555"
echo ""

print_info "Useful Commands:"
echo ""
echo "  View logs:           docker-compose logs -f"
echo "  Stop services:       docker-compose down"
echo "  Restart services:    docker-compose restart"
echo "  Update system:       git pull && docker-compose up -d --build"
echo ""

print_warning "Next Steps:"
echo ""
echo "  1. Edit .env file and add your API keys (OpenAI, Anthropic, etc.)"
echo "  2. Restart services: docker-compose restart"
echo "  3. Register your account at http://localhost:8000/docs"
echo "  4. Start scraping and automating!"
echo ""

# Ask if user wants to open browser
read -p "$(echo -e ${BLUE}Open dashboard in browser? [y/N]:${NC} )" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:3000
    elif command -v open &> /dev/null; then
        open http://localhost:3000
    else
        print_info "Please open http://localhost:3000 in your browser"
    fi
fi

print_success "Installation completed successfully!"
echo ""
echo -e "${YELLOW}⭐ If you like this project, please star it on GitHub!${NC}"
echo ""
