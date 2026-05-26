"""add paso_assert table

Revision ID: add_paso_assert
Revises: d354badf8a3e
Create Date: 2026-05-07

"""

from alembic import op
import sqlalchemy as sa


# Revision identifiers
revision = "add_paso_assert"
down_revision = "7f986a91f9e7"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "paso_assert",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("paso_id", sa.Integer(), sa.ForeignKey("paso.id"), nullable=False, index=True),
        sa.Column("tipo", sa.String(length=50), nullable=False),
        sa.Column("expresion", sa.String(length=255), nullable=True),
        sa.Column("operador", sa.String(length=50), nullable=False),
        sa.Column("valor_esperado", sa.Text(), nullable=True),
        sa.Column("mensaje_error", sa.Text(), nullable=True),
        sa.Column("orden", sa.Integer(), nullable=False, server_default="1"),
    )


def downgrade():
    op.drop_table("paso_assert")
