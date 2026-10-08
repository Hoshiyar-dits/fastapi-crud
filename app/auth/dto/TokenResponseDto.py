from pydantic import BaseModel

from app.users.dto.UserResponseDto import UserResponseDto

class TokenResponseDto(BaseModel):
    status: str
    message: str
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    data: UserResponseDto
