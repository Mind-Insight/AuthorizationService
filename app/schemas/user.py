from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str


class UserSchema(UserCreate):
    id: int

    class Config:
        from_attributes = True


class TokenInfo(BaseModel):
    access_token: str
    token_type: str
