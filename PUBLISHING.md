# 📦 PyPI Package Publishing Guide

This guide explains how to publish AI Automation Empire to PyPI.

## Prerequisites

1. **PyPI Account**: Create accounts on:
   - PyPI: https://pypi.org/account/register/
   - Test PyPI: https://test.pypi.org/account/register/

2. **API Tokens**: Generate API tokens for automated publishing:
   - Go to Account Settings → API tokens
   - Create token with upload permissions
   - Save the token securely

3. **GitHub Secrets**: Add the following secrets to your GitHub repository:
   - Go to Settings → Secrets and variables → Actions
   - Add `PYPI_API_TOKEN` with your PyPI token

## Manual Publishing (First Time)

### 1. Install Build Tools

```bash
cd backend
pip install build twine
```

### 2. Build the Package

```bash
python -m build
```

This creates:
- `dist/ai_automation_empire-1.0.0.tar.gz` (source distribution)
- `dist/ai_automation_empire-1.0.0-py3-none-any.whl` (wheel distribution)

### 3. Check the Package

```bash
twine check dist/*
```

### 4. Test Upload (Optional but Recommended)

```bash
# Upload to Test PyPI first
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ ai-automation-empire
```

### 5. Upload to PyPI

```bash
twine upload dist/*
```

## Automated Publishing with GitHub Actions

The repository includes GitHub Actions workflows for automated publishing.

### Creating a Release

1. **Update Version**:
   - Update version in `backend/pyproject.toml`
   - Update version in `backend/setup.py`
   - Update version in `backend/app/__version__.py`
   - Add changelog entry in `CHANGELOG.md`

2. **Commit Changes**:
```bash
git add -A
git commit -m "chore: bump version to 1.1.0"
git push
```

3. **Create Git Tag**:
```bash
git tag v1.1.0
git push origin v1.1.0
```

4. **Automatic Process**:
   - GitHub Actions detects the tag
   - Builds the package
   - Creates GitHub Release with changelog
   - Publishes to PyPI automatically

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
  - **MAJOR**: Breaking changes
  - **MINOR**: New features (backward compatible)
  - **PATCH**: Bug fixes

Examples:
- `1.0.0` - Initial release
- `1.0.1` - Bug fix
- `1.1.0` - New feature
- `2.0.0` - Breaking change

## Release Checklist

Before creating a release:

- [ ] All tests pass (`pytest`)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in all files
- [ ] README.md reflects new features
- [ ] Dependencies updated in requirements.txt
- [ ] Docker images tested
- [ ] Installation script tested

## Package Structure

```
backend/
├── setup.py              # Package configuration
├── pyproject.toml        # Modern package configuration
├── MANIFEST.in           # Files to include in package
├── README.md             # Package documentation
├── LICENSE               # MIT License
└── app/                  # Package code
    ├── __init__.py
    ├── __version__.py    # Version info
    ├── cli.py            # CLI entry point
    └── ...
```

## Installation Methods

After publishing, users can install via:

### From PyPI
```bash
pip install ai-automation-empire
```

### With Optional Dependencies
```bash
# Install with all features
pip install ai-automation-empire[all]

# Install with specific features
pip install ai-automation-empire[ai,monitoring]
```

### From GitHub
```bash
pip install git+https://github.com/profmohamed/AI-Automation-Empire.git
```

### Development Mode
```bash
git clone https://github.com/profmohamed/AI-Automation-Empire.git
cd AI-Automation-Empire/backend
pip install -e ".[dev]"
```

## CLI Commands

After installation, users can use CLI commands:

```bash
# Show version
ai-empire version

# Start API server
ai-empire start-api --host 0.0.0.0 --port 8000

# Start Celery worker
ai-empire start-worker --concurrency 4

# Create admin user
ai-empire create-admin --email admin@example.com --username admin --password secure123

# Database commands
ai-empire db init
ai-empire db migrate
ai-empire db upgrade
```

## Package Metadata

The package includes rich metadata:

- **Keywords**: automation, scraping, ai, web-scraping, freelance
- **Classifiers**: Production/Stable, Python 3.11+, MIT License
- **Project URLs**: Homepage, Documentation, Bug Tracker, Changelog
- **Entry Points**: CLI commands
- **Dependencies**: All required packages
- **Optional Dependencies**: Grouped by feature

## Troubleshooting

### Build Errors

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Rebuild
python -m build
```

### Upload Errors

```bash
# Check package
twine check dist/*

# Verify credentials
twine upload --repository testpypi dist/*
```

### Version Conflicts

If version already exists on PyPI:
- Cannot re-upload same version
- Increment version and rebuild
- Delete local dist/ and rebuild

## Best Practices

1. **Test First**: Always test on Test PyPI first
2. **Clean Builds**: Remove old dist/ before building
3. **Check Package**: Run `twine check` before uploading
4. **Tag Releases**: Use git tags for version control
5. **Document Changes**: Update CHANGELOG.md
6. **Semantic Versioning**: Follow semver strictly
7. **GitHub Releases**: Use GitHub Releases for visibility

## Support

- PyPI Package: https://pypi.org/project/ai-automation-empire/
- GitHub Issues: https://github.com/profmohamed/AI-Automation-Empire/issues
- Documentation: https://github.com/profmohamed/AI-Automation-Empire/blob/main/README.md

## Example: Complete Release Process

```bash
# 1. Update version everywhere
# Edit: pyproject.toml, setup.py, __version__.py, CHANGELOG.md

# 2. Commit changes
git add -A
git commit -m "chore: release version 1.1.0"
git push

# 3. Create and push tag
git tag v1.1.0
git push origin v1.1.0

# 4. GitHub Actions automatically:
#    - Builds package
#    - Creates GitHub Release
#    - Publishes to PyPI

# 5. Verify
pip install --upgrade ai-automation-empire
ai-empire version
```

## Monitoring

After publishing:

1. **Check PyPI**: https://pypi.org/project/ai-automation-empire/
2. **Verify Installation**: `pip install ai-automation-empire`
3. **Monitor Downloads**: PyPI provides download statistics
4. **Watch Issues**: GitHub Issues for bug reports

---

Happy publishing! 🚀
