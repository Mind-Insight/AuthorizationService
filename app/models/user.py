from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON, Boolean, Text, String
import uuid

from sqlalchemy.dialects.postgresql import UUID
from db.database import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"
    # id: Mapped[uuid.UUID] = mapped_column(
    #     UUID(as_uuid=True),
    #     primary_key=True,
    #     default=uuid.uuid4,
    #     unique=True,
    #     nullable=False,
    # )

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
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )
    connected_accounts: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )
