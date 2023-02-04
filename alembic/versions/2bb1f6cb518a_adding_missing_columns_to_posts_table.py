"""adding missing columns to posts table

Revision ID: 2bb1f6cb518a
Revises: 50e8c7e26a01
Create Date: 2023-02-03 14:25:44.895957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bb1f6cb518a'
down_revision = '50e8c7e26a01'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("published",sa.Boolean,nullable=False,server_default="TRUE")
    )
    op.add_column(
        "posts",
        sa.Column("created_at",sa.TIMESTAMP(timezone=True), nullable = False,
        server_default=sa.text("NOW()"))
    )
    pass


def downgrade() -> None:
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
    pass
