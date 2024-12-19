from repositories.user_repository import UserRepository
from schemas.user import UserCreate
# from fastapi import HTTPException, status


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, user: UserCreate):
        # existing_user = await self.user_repository.get_user_by_email(
        #     user.email
        # )
        # if existing_user:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Email is already registered",
        #     )
        return await self.user_repository.create_user(user)
