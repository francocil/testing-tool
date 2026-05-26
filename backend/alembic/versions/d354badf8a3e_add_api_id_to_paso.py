"""add api_id to paso

Revision ID: d354badf8a3e
Revises: edbfbf831b82
Create Date: 2026-05-05
"""

from alembic import op
import sqlalchemy as sa


revision = "d354badf8a3e"
down_revision = "edbfbf831b82"
branch_labels = None
depends_on = None


def upgrade():
    # Solo agregar la columna si NO existe
    conn = op.get_bind()

    result = conn.execute(
        sa.text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='paso' AND column_name='api_id'
        """)
    ).fetchone()

    if not result:
        op.add_column(
            "paso",
            sa.Column("api_id", sa.Integer(), sa.ForeignKey("api.id"), nullable=True)
        )


def downgrade():
    op.drop_column("paso", "api_id")

