from pydantic import BaseModel

from app.users.dto.UserResponseDto import UserResponseDto

class UserDetailResponseDto(BaseModel):
    status: str
    message: str
    data: UserResponseDto
