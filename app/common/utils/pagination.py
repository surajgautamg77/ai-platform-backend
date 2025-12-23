from fastapi import Query
from pydantic import BaseModel
from typing import List, Generic, TypeVar

T = TypeVar('T')

def pagination_parameters(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
):
    """
    A dependency to extract pagination query parameters (page and size).
    Calculates the 'skip' value for database queries.
    """
    skip = (page - 1) * size
    return {"skip": skip, "limit": size, "page": page, "size": size}

class PaginatedResponse(BaseModel, Generic[T]):
    """
    A generic Pydantic schema for paginated API responses.
    """
    total: int
    page: int
    size: int
    results: List[T]
