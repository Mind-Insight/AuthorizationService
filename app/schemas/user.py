from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    email: EmailStr
    password: bytes


class TokenInfo(BaseModel):
    access_token: str
    token_type: str
