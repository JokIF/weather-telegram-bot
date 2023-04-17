"""create user_images

Revision ID: 680eeee35260
Revises: 7138c51f12e8
Create Date: 2023-04-10 16:31:02.684931

"""
import datetime

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '680eeee35260'
down_revision = '7138c51f12e8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('user_images',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('url', sa.String(), nullable=False),
                    sa.Column('create_at', sa.TIMESTAMP(), default=datetime.datetime.utcnow()),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('user_images')
