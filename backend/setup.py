from setuptools import setup, find_packages

# Read the contents of README file
from pathlib import Path
this_directory = Path(__file__).parent.parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="ai-automation-empire",
    version="1.0.0",
    author="AI Automation Empire Team",
    author_email="support@aiautomationempire.com",
    description="The Ultimate Web Scraping & Automation Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/profmohamed/AI-Automation-Empire",
    project_urls={
        "Bug Tracker": "https://github.com/profmohamed/AI-Automation-Empire/issues",
        "Documentation": "https://github.com/profmohamed/AI-Automation-Empire/blob/main/README.md",
        "Source Code": "https://github.com/profmohamed/AI-Automation-Empire",
        "Changelog": "https://github.com/profmohamed/AI-Automation-Empire/blob/main/CHANGELOG.md",
    },
    packages=find_packages(exclude=["tests", "tests.*", "docs", "docs.*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: FastAPI",
        "Framework :: Celery",
    ],
    python_requires=">=3.11",
    install_requires=[
        "fastapi>=0.109.0",
        "uvicorn[standard]>=0.27.0",
        "sqlalchemy>=2.0.25",
        "celery>=5.3.6",
        "redis>=5.0.1",
        "playwright>=1.41.2",
        "openai>=1.10.0",
        "anthropic>=0.18.1",
        "pydantic>=2.5.3",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "loguru>=0.7.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.4",
            "pytest-asyncio>=0.23.3",
            "black>=24.1.0",
            "flake8>=7.0.0",
        ],
        "all": [
            "sentence-transformers>=2.3.1",
            "stripe>=8.2.0",
            "flower>=2.0.1",
            "sentry-sdk>=1.40.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-empire=app.cli:main",
            "ai-empire-api=app.main:start",
            "ai-empire-worker=app.workers.celery_app:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "automation",
        "scraping",
        "ai",
        "web-scraping",
        "freelance",
        "opportunities",
        "playwright",
        "fastapi",
        "celery",
        "ai-agent",
        "outreach",
        "proposals",
    ],
)
