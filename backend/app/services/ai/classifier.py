"""
AI-powered opportunity classifier
"""
import json
from typing import Dict, Any, List, Optional
from loguru import logger
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from groq import AsyncGroq
from app.core.config import settings


class OpportunityClassifier:
    """Classify and score opportunities using AI"""

    def __init__(self, model_provider: str = "openai"):
        """
        Initialize classifier

        Args:
            model_provider: AI provider (openai, anthropic, groq)
        """
        self.model_provider = model_provider

        if model_provider == "openai" and settings.OPENAI_API_KEY:
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = settings.OPENAI_MODEL
        elif model_provider == "anthropic" and settings.ANTHROPIC_API_KEY:
            self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
            self.model = settings.ANTHROPIC_MODEL
        elif model_provider == "groq" and settings.GROQ_API_KEY:
            self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
            self.model = settings.GROQ_MODEL
        else:
            raise ValueError(f"Invalid model provider or missing API key: {model_provider}")

    async def classify_opportunity(self, opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify opportunity using AI

        Returns:
            Dict with classification results:
                - category: str
                - difficulty: str (easy, medium, hard, expert)
                - ai_score: float (0-100)
                - keywords: List[str]
                - pain_points: List[str]
                - required_skills: List[str]
                - sentiment_score: float (-1 to 1)
                - summary: str
        """
        title = opportunity.get("title", "")
        description = opportunity.get("description", "")

        prompt = self._build_classification_prompt(title, description)

        try:
            if self.model_provider == "openai":
                result = await self._classify_with_openai(prompt)
            elif self.model_provider == "anthropic":
                result = await self._classify_with_anthropic(prompt)
            elif self.model_provider == "groq":
                result = await self._classify_with_groq(prompt)
            else:
                result = {}

            return result

        except Exception as e:
            logger.error(f"Error classifying opportunity: {e}")
            return {}

    def _build_classification_prompt(self, title: str, description: str) -> str:
        """Build classification prompt"""
        return f"""Analyze the following job opportunity and provide a detailed classification.

Title: {title}

Description: {description}

Provide your analysis in the following JSON format:
{{
    "category": "category name (e.g., web-development, design, marketing, data-science, etc.)",
    "difficulty": "easy|medium|hard|expert",
    "ai_score": 0-100 (higher score = better opportunity),
    "keywords": ["keyword1", "keyword2", ...],
    "pain_points": ["pain point 1", "pain point 2", ...],
    "required_skills": ["skill1", "skill2", ...],
    "sentiment_score": -1.0 to 1.0 (negative to positive),
    "summary": "Brief 2-3 sentence summary of the opportunity"
}}

Consider these factors when scoring:
- Budget/payment potential
- Client quality indicators
- Project clarity
- Realistic requirements
- Growth potential
- Time commitment vs. reward

Return ONLY valid JSON, no additional text."""

    async def _classify_with_openai(self, prompt: str) -> Dict[str, Any]:
        """Classify using OpenAI"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert job opportunity analyzer. Analyze opportunities and return structured JSON data.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                response_format={"type": "json_object"},
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            logger.error(f"OpenAI classification error: {e}")
            return {}

    async def _classify_with_anthropic(self, prompt: str) -> Dict[str, Any]:
        """Classify using Anthropic Claude"""
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                temperature=0.3,
                system="You are an expert job opportunity analyzer. Analyze opportunities and return structured JSON data.",
                messages=[{"role": "user", "content": prompt}],
            )

            content = response.content[0].text
            # Extract JSON from response
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end > start:
                result = json.loads(content[start:end])
                return result

            return {}

        except Exception as e:
            logger.error(f"Anthropic classification error: {e}")
            return {}

    async def _classify_with_groq(self, prompt: str) -> Dict[str, Any]:
        """Classify using Groq"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert job opportunity analyzer. Return only valid JSON.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                response_format={"type": "json_object"},
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            logger.error(f"Groq classification error: {e}")
            return {}

    async def batch_classify(self, opportunities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Classify multiple opportunities"""
        results = []
        for opp in opportunities:
            result = await self.classify_opportunity(opp)
            results.append(result)
        return results
