from pydantic import BaseModel, ConfigDict

class UserResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
