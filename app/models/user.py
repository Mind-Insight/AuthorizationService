from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON, Boolean, Column, Integer, Text, String

from db.database import Base, TimestampMixin


class User(Base, TimestampMixin):
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    connected_accounts: Mapped[dict | None] = mapped_column(
        JSON, nullable=True
    )
    device_type = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
