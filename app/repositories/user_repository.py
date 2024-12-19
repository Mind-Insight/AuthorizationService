from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from utils import jwt_utils as jwt


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_data: dict):
        hashed_password = jwt.hash_password(user_data["password"])
        user_data["password"] = hashed_password.decode()
        db_user = User(**user_data)
        self.db.add(db_user)
        await self.db.commit()
        # await self.db.refresh(db_user)
        return db_user

    async def get_user_by_email(self, email: str):
        query = select(User).filter(User.email == email)
        result = await self.db.execute(query)
        return result.scalars().first()
