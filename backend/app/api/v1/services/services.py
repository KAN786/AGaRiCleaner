from collections import deque
from gradio_client import Client

from fastapi import Depends, HTTPException
from app.database import db
from app.models import User, Server

from app.schemas.user_schemas import UserCreate, UserUpdate
from app.schemas.server_schemas import ServerCreate

class UserServices:
    honorLevel: float
    messageEvalList: deque[tuple[bool, float]]

    learningRate = 0.02
    bayesianCnt = 50

    def __init__(self, system_id: str, server_id: str): # server_id used to be int, probably outdated
        self.system_id = system_id
        self.server_id = server_id
        # self.user: User (not needed)
        self.honorLevel: float
        

        # 서버 없으면 만들기
        try:
            create_server(ServerCreate(id=server_id))
        except HTTPException:
            pass


        # 유저 없으면 만들기
        user_ref = db.collection("servers").document(server_id).collection("users").document(system_id)
        user_snapshot = user_ref.get()
        if not user_snapshot.exists:
            user_ref.set(UserCreate(system_id=system_id, server_id=server_id, honor_score=0.5).model_dump())
            self.honorLevel = 0.5
        else:
            user_data = user_snapshot.to_dict()
            self.honorLevel = user_data.get("honor_score", 0.5)

        # Firestore doesn't require you to get messages via User, but rather the Message table itself        

        messages = user_ref.collection("messages") \
            .order_by("date_sent", direction="DESCENDING") \
            .limit(210).stream()
        
        # sets default score to 0.5 if for whatever reason, it wasn't set
        self.messageEvalList = deque([
            (doc.to_dict()["is_toxic"], doc.to_dict().get("score", 0.5)) 
            for doc in messages
        ])

    def update_honor(self, evalResult: tuple[bool, int]):
        def calc(x: tuple[bool, int]):
            
            delta = self.learningRate * x[1] * self.honorLevel * (1 - self.honorLevel);
            delta = -delta if x[0] else delta
            self.honorLevel += delta
        
        # 추가
        self.messageEvalList.append(evalResult)
        calc(evalResult)
        

        # 150 넘으면 가장 오래된 메세지 지우기
        if(len(self.messageEvalList) > 150):
            temp = self.messageEvalList.popleft()
            calc((not temp[0], temp[1]))


        update_user(UserUpdate(
            system_id=self.system_id,
            server_id=self.server_id,
            honor_score=self.honorLevel
        ))

    def getBayesianHonorLevel(self, serverAverage) -> float:
        v = len(self.messageEvalList)

        return v / (v + self.bayesianCnt) * self.honorLevel + \
               self.bayesianCnt / (v + self.bayesianCnt) * serverAverage


def get_agaricleaner_result(client: Client, message: str):
    
    result = client.predict(
            texts=message,
            api_name="/predict"
    )
    return result
        

def create_user(user_create: UserCreate):
    user_ref = db.collection("servers").document(user_create.server_id).collection("users").document(user_create.system_id)
    if user_ref.get().exists:
        raise HTTPException(status_code=400, detail="User already exists")
    user_ref.set(user_create.model_dump())

def update_user(user_update: UserUpdate):
    user_ref = db.collection("servers").document(user_update.server_id).collection("users").document(user_update.system_id)
    if not user_ref.get().exists:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user_update.model_dump(exclude_unset=True)
    user_ref.update(update_data)

def create_server(server_create: ServerCreate):
    server_ref = db.collection("servers").document(server_create.id)
    if server_ref.get().exists:
        raise HTTPException(status_code=400, detail="Server already exists")
    server_ref.set(server_create.model_dump())

def get_server_average_honor_score(server_id: str):
    users_ref = db.collection("servers").document(server_id).collection("users")
    user_docs = users_ref.stream()
    scores = [doc.to_dict().get("honor_score", 0.5) for doc in user_docs]
    return sum(scores) / len(scores) if scores else 0.5

def get_user_honor_score(server_id: str, system_id: str):
    user_ref = db.collection("servers").document(server_id).collection("users").document(system_id)
    user_snapshot = user_ref.get()
    user_data = user_snapshot.to_dict()
    return user_data.get("honor_score")


if __name__ == "__main__":
    messageServices = MessageServices(Client("CLOUDYUL/AGaRiCleaner_Detector"))

    print("Agaricleaner Result:")
    result = messageServices.get_agaricleaner_result("씨발 존나게 더럽네")
    print(result)

