from utils.jwt_utils import hash_password
from models.user import User
from repositories.user_repository import UserRepository
# from schemas.user import UserCreate
# from fastapi import HTTPException, status


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, user_data: dict) -> User:
        # existing_user = await self.user_repository.get_user_by_email(
        #     user.email
        # )
        # if existing_user:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Email is already registered",
        #     )
        user_data = user_data.model_dump()
        user_data["password"] = hash_password(user_data["password"]).decode()
        return await self.user_repository.create_user(user_data)
