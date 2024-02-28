"""description

Revision ID: 83f498739050
Revises: dc0e6e43c394
Create Date: 2024-02-28 12:54:52.681703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83f498739050'
down_revision = 'dc0e6e43c394'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('user_id', sa.Integer, unique=True))
    pass


def downgrade() -> None:
    pass
