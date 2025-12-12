from fastapi import APIRouter, Request
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/")
def get_chats(request: Request):
    db: Session = request.state.db
    # Add your logic here
    return {"message": "This is the chat route"}
