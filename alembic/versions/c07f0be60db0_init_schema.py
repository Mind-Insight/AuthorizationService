"""init schema

Revision ID: c07f0be60db0
Revises: 
Create Date: 2024-12-29 16:08:09.517188

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.core.config import settings

# revision identifiers, used by Alembic.
revision: str = 'c07f0be60db0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(f"create schema {settings.db_schema}")


def downgrade() -> None:
    op.execute(f"drop schema {settings.db_schema}")
