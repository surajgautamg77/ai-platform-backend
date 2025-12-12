from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.core.database import SessionLocal

class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        db = SessionLocal()
        request.state.db = db
        try:
            response = await call_next(request)
        finally:
            db.close()
        return response
