from fastapi import APIRouter
from app.api.v1 import auth_routes, chat_routes, user_routes

api_router = APIRouter()

api_router.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
api_router.include_router(chat_routes.router, prefix="/chat", tags=["chat"])
api_router.include_router(user_routes.router, prefix="/users", tags=["users"])
