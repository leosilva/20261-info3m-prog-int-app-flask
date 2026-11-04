"""adicionando perfil do usuario

Revision ID: b7d9e2a4c681
Revises: a16f7efe1c88
"""
from alembic import op
import sqlalchemy as sa


revision = 'b7d9e2a4c681'
down_revision = 'a16f7efe1c88'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('role', sa.String(length=16), nullable=False, server_default='PADRAO')
        )


def downgrade():
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.drop_column('role')
