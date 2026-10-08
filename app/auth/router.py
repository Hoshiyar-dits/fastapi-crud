from fastapi import APIRouter, Depends, status

from app.auth.dto.LoginDto import LoginDto
from app.auth.dto.SignupDto import SignupDto
from app.auth.service import AuthService, get_auth_service

router = APIRouter(prefix="/auth")

@router.post("/signup")
def signup(data: SignupDto, service: AuthService = Depends(get_auth_service)):
    return service.signup(data)

@router.post("/login")
def login(data: LoginDto, service: AuthService = Depends(get_auth_service)):
    return service.login(data)
