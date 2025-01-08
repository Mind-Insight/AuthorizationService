from fastapi import HTTPException, status
from services.crud import BaseService
from utils.jwt_utils import hash_password, validate_password
from models.user import User
from repositories.user_repository import UserRepository


class UserService(BaseService[User]):
    def __init__(self, repository: UserRepository):
        self.user_repository = repository

    async def register_user(self, user_data: dict) -> User:
        user_data = user_data.model_dump()
        user_data["password"] = hash_password(user_data["password"]).decode()
        print(user_data["password"])
        return await self.user_repository.create(user_data)

    async def validate_user(self, email: str, password: str):
        user = await self.user_repository.get_user_by_email(email=email)
        if user and validate_password(password, user.password):
            return user
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
