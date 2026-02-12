"""Initial migration - create drafts and bot_outputs tables

Revision ID: 001
Revises: 
Create Date: 2026-02-05 09:36:45.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create drafts table
    op.create_table(
        'drafts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_drafts_tenant_id'), 'drafts', ['tenant_id'], unique=False)
    op.create_index(op.f('ix_drafts_expires_at'), 'drafts', ['expires_at'], unique=False)

    # Create bot_outputs table
    op.create_table(
        'bot_outputs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('output_data', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bot_outputs_tenant_id'), 'bot_outputs', ['tenant_id'], unique=False)
    op.create_index(op.f('ix_bot_outputs_expires_at'), 'bot_outputs', ['expires_at'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_bot_outputs_expires_at'), table_name='bot_outputs')
    op.drop_index(op.f('ix_bot_outputs_tenant_id'), table_name='bot_outputs')
    op.drop_table('bot_outputs')
    
    op.drop_index(op.f('ix_drafts_expires_at'), table_name='drafts')
    op.drop_index(op.f('ix_drafts_tenant_id'), table_name='drafts')
    op.drop_table('drafts')
