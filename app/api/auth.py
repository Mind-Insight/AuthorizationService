from fastapi import APIRouter, Depends, Form, HTTPException, status
from pydantic import BaseModel

from utils import jwt_utils
from schemas.user import UserSchema


router = APIRouter(prefix="/jwt", tags=["JWT"])


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


user1 = UserSchema(
    id=1, email="user1@gmail.com", password=jwt_utils.hash_password("user1")
)
user2 = UserSchema(
    id=2, email="user2@gmail.com", password=jwt_utils.hash_password("user2")
)
users_db = {user1.email: user1, user2.email: user2}


def validate_auth_user(username: str = Form(), password: str = Form()):
    unauthed_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
    print("username", type(username))
    if not (user := users_db.get(username + "@gmail.com")):
        raise unauthed_exception
    if jwt_utils.validate_password(
        password=password, hashed_password=user.password
    ):
        return user
    raise unauthed_exception


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": user.email,
        "email": user.email,
    }
    token = jwt_utils.encode_jwt(jwt_payload)
    return TokenInfo(access_token=token, token_type="Bearer")
# from fastapi import APIRouter
# from .dependencies import validate_auth_user
# from schemas.user import TokenInfo
# from utils import jwt_utils
# from schemas.user import UserSchema
# from fastapi import Depends

# router = APIRouter(prefix="/auth", tags=["AUTH"])


# @router.post("/login/", response_model=TokenInfo)
# def auth_user_issue_jwt(user: UserSchema = Depends(validate_auth_user)):
#     jwt_payload = {
#         "sub": user.email,
#         "email": user.email,
#     }
#     token = jwt_utils.encode_jwt(jwt_payload)
#     return TokenInfo(access_token=token, token_type="Bearer")
