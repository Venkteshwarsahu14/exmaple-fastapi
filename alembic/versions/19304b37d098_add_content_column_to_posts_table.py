"""add content column to posts table

Revision ID: 19304b37d098
Revises: 1189a603a537
Create Date: 2023-01-19 10:48:14.719630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19304b37d098'
down_revision = '1189a603a537'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
