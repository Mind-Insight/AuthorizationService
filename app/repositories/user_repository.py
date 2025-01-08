from sqlalchemy import select

from models.user import User
from repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):

    async def get_user_by_email(self, email: str):
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one()
