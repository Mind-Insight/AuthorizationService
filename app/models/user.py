from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, String
from db.database import Base


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(
        Text,
        unique=False,
        nullable=False,
    )
