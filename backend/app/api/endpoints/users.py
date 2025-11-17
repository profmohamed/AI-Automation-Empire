"""
Users API endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.base import get_db
from app.models.user import User
from app.api.deps.auth import get_current_user

router = APIRouter()


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str = None
    role: str
    is_active: bool

    class Config:
        from_attributes = True


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """Get current user info"""
    return current_user
