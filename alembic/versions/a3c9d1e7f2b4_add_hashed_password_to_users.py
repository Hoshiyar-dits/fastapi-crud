"""add hashed_password to users

Revision ID: a3c9d1e7f2b4
Revises: 616e9637eb8a
Create Date: 2026-10-08 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3c9d1e7f2b4'
down_revision: Union[str, Sequence[str], None] = '616e9637eb8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("hashed_password", sa.String(length=255), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "hashed_password")
