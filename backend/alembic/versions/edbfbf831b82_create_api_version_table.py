"""create api_version table

Revision ID: edbfbf831b82
Revises: edbfbf831b81
Create Date: 2026-05-05
"""

from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision = 'edbfbf831b82'
down_revision = 'edbfbf831b81'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'api_version',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('api_id', sa.Integer(), sa.ForeignKey('api.id', ondelete='CASCADE'), nullable=False, index=True),

        sa.Column('version', sa.String(length=20), nullable=False),

        sa.Column('metodo', sa.String(length=10), nullable=False),
        sa.Column('base_url', sa.String(length=255), nullable=True),
        sa.Column('endpoint', sa.Text(), nullable=False),

        sa.Column('auth_tipo', sa.String(length=20), nullable=False, server_default="none"),
        sa.Column('auth_config', sa.Text(), nullable=True),

        sa.Column('headers_por_defecto', sa.Text(), nullable=True),
        sa.Column('body_ejemplo', sa.Text(), nullable=True),

        sa.Column('timeout_segundos', sa.Integer(), nullable=False, server_default="10"),
        sa.Column('retries', sa.Integer(), nullable=False, server_default="0"),

        sa.Column('creado_por_usuario_id', sa.Integer(), sa.ForeignKey('usuario.id'), nullable=True),

        sa.Column('fecha_creacion', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )


def downgrade():
    op.drop_index('ix_api_version_version', table_name='api_version')
    op.drop_index('ix_api_version_api_id', table_name='api_version')
    op.drop_table('api_version')
