from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    # system_name: str
    system_id: str
    server_id: str
    honor_score: float = 0.5

class UserUpdate(BaseModel):
    # system_name: Optional[str] = None
    system_id: Optional[str] = None
    server_id: Optional[str] = None
    honor_score: Optional[float] = None