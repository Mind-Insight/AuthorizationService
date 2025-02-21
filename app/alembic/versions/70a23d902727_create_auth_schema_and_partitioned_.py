"""Create auth schema and partitioned users table

Revision ID: 70a23d902727
Revises: 
Create Date: 2025-02-21 11:47:14.255054

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "70a23d902727"
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
            age INT NOT NULL,
            PRIMARY KEY (id, device_type, age),
            UNIQUE (email, device_type, age)
        ) PARTITION BY LIST (device_type);
        """
    )

    for device in ["phone", "tablet", "computer", "unknown"]:
        op.execute(
            f"""
            CREATE TABLE auth.users_{device} PARTITION OF auth.users
            FOR VALUES IN ('{device}')
            PARTITION BY RANGE (age);
            """
        )
    age_ranges = [(0, 18, "young"), (18, 50, "adult"), (50, 150, "senior")]

    for device in ["phone", "tablet", "computer", "unknown"]:
        for start, end, label in age_ranges:
            op.execute(
                f"""
                CREATE TABLE auth.users_{device}_{label} PARTITION OF auth.users_{device}
                FOR VALUES FROM ({start}) TO ({end});
                """
            )


def downgrade():
    for device in ["phone", "tablet", "computer", "unknown"]:
        for _, _, label in [
            (0, 18, "young"),
            (18, 50, "adult"),
            (50, 150, "senior"),
        ]:
            op.execute(f"DROP TABLE IF EXISTS auth.users_{device}_{label}")
    for device in ["phone", "tablet", "computer", "unknown"]:
        op.execute(f"DROP TABLE IF EXISTS auth.users_{device}")

    op.execute("DROP TABLE IF EXISTS auth.users")
    op.execute("DROP SCHEMA IF EXISTS auth")
