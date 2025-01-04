from fastapi import Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service import UserService
from repositories.user_repository import UserRepository
from utils import jwt_utils
from db.database import get_db
from schemas.user import UserSchema


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")


def get_user_service(db: AsyncSession = Depends(get_db)):
    user_repository = UserRepository(db)
    return UserService(user_repository)


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = jwt_utils.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token: {e}",
        )
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    db: AsyncSession = Depends(get_db),
) -> UserSchema:
    email: str | None = payload.get("sub")
    user_repository = UserRepository(db)
    user = await user_repository.get_user_by_email(email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid (user not found)",
        )
    return user


async def validate_auth_user(
    email: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
    user_service: UserService = Depends(get_user_service),
) -> UserSchema:
    user = await user_service.validate_user(email=email, password=password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
