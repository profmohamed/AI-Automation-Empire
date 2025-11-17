"""
Autonomous AI Agent - The brain of the automation system
"""
import asyncio
from typing import Dict, Any, List
from loguru import logger
from datetime import datetime
from app.services.ai.classifier import OpportunityClassifier
from app.services.ai.proposal_generator import ProposalGenerator
from app.services.ai.analyzer import OpportunityAnalyzer


class AIAgent:
    """Autonomous agent that orchestrates the entire automation pipeline"""

    def __init__(self, model_provider: str = "openai"):
        self.classifier = OpportunityClassifier(model_provider)
        self.proposal_generator = ProposalGenerator(model_provider)
        self.analyzer = OpportunityAnalyzer()

    async def process_opportunity(
        self,
        opportunity: Dict[str, Any],
        user_profile: Dict[str, Any],
        auto_generate_proposal: bool = True,
    ) -> Dict[str, Any]:
        """
        Full processing pipeline for a single opportunity

        1. Analyze & extract insights
        2. Classify using AI
        3. Score & rank
        4. Generate proposal if high-quality
        5. Return enriched opportunity
        """
        logger.info(f"Processing opportunity: {opportunity.get('title', 'Unknown')}")

        # Step 1: Analyze
        description = opportunity.get("description", "")
        title = opportunity.get("title", "")
        combined_text = f"{title} {description}"

        opportunity["keywords"] = self.analyzer.extract_keywords(combined_text)
        opportunity["is_urgent"] = self.analyzer.detect_urgency(combined_text)
        opportunity["contact_info"] = self.analyzer.extract_contact_info(description)

        # Step 2: Classify with AI
        classification = await self.classifier.classify_opportunity(opportunity)
        opportunity.update({
            "category": classification.get("category"),
            "difficulty": classification.get("difficulty"),
            "ai_score": classification.get("ai_score"),
            "pain_points": classification.get("pain_points", []),
            "required_skills": classification.get("required_skills", []),
            "sentiment_score": classification.get("sentiment_score"),
            "ai_summary": classification.get("summary"),
        })

        # Step 3: Calculate complexity
        opportunity["complexity_score"] = self.analyzer.calculate_complexity_score(opportunity)

        # Step 4: Generate proposal if high-quality and auto-generate is enabled
        if auto_generate_proposal and opportunity.get("ai_score", 0) >= 70:
            logger.info("High-quality opportunity detected, generating proposal...")
            proposal = await self.proposal_generator.generate_proposal(
                opportunity, user_profile
            )
            opportunity["generated_proposal"] = proposal

        opportunity["processed_at"] = datetime.utcnow().isoformat()

        return opportunity

    async def process_batch(
        self,
        opportunities: List[Dict[str, Any]],
        user_profile: Dict[str, Any],
        auto_generate_proposal: bool = True,
    ) -> List[Dict[str, Any]]:
        """Process multiple opportunities in parallel"""
        tasks = [
            self.process_opportunity(opp, user_profile, auto_generate_proposal)
            for opp in opportunities
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions
        processed = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error processing opportunity {i}: {result}")
            else:
                processed.append(result)

        return processed

    async def decide_next_action(self, opportunity: Dict[str, Any]) -> str:
        """
        Decide what action to take next for an opportunity

        Returns:
            - "contact": Reach out to client
            - "wait": Wait for more info
            - "ignore": Not a good fit
            - "research": Need more research
        """
        ai_score = opportunity.get("ai_score", 0)
        sentiment = opportunity.get("sentiment_score", 0)
        budget_info = opportunity.get("budget", {})

        # High-quality opportunity
        if ai_score >= 80 and sentiment > 0:
            return "contact"

        # Medium quality with good budget
        elif ai_score >= 60 and budget_info.get("max", 0) > 1000:
            return "contact"

        # Needs more info
        elif ai_score >= 50 and not budget_info.get("min"):
            return "research"

        # Low quality
        elif ai_score < 40:
            return "ignore"

        # Default: wait
        else:
            return "wait"

    async def rank_opportunities(
        self, opportunities: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Rank opportunities by quality score"""
        return sorted(
            opportunities,
            key=lambda x: x.get("ai_score", 0),
            reverse=True,
        )
