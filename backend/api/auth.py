from fastapi import APIRouter, HTTPException, status

from auth_schema import LoginRequest, TokenResponse
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    if not AuthService.authenticate_user(request.username, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = AuthService.create_access_token(request.username)

    return {
        "access_token": token,
        "token_type": "bearer",
    }