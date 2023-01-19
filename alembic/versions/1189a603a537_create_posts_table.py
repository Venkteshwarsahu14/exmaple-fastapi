"""create posts table

Revision ID: 1189a603a537
Revises: 
Create Date: 2023-01-19 10:33:01.067645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1189a603a537'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable = False,primary_key = True),sa.Column('title',sa.String,nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
