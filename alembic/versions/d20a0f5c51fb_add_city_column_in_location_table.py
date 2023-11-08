"""add city column in location table

Revision ID: d20a0f5c51fb
Revises: 
Create Date: 2023-11-08 19:19:26.758612

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd20a0f5c51fb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('location', sa.Column('city', sa.String(45)))


def downgrade() -> None:
    op.drop_column('location', 'city')
