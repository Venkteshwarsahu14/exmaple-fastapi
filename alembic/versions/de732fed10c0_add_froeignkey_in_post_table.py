"""add froeignkey in post table

Revision ID: de732fed10c0
Revises: 481ac65b91fc
Create Date: 2023-01-19 11:20:06.549296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de732fed10c0'
down_revision = '481ac65b91fc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("owner_id",sa.Integer(),nullable = False))
    op.create_foreign_key("post_users_fk",source_table="posts",referent_table="users",local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk',table_name='posts')
    op.drop_column('posts','owner_id')
    pass
