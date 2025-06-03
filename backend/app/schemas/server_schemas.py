from pydantic import BaseModel
from typing import Optional

class ServerCreate(BaseModel):
    id: str
    name: str
    average_honor_score: float = 0.5

class ServerUpdate(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    average_honor_score: Optional[float] = None