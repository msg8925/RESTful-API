"""Add foreign key to posts table

Revision ID: 528914d6e956
Revises: 5e095930e41e
Create Date: 2022-10-03 13:47:49.274003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '528914d6e956'
down_revision = '5e095930e41e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    
