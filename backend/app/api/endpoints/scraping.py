"""
Scraping job API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from app.db.base import get_db
from app.models.scraping import ScrapingJob, ScrapingPlatform
from app.models.user import User
from app.api.deps.auth import get_current_user

router = APIRouter()


class ScrapingJobCreate(BaseModel):
    name: str
    platform: str
    keywords: List[str]
    max_pages: int = 5
    max_items: int = 100


class ScrapingJobResponse(BaseModel):
    id: int
    name: str
    platform: str
    status: str
    total_items_scraped: int
    is_active: bool

    class Config:
        from_attributes = True


@router.post("/jobs", response_model=ScrapingJobResponse, status_code=201)
async def create_scraping_job(
    job_data: ScrapingJobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create new scraping job"""
    job = ScrapingJob(
        user_id=current_user.id,
        name=job_data.name,
        platform=job_data.platform,
        target_url=f"https://{job_data.platform}.com",
        scraping_config={"keywords": job_data.keywords},
        max_pages=job_data.max_pages,
        max_items=job_data.max_items,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


@router.get("/jobs", response_model=List[ScrapingJobResponse])
async def list_scraping_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List user's scraping jobs"""
    jobs = db.query(ScrapingJob).filter(ScrapingJob.user_id == current_user.id).all()
    return jobs


@router.post("/jobs/{job_id}/run")
async def run_scraping_job(
    job_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Run scraping job"""
    job = db.query(ScrapingJob).filter(
        ScrapingJob.id == job_id,
        ScrapingJob.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Queue scraping task (would be Celery task in production)
    # background_tasks.add_task(run_scraper_task, job_id)

    return {"message": "Scraping job queued", "job_id": job_id}


@router.delete("/jobs/{job_id}")
async def delete_scraping_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete scraping job"""
    job = db.query(ScrapingJob).filter(
        ScrapingJob.id == job_id,
        ScrapingJob.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(job)
    db.commit()

    return {"message": "Job deleted"}
