# backend/app/api/v1/endpoints/message.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime
from app.models import Message, User
from app.api.v1.services.services import UserServices, get_agaricleaner_result, get_server_average_honor_score
from app.database import get_session
from fastapi import Request

import random
router = APIRouter()


@router.post("/{server_id}/{system_id}")
async def eval_message(
    server_id: str,
    system_id: str, 
    message: str, 
    request: Request,
    session: Session = Depends(get_session)
    ):

    
    date_sent: datetime = datetime.now()
    word_count: int = len(message.split())
    score: float
    is_toxic: bool



    # 계산용 객체에 넣기
    userServices = UserServices(system_id, server_id, session)
    server_average_honor_score = get_server_average_honor_score(server_id, session)


    if(
        False
        # 첫번째 필터에서 통과하지 못한 경우. 노골적인 욕설이라 1점
    ):
        score = 1
        is_toxic = True
    else:
        score = userServices.getBayesianHonorLevel(server_average_honor_score)
        p = (1 - score) * 1

        # 필터링 당첨
        if(random.random() < p):
            result = get_agaricleaner_result(request.app.state.client, message)

            result_label = result[0]["label"]
            score = result[0]["score"]

            if (
                result_label
                # 부정적일 시
            ):
                is_toxic = True
                userServices.update_honor((True, score))
            else:
                is_toxic = False
                userServices.update_honor((False, score))
        # 그냥 넘어감. 테스트 안했으니 0.5점
        else:
            is_toxic = False
            score = 0.5
            pass

        
    result_message = Message(
        user_id=userServices.user.id,
        date_sent=date_sent,
        word_count=word_count,
        score=score,
        is_toxic=is_toxic
    )
    session.add(result_message)
    session.commit()
    session.refresh(result_message)
    return result_message


