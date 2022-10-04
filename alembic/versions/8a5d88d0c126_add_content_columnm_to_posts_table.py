"""Add content columnm to posts table

Revision ID: 8a5d88d0c126
Revises: 5de6e205bc73
Create Date: 2022-10-03 13:22:45.774580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a5d88d0c126'
down_revision = '5de6e205bc73'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')

