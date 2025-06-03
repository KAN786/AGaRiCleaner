from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.user_service import get_user_email_domain

usersRouter = APIRouter()

@usersRouter.get("/{user_id}/honorLevel")
def get_email_domain(user_id: int, db: Session = Depends(get_db)):
    domain = get_user_email_domain(db, user_id)
    return {"honorLevel": honorLevel}

@usersRouter.get("/{user_id}/evalResult")
def get_user_eval_result(user_id: int, 
                          message: str = Query(...),
                          db: Session = Depends(get_db)):
    result = get_user_eval_result(db, user_id)
    return {"result": result}

