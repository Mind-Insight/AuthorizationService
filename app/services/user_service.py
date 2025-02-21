from fastapi import HTTPException, status

from services.crud import BaseService
from utils.jwt_utils import hash_password, validate_password
from models.user import User
from repositories.user_repository import UserRepository


class UserService(BaseService[User]):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register_user(self, user_data: dict) -> User:
        user_data = user_data.model_dump()
        user_data["password"] = hash_password(user_data["password"])
        
        # Проверяем, есть ли device_type, если нет - устанавливаем "unknown"
        if "device_type" not in user_data:
            user_data["device_type"] = "unknown"

        return await self.repository.create(user_data)

    async def change_password(
        self,
        user_id: str,
        current_password: str,
        new_password: str,
    ):
        user = await self.repository.get(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if not validate_password(current_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Incorrect password",
            )

        new_hashed_password = hash_password(new_password)
        await self.repository.update(
            user_id, {"password": new_hashed_password}
        )

    async def validate_user(self, email: str, password: str):
        user = await self.repository.get_user_by_email(email=email)
        if user and validate_password(password, user.password):
            return user
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
