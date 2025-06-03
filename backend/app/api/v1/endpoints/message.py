# backend/app/api/v1/endpoints/message.py
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from datetime import datetime
from app.models import Message, User
from app.api.v1.services.userServices import UserServices
from app.database import get_session

import random
router = APIRouter()

# @router.get("/{server_id}/{system_id}")
# def get_messages(server_id: str, system_id: str, session: Session = Depends(get_session)):
#     messages = session.exec(
#         select(Message).where(
#             (Message.server_id == server_id) & (Message.system_id == system_id)
#         )
#     ).all()
#     return messages


@router.get("/{user_server_id}/{user_system_id}")
def eval_message(
    user_server_id: str,
    user_system_id: str, 
    message: str, 
    session: Session = Depends(get_session)):

    

    user_id: int 
    date_sent: datetime = datetime.now()
    word_count: int = len(message.split())
    score: float
    is_toxic: bool

    # db에서 유저 가져오기
    user = session.exec(
        select(User).where(
            (User.server_id == user_server_id) & 
            (User.system_id == user_system_id)
        )
    ).first()

    if not user:
        # 400 에러 반환
        raise HTTPException(status_code=400, detail="User not found")


    user_id = user.id


    # 유저의 메세지 목록 가져오기
    messages = session.exec(
        select(Message).where(
            (Message.user_id == user.id)
        )
    ).all()
    messageEvalList = [(msg.is_toxic, msg.score) for msg in messages]

    # 계산용 객체에 넣기
    userServices = UserServices(user.honor_score, messageEvalList)


    if(
        # 첫번째 필터에서 통과하지 못한 경우. 노골적인 욕설이라 1점
    ):
        score = 1
        is_toxic = True
    else:
        score = userServices.getBayesianHonorLevel()
        p = (1 - score) * 1

        # 필터링 당첨
        if(random.random() < p):
            # do test
            if (
                # 부정적일 시
            ):
                is_toxic = True
                userServices.update_honor((True, test_score))
            else:
                is_toxic = False
                userServices.update_honor((False, test_score))
        # 그냥 넘어감. 테스트 안했으니 0.5점
        else:
            is_toxic = False
            score = 0.5
            pass

        
    result_message = Message(
        user_id=user_id,
        date_sent=date_sent,
        word_count=word_count,
        score=score,
        is_toxic=is_toxic
    )
    session.add(result_message)
    session.commit()
    session.refresh(result_message)
    return result_message

   

# @router.post("/")
# def create_message(session: Session = Depends(get_session)):
#     msg = Message(
#         user_id=1,
#         date_sent=datetime.now(),
#         word_count=10,
#         first_filter_passed=False,
#         second_filter_checked=True,
#         second_filter_score=0.8,
#         final_toxic=True
#     )
#     session.add(msg)
#     session.commit()
#     session.refresh(msg)
#     return msg
