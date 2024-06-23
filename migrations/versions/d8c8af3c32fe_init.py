"""init

Revision ID: d8c8af3c32fe
Revises: 
Create Date: 2024-04-10 08:49:33.480133

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d8c8af3c32fe"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "places",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("country", sa.String(), nullable=False),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("address", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_places_id"), "places", ["id"], unique=False)
    op.create_table(
        "opinions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("opinion", sa.String(), nullable=True),
        sa.Column("vote", sa.Integer(), nullable=False),
        sa.Column("date_of_visit", sa.Date(), nullable=True),
        sa.Column("place_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["place_id"],
            ["places.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_opinions_id"), "opinions", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_opinions_id"), table_name="opinions")
    op.drop_table("opinions")
    op.drop_index(op.f("ix_places_id"), table_name="places")
    op.drop_table("places")
    # ### end Alembic commands ###