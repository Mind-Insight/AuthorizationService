from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: str
    password: str


class UserSchema(UserCreate):
    id: int

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class TokenInfo(BaseModel):
    access_token: str
    token_type: str
