# backend/app/models.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from typing import Optional, List

class Server(SQLModel, table = True):
    # other platforms might keep server id as a combination of char and int
    id: str = Field(default=None, primary_key=True) 
    name: str
    average_honor_score: float

    users: List["User"] = Relationship(back_populates="server")
    messages: List["Message"] = Relationship(back_populates="server")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) # has autoincrement integrated by default
    system_name: str
    system_id: str
    server_id: int = Field(foreign_key="server.id")
    honor_score: float

    server: Optional[Server] = Relationship(back_populates="users")
    messages: List["Message"] = Relationship(back_populates="users")

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    date_sent: datetime
    word_count: int
    # first_filter_passed: bool
    # second_filter_checked: bool
    score: Optional[float] = None
    is_toxic: bool

    server: Optional[Server] = Relationship(back_populates="messages")
    user: Optional[User] = Relationship(back_populates="messages")

