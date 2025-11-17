"""
Outreach campaigns API endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.db.base import get_db
from app.models.outreach import OutreachCampaign
from app.models.user import User
from app.api.deps.auth import get_current_user

router = APIRouter()


class CampaignResponse(BaseModel):
    id: int
    name: str
    channel: str
    status: str
    total_sent: int
    total_replied: int

    class Config:
        from_attributes = True


@router.get("/", response_model=List[CampaignResponse])
async def list_campaigns(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List user's campaigns"""
    campaigns = db.query(OutreachCampaign).filter(OutreachCampaign.user_id == current_user.id).all()
    return campaigns
