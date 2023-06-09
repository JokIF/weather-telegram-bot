"""add two tables user, user_loc

Revision ID: abda8af456a5
Revises: 
Create Date: 2023-02-19 23:32:40.756463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abda8af456a5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('language', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_loc',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('lon', sa.DECIMAL(), nullable=False),
    sa.Column('lat', sa.DECIMAL(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_loc')
    op.drop_table('user')
    # ### end Alembic commands ###
