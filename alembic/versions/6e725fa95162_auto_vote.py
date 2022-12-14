"""Auto-vote

Revision ID: 6e725fa95162
Revises: 8c2d4a914e77
Create Date: 2022-10-03 14:56:48.446478

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6e725fa95162'
down_revision = '8c2d4a914e77'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_table('users',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('email', sa.String(), nullable=False),
    # sa.Column('password', sa.String(), nullable=False),
    # sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    # sa.PrimaryKeyConstraint('id'),
    # sa.UniqueConstraint('email')
    # )
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    # op.drop_table('user')
    # op.drop_constraint('post_users_fk', 'posts', type_='foreignkey')
    # op.create_foreign_key(None, 'posts', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_constraint(None, 'posts', type_='foreignkey')
    # op.create_foreign_key('post_users_fk', 'posts', 'user', ['owner_id'], ['id'], ondelete='CASCADE')
    # op.create_table('user',
    # sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    # sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    # sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False),
    # sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    # sa.PrimaryKeyConstraint('id', name='user_pkey'),
    # sa.UniqueConstraint('email', name='user_email_key')
    # )
    op.drop_table('votes')
    # op.drop_table('users')
    # ### end Alembic commands ###
