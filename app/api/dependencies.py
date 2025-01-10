from fastapi import Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from services.user_service import UserService
from repositories.user_repository import UserRepository
from utils import jwt_utils
from db.database import get_db, get_redis
from schemas.user import UserSchema


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    user_repository = UserRepository(db, User)
    return UserService(user_repository)


async def get_token_from_redis(
    token: str, redis: Redis = Depends(get_redis)
) -> str:
    email = await redis.get(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found or expired",
        )


async def get_current_token_payload(
    token: str = Depends(oauth2_scheme), redis: Redis = Depends(get_redis)
) -> dict:
    await get_token_from_redis(token, redis)
    try:
        payload = jwt_utils.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
        )
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    user_service: UserService = Depends(get_user_service),
) -> UserSchema:
    email: str | None = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid (missing email in payload)",
        )
    user = await user_service.repository.get_user_by_email(email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid (user not found)",
        )
    return user


async def validate_auth_user(
    username: str = Form(...),
    password: str = Form(...),
    user_service: UserService = Depends(get_user_service),
) -> UserSchema:
    user = await user_service.validate_user(email=username, password=password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return user
