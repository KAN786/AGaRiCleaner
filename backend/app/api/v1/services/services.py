

from collections import deque
from gradio_client import Client

from fastapi import Depends, HTTPException
from sqlmodel import Session, select, func
from app.database import get_session
from app.models import User, Server

from app.schemas.user_schemas import UserCreate, UserUpdate
from app.schemas.server_schemas import ServerCreate

class UserServices:
    honorLevel: int
    messageEvalList: deque[tuple[bool, int]]

    learningRate = 0.05
    bayesianCnt = 50

    def __init__(self, system_id: str, server_id: int, session: Session):
        self.system_id = system_id
        self.server_id = server_id
        self.user: User
        self.honorLevel: float

        self.session = session
        
        # 서버 없으면 만들기
        try:    
            create_server(ServerCreate(id=server_id), session)
        except HTTPException as e:
            pass
        
        # 유저 없으면 만들기
        try:
            # 서버의 평균 honor_score 가져오기

            create_user(UserCreate(system_id=system_id, server_id=server_id, honor_score=0.5), session=session)
        except HTTPException as e:
            pass
        

        # db에서 유저 가져오기
        self.user = session.exec(
            select(User).where(
                (User.server_id == server_id) & 
                (User.system_id == system_id)
            )
        ).one()

        if not self.user:
            # 400 에러 반환
            raise HTTPException(
                status_code=400,
                detail=f"User {server_id} doesn't exists"
            )


        self.honorLevel = self.user.honor_score
        self.messageEvalList = [(msg.is_toxic, msg.score) for msg in self.user.messages]

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
        ), session=self.session)

        
            
    
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
        

def create_user(user_create: UserCreate, session: Session):
    existing_user = session.exec(
        select(User).where(
            User.system_id == user_create.system_id
    )).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail=f"User with system_id {user_create.system_id} already exists"
        )
    
    user = User.model_validate(user_create)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def update_user(user_update: UserUpdate, session: Session):
    user = session.exec(
        select(User).where(
            (User.server_id == user_update.server_id) & (User.system_id == user_update.system_id)
        )
    ).one()

    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    update_data = user_update.model_dump(exclude_unset = True)
    for key, value in update_data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def create_server(server_create: ServerCreate, session: Session):
    existing_server = session.exec(
        select(Server).where(
            Server.id == server_create.id
    )).first()

    if existing_server:
        raise HTTPException(status_code = 400, detail=f"Server with id {server_create.id} already exists")

    server = Server.model_validate(server_create)

    session.add(server)
    session.commit()
    session.refresh(server)
    return server

def get_server_average_honor_score(server_id: str, session: Session):
    avg_score = session.exec(
        select(func.avg(User.honor_score))
        .where(User.server_id == server_id)
    ).one()
    return avg_score or 0.5

if __name__ == "__main__":
    messageServices = MessageServices(Client("CLOUDYUL/AGaRiCleaner_Detector"))

    print("Agaricleaner Result:")
    result = messageServices.get_agaricleaner_result("씨발 존나게 더럽네")
    print(result)

