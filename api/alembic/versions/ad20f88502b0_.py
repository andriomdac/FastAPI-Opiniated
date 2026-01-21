"""empty message

Revision ID: ad20f88502b0
Revises: dd5ae0e2e14e
Create Date: 2026-01-19 21:31:37.697096

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad20f88502b0'
down_revision: Union[str, Sequence[str], None] = 'dd5ae0e2e14e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
