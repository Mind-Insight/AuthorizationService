from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreateSchema
from services.user_service import UserService
from repositories.user_repository import UserRepository
from db import database

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register/")
async def register_user(
    user_data: UserCreateSchema, db: AsyncSession = Depends(database.get_db)
):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    user = await user_service.register_user(user_data)
    return {"id": user.id, "email": user.email}
