from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from repositories import UserRepository


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, email: str, name: str):
        user = User(email=email, name=name)
        user_repository = UserRepository(self.db)
        return await user_repository.create_user(user)
