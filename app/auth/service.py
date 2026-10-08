from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.dto.LoginDto import LoginDto
from app.auth.dto.SignupDto import SignupDto
from app.auth.dto.TokenResponseDto import TokenResponseDto
from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    hash_password,
    verify_password,
)
from app.database.database import get_db
from app.users.dto.UserCreatedResponseDto import UserCreatedResponseDto
from app.users.dto.UserResponseDto import UserResponseDto
from app.users.repository import UserRepository


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def signup(self, data: SignupDto) -> UserCreatedResponseDto:
        if self.repository.get_by_email(data.email):
            raise HTTPException(status_code=400, detail="Email already exists")

        try:
            user = self.repository.create(
                name=data.name,
                email=data.email,
                hashed_password=hash_password(data.password),
            )
        except IntegrityError:
            self.repository.db.rollback()
            raise HTTPException(status_code=400, detail="Email already exists")

        return UserCreatedResponseDto(
            status="success",
            message="User created successfully",
            data=UserResponseDto.model_validate(user),
        )

    def login(self, data: LoginDto) -> TokenResponseDto:
        user = self.repository.get_by_email(data.email)
        if not user or not user.hashed_password or not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        return TokenResponseDto(
            status="success",
            message="Login successful",
            access_token=create_access_token(str(user.id)),
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            data=UserResponseDto.model_validate(user),
        )


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))
