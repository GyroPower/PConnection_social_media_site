"""add foreign key to posts table

Revision ID: 50e8c7e26a01
Revises: 98438374186e
Create Date: 2023-02-03 14:12:34.569540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50e8c7e26a01'
down_revision = '98438374186e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("owner_id",sa.Integer,nullable=False)
    )
    op.create_foreign_key("posts_users_fkey",source_table="posts",referent_table="users",
    local_cols=["owner_id"],remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fkey",table_name="posts")
    op.drop_column("posts","owner_id")
    pass
