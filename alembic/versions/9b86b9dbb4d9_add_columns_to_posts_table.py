"""add columns to posts table

Revision ID: 9b86b9dbb4d9
Revises: 142b80098ec7
Create Date: 2023-02-03 13:41:46.921195

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b86b9dbb4d9'
down_revision = '142b80098ec7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("content",sa.String(300),nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
