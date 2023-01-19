"""add users table

Revision ID: 481ac65b91fc
Revises: 19304b37d098
Create Date: 2023-01-19 11:06:09.240447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '481ac65b91fc'
down_revision = '19304b37d098'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",sa.Column("id",sa.Integer(),nullable = False),
                        sa.Column('email',sa.String,nullable = False),
                        sa.Column('password',sa.String, nullable = False),
                        sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default = sa.text("now()")),
                        sa.PrimaryKeyConstraint('id'),
                        sa.UniqueConstraint('email')   
                    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
