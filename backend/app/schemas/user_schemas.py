from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    system_name: str
    system_id: str
    server_id: int
    honor_score: int

class UserUpdate(BaseModel):
    system_name: Optional[str] = None
    system_id: Optional[str] = None
    server_id: Optional[int] = None
    honor_score: Optional[int] = None