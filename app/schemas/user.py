from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    email: EmailStr
    password: str
    is_active: bool
    connected_accounts: dict[str, str] | None
    device_type: str
    age: int


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: str
    email: str


class ChangePassword(BaseModel):
    current_password: str
    new_password: str