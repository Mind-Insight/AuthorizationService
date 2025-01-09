"""init schema

Revision ID: 9c194ec0988e
Revises: 
Create Date: 2025-01-09 21:57:05.562554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.core.config import settings


# revision identifiers, used by Alembic.
revision: str = '9c194ec0988e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(f"create schema {settings.db_schema}")


def downgrade() -> None:
    op.execute(f"drop schema {settings.db_schema}")