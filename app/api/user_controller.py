from fastapi import (
    APIRouter,
    Depends,
)
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_auth_user, validate_auth_user
from models.user import User
from utils import jwt_utils
from schemas.user import UserResponse, UserSchema, TokenInfo
from services.user_service import UserService
from repositories.user_repository import UserRepository
from db import database


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register/", response_model=UserResponse)
async def register_user(
    user_data: UserSchema,
    db: AsyncSession = Depends(database.get_db),
):
    user_repository = UserRepository(db, User)
    user_service = UserService(user_repository)
    user = await user_service.register_user(user_data)
    return UserResponse(id=user.id, email=user.email)


@router.post("/login/", response_model=TokenInfo)
async def login_user(
    user: UserSchema = Depends(validate_auth_user),
    redis: Redis = Depends(database.get_redis),
):
    jwt_payload = {
        "sub": user.email,
        "email": user.email,
    }
    token = jwt_utils.encode_jwt(jwt_payload)
    await redis.set(token, user.email, ex=3600)
    return TokenInfo(access_token=token, token_type="Bearer")


@router.get("/me/", response_model=UserResponse)
async def get_user_profile(
    user: UserSchema = Depends(get_current_auth_user),
):
    return UserResponse(id=str(user.id), email=user.email)


@router.patch("/me/")
async def udpate_profile(user: UserSchema = Depends(get_current_auth_user)):
    pass
