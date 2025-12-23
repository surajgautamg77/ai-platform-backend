from pydantic import BaseModel
from datetime import datetime

class CreateChatsSession(BaseModel):
    session_name:str

class Session(BaseModel):
    id: int
    session_name: str
    created_at: datetime

    model_config = {"from_attributes": True}