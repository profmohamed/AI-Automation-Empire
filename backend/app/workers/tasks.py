"""
Celery tasks for async processing
"""
import asyncio
from typing import Dict, Any
from loguru import logger
from app.workers.celery_app import celery_app
from app.services.scrapers.upwork_scraper import UpworkScraper
from app.services.scrapers.linkedin_scraper import LinkedInScraper
from app.services.ai.ai_agent import AIAgent
from app.services.ai.proposal_generator import ProposalGenerator
from app.db.base import SessionLocal
from app.models.opportunity import Opportunity
from app.models.scraping import ScrapingJob, ScrapingLog, ScrapingStatus
from datetime import datetime


@celery_app.task(name="scrape_upwork_jobs")
def scrape_upwork_jobs(job_id: int, keywords: str, max_pages: int = 5):
    """Scrape Upwork jobs"""
    db = SessionLocal()

    try:
        # Update job status
        job = db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()
        if not job:
            return {"error": "Job not found"}

        job.status = ScrapingStatus.RUNNING
        db.commit()

        # Create scraping log
        log = ScrapingLog(job_id=job_id, status=ScrapingStatus.RUNNING)
        db.add(log)
        db.commit()

        # Run scraper
        scraper = UpworkScraper(headless=True)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        results = loop.run_until_complete(
            scraper.scrape_jobs(keywords=keywords, max_pages=max_pages)
        )
        loop.run_until_complete(scraper.close())

        # Save opportunities
        for result in results:
            opportunity = Opportunity(
                user_id=job.user_id,
                title=result.get("title"),
                description=result.get("description"),
                source_url=result.get("url"),
                source_platform="upwork",
                raw_data=result,
            )
            db.add(opportunity)

        # Update job and log
        job.status = ScrapingStatus.COMPLETED
        job.total_items_scraped += len(results)
        job.total_runs += 1

        log.status = ScrapingStatus.COMPLETED
        log.items_found = len(results)
        log.completed_at = datetime.utcnow()

        db.commit()

        logger.info(f"Scraped {len(results)} jobs from Upwork")

        return {"success": True, "items_scraped": len(results)}

    except Exception as e:
        logger.error(f"Error scraping Upwork jobs: {e}")
        if job:
            job.status = ScrapingStatus.FAILED
        if log:
            log.status = ScrapingStatus.FAILED
            log.error_message = str(e)
        db.commit()
        return {"error": str(e)}

    finally:
        db.close()


@celery_app.task(name="process_opportunity_with_ai")
def process_opportunity_with_ai(opportunity_id: int):
    """Process opportunity with AI agent"""
    db = SessionLocal()

    try:
        opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
        if not opportunity:
            return {"error": "Opportunity not found"}

        # Convert to dict
        opp_data = {
            "title": opportunity.title,
            "description": opportunity.description,
            "platform": opportunity.source_platform,
        }

        # Process with AI
        agent = AIAgent()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        result = loop.run_until_complete(
            agent.process_opportunity(opp_data, {})
        )

        # Update opportunity
        opportunity.ai_score = result.get("ai_score")
        opportunity.category = result.get("category")
        opportunity.difficulty = result.get("difficulty")
        opportunity.keywords = result.get("keywords")
        opportunity.pain_points = result.get("pain_points")

        db.commit()

        logger.info(f"Processed opportunity {opportunity_id} with AI")

        return {"success": True, "ai_score": result.get("ai_score")}

    except Exception as e:
        logger.error(f"Error processing opportunity: {e}")
        return {"error": str(e)}

    finally:
        db.close()


@celery_app.task(name="generate_proposal")
def generate_proposal(opportunity_id: int, user_id: int):
    """Generate proposal for opportunity"""
    db = SessionLocal()

    try:
        opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
        if not opportunity:
            return {"error": "Opportunity not found"}

        opp_data = {
            "title": opportunity.title,
            "description": opportunity.description,
        }

        # Generate proposal
        generator = ProposalGenerator()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        proposal = loop.run_until_complete(
            generator.generate_proposal(opp_data, {})
        )

        logger.info(f"Generated proposal for opportunity {opportunity_id}")

        return {"success": True, "proposal": proposal}

    except Exception as e:
        logger.error(f"Error generating proposal: {e}")
        return {"error": str(e)}

    finally:
        db.close()


@celery_app.task(name="autonomous_agent_loop")
def autonomous_agent_loop():
    """Autonomous agent that continuously finds and processes opportunities"""
    db = SessionLocal()

    try:
        # Find unprocessed opportunities
        opportunities = db.query(Opportunity).filter(
            Opportunity.ai_score == None
        ).limit(10).all()

        for opp in opportunities:
            # Process with AI
            process_opportunity_with_ai.delay(opp.id)

        logger.info(f"Autonomous agent processed {len(opportunities)} opportunities")

        return {"success": True, "processed": len(opportunities)}

    except Exception as e:
        logger.error(f"Error in autonomous agent loop: {e}")
        return {"error": str(e)}

    finally:
        db.close()
