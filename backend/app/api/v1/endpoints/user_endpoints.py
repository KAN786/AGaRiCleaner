# backend/app/api/v1/endpoints/message.py
from fastapi import APIRouter, Request, HTTPException
from datetime import datetime
from app.models import Message, User
from app.database import db
from app.api.v1.services.services import UserServices, get_agaricleaner_result, get_server_average_honor_score

import random
import uuid
import json
router = APIRouter()


from pydantic import BaseModel

class MessageInput(BaseModel):
    message: str

@router.post("/{server_id}/{system_id}")
async def eval_message(server_id: str, system_id: str, input: MessageInput, request: Request):
    message = input.message

    date_sent: datetime = datetime.now()
    word_count: int = len(message.split())
    score: float
    is_toxic: bool



    userServices = UserServices(system_id, server_id)
    server_average_honor_score = get_server_average_honor_score(server_id)


    with open("app/api/v1/endpoints/badwords.json", "r", encoding="utf-8") as f:
        data = json.load(f)["badwords"]

       
    score = userServices.getBayesianHonorLevel(server_average_honor_score)
    p = (1 - score) * 1

    # 필터링 당첨
    if(random.random() < p or any(word in message for word in data)):
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

        
    # firestore 에 메시지 데이터 저장
    message_data = {
        "system_id" : system_id,
        "server_id" : server_id,
        "date_sent": date_sent.isoformat(),
        "word_count": word_count,
        "score": score,
        "is_toxic": is_toxic,
    }

    message_id = str(uuid.uuid4())  # 자동 생성 메시지 ID (uuid4는 기준 없는 랜덤 uid)
    db.collection("servers").document(server_id)\
      .collection("users").document(system_id)\
      .collection("messages").document(message_id).set(message_data)

    return message_data



