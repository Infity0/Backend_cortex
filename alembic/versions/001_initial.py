"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2025-12-12 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create User table
    op.create_table(
        'User',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('username', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('token_balance', sa.Integer(), default=0, nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True, nullable=True),
        sa.Column('email_verified', sa.Boolean(), default=False, nullable=True),
        sa.Column('verification_code', sa.String(6), nullable=True),
        sa.Column('verification_code_expires', sa.DateTime(), nullable=True),
        sa.Column('reset_token', sa.String(255), nullable=True),
        sa.Column('reset_token_expires', sa.DateTime(), nullable=True),
        sa.Column('avatar_url', sa.String(255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_User_id', 'User', ['id'])
    op.create_index('ix_User_email', 'User', ['email'])

    # Create SUBSCRIPTION_PLANS table
    op.create_table(
        'SUBSCRIPTION_PLANS',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('price', sa.DECIMAL(10, 2), nullable=False),
        sa.Column('tokens_included', sa.Integer(), nullable=False),
        sa.Column('duration_days', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('note', sa.String(255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_SUBSCRIPTION_PLANS_id', 'SUBSCRIPTION_PLANS', ['id'])

    op.create_table(
        'SUBSCRIPTIONS',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('User_id', sa.Integer(), nullable=False),
        sa.Column('SUBSCRIPTION_PLANS_id', sa.Integer(), nullable=False),
        sa.Column('start_date', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('end_date', sa.DateTime(), nullable=False),
        sa.Column('status', sa.Enum('active', 'inactive', 'cancelled', name='subscription_status'), default='active'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('auto_renew', sa.Integer(), default=1, nullable=True),
        sa.ForeignKeyConstraint(['User_id'], ['User.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['SUBSCRIPTION_PLANS_id'], ['SUBSCRIPTION_PLANS.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_SUBSCRIPTIONS_id', 'SUBSCRIPTIONS', ['id'])

    op.create_table(
        'TRANSACTIONS',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('User_id', sa.Integer(), nullable=False),
        sa.Column('SUBSCRIPTIONS_id', sa.Integer(), nullable=True),
        sa.Column('amount', sa.DECIMAL(10, 2), nullable=False),
        sa.Column('payment_method', sa.String(50), nullable=True),
        sa.Column('date', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('status', sa.String(20), default='pending', nullable=True),
        sa.ForeignKeyConstraint(['User_id'], ['User.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['SUBSCRIPTIONS_id'], ['SUBSCRIPTIONS.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_TRANSACTIONS_id', 'TRANSACTIONS', ['id'])

    op.create_table(
        'REQUESTS',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('User_id', sa.Integer(), nullable=False),
        sa.Column('request_type', sa.String(50), nullable=True),
        sa.Column('input_text', sa.String(500), nullable=True),
        sa.Column('input_image_url', sa.String(255), nullable=True),
        sa.Column('tokens_used', sa.Integer(), nullable=True),
        sa.Column('status', sa.Enum('pending', 'processing', 'completed', 'failed', name='request_status'), default='pending'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('style', sa.String(50), nullable=True),
        sa.Column('resolution', sa.String(20), nullable=True),
        sa.Column('error_message', sa.String(500), nullable=True),
        sa.ForeignKeyConstraint(['User_id'], ['User.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_REQUESTS_id', 'REQUESTS', ['id'])

    op.create_table(
        'IMAGES',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('User_id', sa.Integer(), nullable=False),
        sa.Column('REQUESTS_id', sa.Integer(), nullable=True),
        sa.Column('image_url', sa.String(255), nullable=False),
        sa.Column('original_url', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('is_favorite', sa.Boolean(), default=False, nullable=True),
        sa.ForeignKeyConstraint(['User_id'], ['User.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['REQUESTS_id'], ['REQUESTS.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_IMAGES_id', 'IMAGES', ['id'])

    op.execute("""
        INSERT INTO SUBSCRIPTION_PLANS (name, price, tokens_included, duration_days, description, note)
        VALUES 
            ('Sirdar', 0.00, 1000, 3, 'Trial plan', 'Free 3-day trial with 1000 tokens'),
            ('Expert', 1500.00, 24000, 30, 'Advanced plan', '1500 RUB/month with 24000 tokens'),
            ('Lord', 12000.00, 999999, 365, 'Professional plan', '12000 RUB/year with unlimited tokens')
    """)


def downgrade() -> None:
    op.drop_table('IMAGES')
    op.drop_table('REQUESTS')
    op.drop_table('TRANSACTIONS')
    op.drop_table('SUBSCRIPTIONS')
    op.drop_table('SUBSCRIPTION_PLANS')
    op.drop_table('User')
