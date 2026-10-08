from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.database.database import get_db
from app.users.models import User
from app.users.repository import UserRepository
from app.users.dto.UpdateUserDto import UpdateUserDto
from app.users.dto.UserDetailResponseDto import UserDetailResponseDto
from app.users.dto.UserListResponseDto import UserListResponseDto
from app.users.dto.UserResponseDto import UserResponseDto


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_users(self, skip: int, limit: int) -> UserListResponseDto:
        users = self.repository.get_all(skip=skip, limit=limit)
        return UserListResponseDto(
            status="success",
            message="Users fetched successfully",
            data=[UserResponseDto.model_validate(user) for user in users],
        )

    def get_user(self, user_id: int) -> UserDetailResponseDto:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return UserDetailResponseDto(
            status="success",
            message="User fetched successfully",
            data=UserResponseDto.model_validate(user),
        )

    def update_user(self, user_id: int, data: UpdateUserDto, current_user: User) -> UserDetailResponseDto:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.id != current_user.id:
            raise HTTPException(status_code=403, detail="You can only update your own account")

        fields = data.model_dump(exclude_unset=True, exclude_none=True)
        if "email" in fields and fields["email"] != user.email:
            if self.repository.get_by_email(fields["email"]):
                raise HTTPException(status_code=400, detail="Email already exists")
        if "password" in fields:
            fields["hashed_password"] = hash_password(fields.pop("password"))

        try:
            user = self.repository.update(user, fields)
        except IntegrityError:
            self.repository.db.rollback()
            raise HTTPException(status_code=400, detail="Email already exists")

        return UserDetailResponseDto(
            status="success",
            message="User updated successfully",
            data=UserResponseDto.model_validate(user),
        )


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))
