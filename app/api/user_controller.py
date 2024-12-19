from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserSchema
from services.user_service import UserService
from repositories.user_repository import UserRepository
from db import database

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register/", response_model=UserSchema)
async def register_user(
    user_data: dict, db: AsyncSession = Depends(database.get_db)
):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    return await user_service.register_user(user_data)
