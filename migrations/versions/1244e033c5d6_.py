"""empty message

Revision ID: 1244e033c5d6
Revises: 
Create Date: 2021-05-16 20:06:29.476298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1244e033c5d6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=64), nullable=False),
    sa.Column('user_password', sa.String(length=64), nullable=False),
    sa.Column('roles', sa.Enum(), nullable=False),
    sa.Column('roles_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['roles_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
