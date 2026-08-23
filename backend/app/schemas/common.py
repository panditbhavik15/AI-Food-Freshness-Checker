"""
Common response schemas used across all endpoints.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Structured error information."""
    code: str
    message: str


class ApiResponse(BaseModel):
    """Standard API response envelope."""
    success: bool
    data: Optional[Any] = None
    error: Optional[ErrorDetail] = None
    timestamp: datetime = None

    def __init__(self, **kwargs):
        if "timestamp" not in kwargs or kwargs["timestamp"] is None:
            kwargs["timestamp"] = datetime.utcnow()
        super().__init__(**kwargs)


def success_response(data: Any = None) -> dict:
    """Create a successful API response."""
    return ApiResponse(success=True, data=data).model_dump()


def error_response(code: str, message: str) -> dict:
    """Create an error API response."""
    return ApiResponse(
        success=False,
        error=ErrorDetail(code=code, message=message),
    ).model_dump()
