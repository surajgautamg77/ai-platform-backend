from pydantic import BaseModel

class ChatsSession(BaseModel):
    session_name:str