"""Create auth schema and partitioned users table

Revision ID: b94ceefbf314
Revises: 
Create Date: 2025-02-21 09:42:33.228995

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b94ceefbf314"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("CREATE SCHEMA IF NOT EXISTS auth")
    op.execute(
        """
        CREATE TABLE auth.users (
            id UUID DEFAULT gen_random_uuid(),
            email VARCHAR(100) NOT NULL,
            password TEXT NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            connected_accounts JSON,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            device_type TEXT NOT NULL,
            PRIMARY KEY (id, device_type),
            UNIQUE (email, device_type)
        ) PARTITION BY LIST (device_type);
    """
    )

    op.execute(
        """
        CREATE TABLE auth.users_phone PARTITION OF auth.users
        FOR VALUES IN ('phone');
    """
    )

    op.execute(
        """
        CREATE TABLE auth.users_tablet PARTITION OF auth.users
        FOR VALUES IN ('tablet');
    """
    )

    op.execute(
        """
        CREATE TABLE auth.users_computer PARTITION OF auth.users
        FOR VALUES IN ('computer');
    """
    )

    op.execute(
        """
        CREATE TABLE auth.users_unknown PARTITION OF auth.users
        FOR VALUES IN ('unknown');
    """
    )


def downgrade():
    op.execute("DROP TABLE IF EXISTS auth.users_phone")
    op.execute("DROP TABLE IF EXISTS auth.users_tablet")
    op.execute("DROP TABLE IF EXISTS auth.users_computer")
    op.execute("DROP TABLE IF EXISTS auth.users_unknown")
    op.execute("DROP TABLE IF EXISTS auth.users")
    op.execute("DROP SCHEMA IF EXISTS auth")
