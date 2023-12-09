from alembic import op
import sqlalchemy as sa
from sqlalchemy import Sequence


revision = '9062e52dc642'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('file',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('original_name', sa.String(225), nullable=False),
                    sa.Column('random_name', sa.String(225), nullable=False, unique=True),
                    sa.Column('inspectionform_id', sa.Integer, nullable=False, index=True),
                    sa.ForeignKeyConstraint(['inspectionform_id'], ['inspectionform.id'])
                    )