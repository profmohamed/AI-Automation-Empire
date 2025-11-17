# Contributing to AI Automation Empire

Thank you for your interest in contributing! We welcome contributions from the community.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/ai-automation-empire.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit: `git commit -m "Add: your feature description"`
7. Push: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/ai-automation-empire.git
cd ai-automation-empire

# Install dependencies
./install.sh

# Start development environment
docker-compose up -d
```

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Write docstrings for functions and classes
- Format with Black: `black .`
- Lint with flake8: `flake8 .`

### TypeScript/React
- Follow Airbnb style guide
- Use TypeScript for type safety
- Format with Prettier
- Lint with ESLint

## Testing

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

## Commit Messages

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

Example: `feat: add LinkedIn scraper with anti-bot protection`

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Give constructive feedback
- Focus on the code, not the person

## Questions?

Open an issue or join our Discord community.

Thank you for contributing! 🎉
