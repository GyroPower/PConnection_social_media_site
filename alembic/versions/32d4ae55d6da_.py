"""empty message

Revision ID: 32d4ae55d6da
Revises: 75200e767cb8
Create Date: 2023-04-28 12:18:55.898473

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = "32d4ae55d6da"
down_revision = "75200e767cb8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("description", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "description")
    # ### end Alembic commands ###
