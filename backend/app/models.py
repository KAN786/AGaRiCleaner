# backend/app/models.py
# from sqlmodel import SQLModel, Field, Relationship (firebase is NoSQL)
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class Server(BaseModel):
    # other platforms might keep server id as a combination of char and int
    id: str # discord Server ID 

class User(BaseModel):
    # id: Optional[int] # FE doesn't need to access this
    # system_name: str
    system_id: str
    server_id: str
    honor_score: float

class Message(BaseModel):
    # id: Optional[int] # FE doesn't need to access this
    system_id: str
    server_id: str
    date_sent: datetime
    word_count: int
    score: Optional[float] = None
    is_toxic: bool

