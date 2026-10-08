from fastapi import APIRouter, Depends, Query

from app.auth.dependencies import get_current_user
from app.users.dto.UpdateUserDto import UpdateUserDto
from app.users.dto.UserDetailResponseDto import UserDetailResponseDto
from app.users.dto.UserListResponseDto import UserListResponseDto
from app.users.dto.UserResponseDto import UserResponseDto
from app.users.models import User
from app.users.service import UserService, get_user_service

router = APIRouter(prefix="/users", dependencies=[Depends(get_current_user)])

@router.get("")
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: UserService = Depends(get_user_service),
):
    return service.get_users(skip, limit)

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return UserDetailResponseDto(
        status="success",
        message="User fetched successfully",
        data=UserResponseDto.model_validate(current_user),
    )

@router.get("/{user_id}")
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    return service.get_user(user_id)

@router.patch("/{user_id}")
def update_user(
    user_id: int,
    data: UpdateUserDto,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return service.update_user(user_id, data, current_user)
