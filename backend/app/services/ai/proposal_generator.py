"""
AI-powered proposal generator
"""
from typing import Dict, Any, Optional
from loguru import logger
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from groq import AsyncGroq
from app.core.config import settings


class ProposalGenerator:
    """Generate custom proposals using AI"""

    def __init__(self, model_provider: str = "openai"):
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
            raise ValueError(f"Invalid model provider: {model_provider}")

    async def generate_proposal(
        self,
        opportunity: Dict[str, Any],
        user_profile: Optional[Dict[str, Any]] = None,
        style: str = "professional",
        length: str = "medium",
    ) -> Dict[str, Any]:
        """
        Generate a custom proposal for an opportunity

        Args:
            opportunity: Opportunity details
            user_profile: User's profile, skills, experience
            style: Tone/style (professional, casual, enthusiastic, formal)
            length: Length (short, medium, long)

        Returns:
            Dict with:
                - title: str
                - content: str (full proposal)
                - short_pitch: str (elevator pitch)
                - cover_letter: str
        """
        prompt = self._build_proposal_prompt(opportunity, user_profile, style, length)

        try:
            if self.model_provider == "openai":
                result = await self._generate_with_openai(prompt)
            elif self.model_provider == "anthropic":
                result = await self._generate_with_anthropic(prompt)
            elif self.model_provider == "groq":
                result = await self._generate_with_groq(prompt)
            else:
                result = {}

            return result

        except Exception as e:
            logger.error(f"Error generating proposal: {e}")
            return {}

    def _build_proposal_prompt(
        self,
        opportunity: Dict[str, Any],
        user_profile: Optional[Dict[str, Any]],
        style: str,
        length: str,
    ) -> str:
        """Build proposal generation prompt"""
        title = opportunity.get("title", "")
        description = opportunity.get("description", "")
        budget = opportunity.get("budget", {})
        skills = opportunity.get("skills", [])

        user_context = ""
        if user_profile:
            name = user_profile.get("name", "")
            experience = user_profile.get("experience", "")
            skills_list = user_profile.get("skills", [])
            portfolio = user_profile.get("portfolio_url", "")

            user_context = f"""
Your Profile:
- Name: {name}
- Experience: {experience}
- Skills: {', '.join(skills_list)}
- Portfolio: {portfolio}
"""

        length_guide = {
            "short": "Keep it concise, under 200 words",
            "medium": "Aim for 300-500 words",
            "long": "Detailed proposal, 500-800 words",
        }

        return f"""Generate a winning freelance proposal for the following job opportunity.

Job Title: {title}

Job Description:
{description}

Budget: {budget}
Required Skills: {', '.join(skills)}

{user_context}

Style: {style}
Length: {length_guide.get(length, 'medium')}

Create a proposal that:
1. Addresses the client's pain points directly
2. Shows understanding of their needs
3. Highlights relevant experience/skills
4. Proposes a clear solution
5. Includes a call-to-action
6. Sounds genuine and personalized (NOT generic)

Return your response in this format:

TITLE: [Catchy proposal title]

SHORT_PITCH: [30-50 word elevator pitch]

COVER_LETTER:
[Main proposal content - personalized, solution-focused, engaging]

Make it sound human, not robotic. No fluff, just value.
"""

    async def _generate_with_openai(self, prompt: str) -> Dict[str, Any]:
        """Generate using OpenAI"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert freelance proposal writer with a proven track record of winning high-value projects. Write compelling, personalized proposals.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=1500,
            )

            content = response.choices[0].message.content
            return self._parse_proposal_response(content)

        except Exception as e:
            logger.error(f"OpenAI generation error: {e}")
            return {}

    async def _generate_with_anthropic(self, prompt: str) -> Dict[str, Any]:
        """Generate using Anthropic"""
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.7,
                system="You are an expert freelance proposal writer. Create personalized, winning proposals.",
                messages=[{"role": "user", "content": prompt}],
            )

            content = response.content[0].text
            return self._parse_proposal_response(content)

        except Exception as e:
            logger.error(f"Anthropic generation error: {e}")
            return {}

    async def _generate_with_groq(self, prompt: str) -> Dict[str, Any]:
        """Generate using Groq"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert proposal writer. Create compelling proposals.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=1500,
            )

            content = response.choices[0].message.content
            return self._parse_proposal_response(content)

        except Exception as e:
            logger.error(f"Groq generation error: {e}")
            return {}

    def _parse_proposal_response(self, content: str) -> Dict[str, Any]:
        """Parse AI response into structured format"""
        result = {
            "title": "",
            "short_pitch": "",
            "cover_letter": "",
            "content": content,
        }

        try:
            # Extract title
            if "TITLE:" in content:
                title_start = content.index("TITLE:") + 6
                title_end = content.index("\n", title_start)
                result["title"] = content[title_start:title_end].strip()

            # Extract short pitch
            if "SHORT_PITCH:" in content:
                pitch_start = content.index("SHORT_PITCH:") + 12
                pitch_end = content.index("\n\n", pitch_start)
                result["short_pitch"] = content[pitch_start:pitch_end].strip()

            # Extract cover letter
            if "COVER_LETTER:" in content:
                letter_start = content.index("COVER_LETTER:") + 13
                result["cover_letter"] = content[letter_start:].strip()

        except Exception as e:
            logger.warning(f"Error parsing proposal sections: {e}")
            # If parsing fails, use full content as cover letter
            result["cover_letter"] = content

        return result

    async def generate_follow_up(
        self,
        original_proposal: str,
        days_since_sent: int,
        follow_up_number: int = 1,
    ) -> str:
        """Generate follow-up message"""
        prompt = f"""Generate a professional follow-up message for a proposal sent {days_since_sent} days ago.

Original Proposal:
{original_proposal[:500]}...

This is follow-up #{follow_up_number}.

Requirements:
- Keep it brief (under 100 words)
- Friendly but professional
- Add value (don't just ask "did you see my proposal?")
- Include a soft call-to-action
- Show continued interest

Return only the follow-up message, no labels."""

        try:
            if self.model_provider == "openai":
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=300,
                )
                return response.choices[0].message.content

            elif self.model_provider == "anthropic":
                response = await self.client.messages.create(
                    model=self.model,
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}],
                )
                return response.content[0].text

            elif self.model_provider == "groq":
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=300,
                )
                return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error generating follow-up: {e}")
            return ""
