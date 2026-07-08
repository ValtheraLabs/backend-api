from collections import defaultdict
from time import monotonic

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    decode_access_token,
    register_user,
)
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

AUTH_RATE_LIMIT = 10
AUTH_RATE_WINDOW = 60
_auth_attempts: dict[str, list[float]] = defaultdict(list)


def rate_limit_auth(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    now = monotonic()
    cutoff = now - AUTH_RATE_WINDOW
    attempts = [t for t in _auth_attempts[client_ip] if t >= cutoff]
    if len(attempts) >= AUTH_RATE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many auth attempts. Try again later.",
        )
    attempts.append(now)
    _auth_attempts[client_ip] = attempts


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db), _: None = Depends(rate_limit_auth)):
    try:
        user = register_user(db, payload.email, payload.display_name, payload.password)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Registration failed")

    token = create_access_token(user.id)
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db), _: None = Depends(rate_limit_auth)):
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(user.id)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
def me(current_user: UserResponse = Depends(get_current_user)):
    return current_user
