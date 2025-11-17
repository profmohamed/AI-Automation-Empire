"""
Proposals API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.db.base import get_db
from app.models.proposal import Proposal
from app.models.user import User
from app.api.deps.auth import get_current_user

router = APIRouter()


class ProposalResponse(BaseModel):
    id: int
    title: str
    content: str
    status: str
    opportunity_id: int = None

    class Config:
        from_attributes = True


@router.get("/", response_model=List[ProposalResponse])
async def list_proposals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List user's proposals"""
    proposals = db.query(Proposal).filter(Proposal.user_id == current_user.id).all()
    return proposals


@router.get("/{proposal_id}", response_model=ProposalResponse)
async def get_proposal(
    proposal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get single proposal"""
    proposal = db.query(Proposal).filter(
        Proposal.id == proposal_id,
        Proposal.user_id == current_user.id
    ).first()

    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    return proposal
