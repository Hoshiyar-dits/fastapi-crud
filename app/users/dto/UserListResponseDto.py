from pydantic import BaseModel

from app.users.dto.UserResponseDto import UserResponseDto

class UserListResponseDto(BaseModel):
    status: str
    message: str
    data: list[UserResponseDto]
