"""create table

Revision ID: 142b80098ec7
Revises: 
Create Date: 2023-02-03 13:33:35.573833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '142b80098ec7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id",sa.Integer,primary_key=True),
        sa.Column("title",sa.String(50),nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
