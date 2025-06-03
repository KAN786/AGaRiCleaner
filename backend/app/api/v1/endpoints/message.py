# backend/app/api/v1/endpoints/message.py
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from datetime import datetime
from app.models import Message
from app.database import get_session
from app.schemas.message_schemas import MessageGet


router = APIRouter()

@router.get("/{server_id}/{system_id}")
def get_messages(server_id: str, system_id: str, session: Session = Depends(get_session)):
    messages = session.exec(
        select(Message).where(
            (Message.server_id == server_id) & (Message.system_id == system_id)
        )
    ).all()
    return messages

@router.post("/")
def create_message(session: Session = Depends(get_session)):
    msg = Message(
        user_id=1,
        date_sent=datetime.now(),
        word_count=10,
        first_filter_passed=False,
        second_filter_checked=True,
        second_filter_score=0.8,
        final_toxic=True
    )
    session.add(msg)
    session.commit()
    session.refresh(msg)
    return msg
