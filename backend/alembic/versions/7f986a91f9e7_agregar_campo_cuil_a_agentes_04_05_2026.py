"""add cuil to agentes

Revision ID: 7f986a91f9e7
Revises: d354badf8a3e
Create Date: 2026-05-04
"""

from alembic import op
import sqlalchemy as sa


revision = "7f986a91f9e7"
down_revision = "d354badf8a3e"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    result = conn.execute(
        sa.text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='agentes' AND column_name='cuil'
        """)
    ).fetchone()

    if not result:
        op.add_column(
            "agentes",
            sa.Column("cuil", sa.String(length=20), unique=True, nullable=False)
        )


def downgrade():
    op.drop_column("agentes", "cuil")

