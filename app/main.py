from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

# Import domain routers
from app.users import router as user_router
from app.chats import router as chat_router
from app.auth import router as auth_router

from app.core.database import engine, Base
from app.middleware.middleware import DBSessionMiddleware

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Platform API",
    description="API for the AI Platform",
    version="1.0.0",
)

# Add middleware
app.add_middleware(DBSessionMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health Check"])
def read_root():
    return {"message": "Welcome to the AI Platform API"}

# Include domain routers
api_router = APIRouter()
api_router.include_router(auth_router.router, prefix="/auth", tags=["auth"])
api_router.include_router(chat_router.router, prefix="/chat", tags=["chat"])
api_router.include_router(user_router.router, prefix="/users", tags=["users"])

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    from app.core.config import settings
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
