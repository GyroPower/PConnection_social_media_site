"""empty message

Revision ID: b29430da66f2
Revises: fc47f86f4f4c
Create Date: 2023-05-10 19:25:16.163155

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = "b29430da66f2"
down_revision = "fc47f86f4f4c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("posts", sa.Column("username", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("posts", "username")
    # ### end Alembic commands ###
