from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.user_service import get_user_email_domain

router = APIRouter()

@router.get("/{user_id}/email-domain")
def get_email_domain(user_id: int, db: Session = Depends(get_db)):
    domain = get_user_email_domain(db, user_id)
    return {"email_domain": domain}