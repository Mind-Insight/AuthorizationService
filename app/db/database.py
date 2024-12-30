from datetime import datetime, timezone
from typing import AsyncGenerator
import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import TIMESTAMP, MetaData
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncAttrs,
    async_sessionmaker,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
)

from core.config import settings


DATABASE_URL = settings.get_db_url()
engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()]
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    metadata = MetaData(
        naming_convention=convention,
        schema=settings.db_schema,
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )


async def get_db() -> AsyncGenerator:
    async with async_session() as session:
        yield session
        await session.close()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
