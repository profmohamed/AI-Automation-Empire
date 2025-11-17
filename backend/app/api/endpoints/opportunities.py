"""
Opportunities API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.db.base import get_db
from app.models.opportunity import Opportunity
from app.models.user import User
from app.api.deps.auth import get_current_user

router = APIRouter()


class OpportunityResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    platform: Optional[str]
    ai_score: Optional[float]
    category: Optional[str]
    status: str

    class Config:
        from_attributes = True


@router.get("/", response_model=List[OpportunityResponse])
async def list_opportunities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    platform: Optional[str] = None,
    min_score: Optional[float] = Query(None, ge=0, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List user's opportunities"""
    query = db.query(Opportunity).filter(Opportunity.user_id == current_user.id)

    if platform:
        query = query.filter(Opportunity.source_platform == platform)

    if min_score:
        query = query.filter(Opportunity.ai_score >= min_score)

    opportunities = query.order_by(Opportunity.created_at.desc()).offset(skip).limit(limit).all()

    return opportunities


@router.get("/{opportunity_id}", response_model=OpportunityResponse)
async def get_opportunity(
    opportunity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get single opportunity"""
    opportunity = db.query(Opportunity).filter(
        Opportunity.id == opportunity_id,
        Opportunity.user_id == current_user.id
    ).first()

    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    return opportunity


@router.delete("/{opportunity_id}")
async def delete_opportunity(
    opportunity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete opportunity"""
    opportunity = db.query(Opportunity).filter(
        Opportunity.id == opportunity_id,
        Opportunity.user_id == current_user.id
    ).first()

    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    db.delete(opportunity)
    db.commit()

    return {"message": "Opportunity deleted successfully"}
