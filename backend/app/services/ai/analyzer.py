"""
Opportunity analyzer - extract insights from opportunities
"""
from typing import Dict, Any, List
from loguru import logger
import re


class OpportunityAnalyzer:
    """Analyze opportunities and extract insights"""

    def analyze_budget(self, budget_text: str) -> Dict[str, Any]:
        """Extract budget information"""
        result = {
            "min": None,
            "max": None,
            "currency": "USD",
            "is_hourly": False,
        }

        try:
            # Check if hourly
            if any(word in budget_text.lower() for word in ["hour", "/hr", "hourly"]):
                result["is_hourly"] = True

            # Extract currency
            if "$" in budget_text or "usd" in budget_text.lower():
                result["currency"] = "USD"
            elif "€" in budget_text or "eur" in budget_text.lower():
                result["currency"] = "EUR"
            elif "£" in budget_text or "gbp" in budget_text.lower():
                result["currency"] = "GBP"

            # Extract numbers
            numbers = re.findall(r"[\d,]+(?:\.\d+)?", budget_text.replace(",", ""))
            numbers = [float(n) for n in numbers]

            if len(numbers) >= 2:
                result["min"] = min(numbers)
                result["max"] = max(numbers)
            elif len(numbers) == 1:
                result["min"] = numbers[0]
                result["max"] = numbers[0]

        except Exception as e:
            logger.warning(f"Error parsing budget: {e}")

        return result

    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        # Common tech and business keywords
        keywords = set()

        tech_keywords = [
            "python", "javascript", "react", "node", "django", "flask", "fastapi",
            "vue", "angular", "typescript", "java", "c++", "rust", "go", "php",
            "sql", "nosql", "mongodb", "postgresql", "mysql", "redis", "docker",
            "kubernetes", "aws", "azure", "gcp", "ai", "ml", "machine learning",
            "deep learning", "nlp", "computer vision", "data science", "analytics",
            "frontend", "backend", "fullstack", "mobile", "ios", "android",
            "design", "ui", "ux", "figma", "sketch", "photoshop", "illustrator",
            "marketing", "seo", "content", "copywriting", "social media",
        ]

        text_lower = text.lower()
        for keyword in tech_keywords:
            if keyword in text_lower:
                keywords.add(keyword)

        return list(keywords)

    def calculate_complexity_score(self, opportunity: Dict[str, Any]) -> float:
        """Calculate complexity score (0-100)"""
        score = 50.0  # Base score

        # Adjust based on description length
        description = opportunity.get("description", "")
        if len(description) > 1000:
            score += 10
        elif len(description) < 200:
            score -= 10

        # Adjust based on required skills
        skills = opportunity.get("skills", [])
        if len(skills) > 5:
            score += 15
        elif len(skills) > 10:
            score += 25

        # Adjust based on budget
        budget = opportunity.get("budget", {})
        budget_max = budget.get("max", 0)
        if budget_max > 10000:
            score += 20
        elif budget_max > 5000:
            score += 10

        # Cap between 0-100
        return max(0, min(100, score))

    def detect_urgency(self, text: str) -> bool:
        """Detect if opportunity is urgent"""
        urgency_keywords = [
            "urgent", "asap", "immediately", "rush", "quick", "fast",
            "deadline", "today", "this week", "emergency",
        ]

        text_lower = text.lower()
        return any(keyword in text_lower for keyword in urgency_keywords)

    def extract_contact_info(self, text: str) -> Dict[str, Any]:
        """Extract contact information from text"""
        contact = {
            "emails": [],
            "phones": [],
            "urls": [],
        }

        # Extract emails
        emails = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text)
        contact["emails"] = list(set(emails))

        # Extract phone numbers
        phones = re.findall(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b", text)
        contact["phones"] = list(set(phones))

        # Extract URLs
        urls = re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", text)
        contact["urls"] = list(set(urls))

        return contact
