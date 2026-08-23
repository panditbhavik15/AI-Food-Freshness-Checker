"""
Authentication endpoints — register, login, logout, profile.
"""

import logging
import re
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.api.v1.deps import get_current_user_required
from app.models.user import User
from app.schemas.common import success_response, error_response
from app.schemas.user import UserRegisterRequest, UserLoginRequest

logger = logging.getLogger(__name__)

router = APIRouter()


def _validate_password_strength(password: str) -> Optional[str]:
    """Validate password meets minimum requirements."""
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"[a-zA-Z]", password):
        return "Password must contain at least one letter."
    if not re.search(r"\d", password):
        return "Password must contain at least one number."
    return None


@router.post("/register")
def register(
    request: UserRegisterRequest,
    db: Session = Depends(get_db),
):
    """
    Register a new user account.

    Requires email and password (min 8 chars, 1 letter, 1 number).
    Returns JWT tokens on success.
    """
    # Check password strength
    pwd_error = _validate_password_strength(request.password)
    if pwd_error:
        return error_response("WEAK_PASSWORD", pwd_error)

    # Check if email already exists
    existing = db.query(User).filter(User.email == request.email.lower()).first()
    if existing:
        return error_response("EMAIL_EXISTS", "An account with this email already exists.")

    # Create user
    user = User(
        email=request.email.lower(),
        hashed_password=hash_password(request.password),
        display_name=request.display_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate tokens
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)

    logger.info(f"New user registered: {user.email}")

    return success_response({
        "user": {
            "id": user.id,
            "email": user.email,
            "display_name": user.display_name,
        },
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    })


@router.post("/login")
def login(
    request: UserLoginRequest,
    db: Session = Depends(get_db),
):
    """
    Authenticate user and return JWT tokens.

    Returns generic error for invalid credentials (security best practice).
    """
    user = db.query(User).filter(User.email == request.email.lower()).first()

    if not user or not verify_password(request.password, user.hashed_password):
        return error_response("INVALID_CREDENTIALS", "Invalid email or password.")

    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)

    logger.info(f"User logged in: {user.email}")

    return success_response({
        "user": {
            "id": user.id,
            "email": user.email,
            "display_name": user.display_name,
        },
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    })


@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user_required),
):
    """
    Logout the current user.

    For JWT-based auth, logout is handled client-side by discarding the token.
    This endpoint exists for API completeness and audit logging.
    """
    logger.info(f"User logged out: {current_user.email}")
    return success_response({"message": "Successfully logged out."})


@router.get("/profile")
def get_profile(
    current_user: User = Depends(get_current_user_required),
):
    """Get the current user's profile."""
    return success_response({
        "id": current_user.id,
        "email": current_user.email,
        "display_name": current_user.display_name,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
    })
