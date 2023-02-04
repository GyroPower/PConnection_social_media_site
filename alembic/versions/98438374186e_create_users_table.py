"""create users table

Revision ID: 98438374186e
Revises: 9b86b9dbb4d9
Create Date: 2023-02-03 13:54:11.302242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98438374186e'
down_revision = '9b86b9dbb4d9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id",sa.Integer,primary_key=True),
        sa.Column("email",sa.String(),nullable=False),
        sa.Column("password",sa.String(),nullable=False),
        sa.Column("created_at",sa.TIMESTAMP(timezone=True),server_default=sa.text("now()"),
        nullable=False),
        sa.UniqueConstraint("email")
    )
    pass


def downgrade() -> None:

    op.drop_table("users")
    pass
