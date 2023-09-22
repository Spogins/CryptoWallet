"""init

Revision ID: 500d27676e16
Revises: 
Create Date: 2023-08-26 18:53:16.068490

"""
from typing import Sequence, Union

import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '500d27676e16'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blockchain',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('image', sqlalchemy_utils.types.url.URLType(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_blockchain_id'), 'blockchain', ['id'], unique=False)
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hash', sa.String(), nullable=True),
    sa.Column('from_address', sa.String(), nullable=True),
    sa.Column('to_address', sa.String(), nullable=True),
    sa.Column('value', sa.DECIMAL(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('txn_fee', sa.DECIMAL(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transaction_id'), 'transaction', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('avatar', sqlalchemy_utils.types.url.URLType(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('chat_access', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=False)
    op.create_table('asset',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('abbreviation', sa.String(), nullable=True),
    sa.Column('image', sqlalchemy_utils.types.url.URLType(), nullable=True),
    sa.Column('symbol', sa.String(), nullable=True),
    sa.Column('decimal_places', sa.Integer(), nullable=True),
    sa.Column('blockchain_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['blockchain_id'], ['blockchain.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_asset_id'), 'asset', ['id'], unique=False)
    op.create_table('chat_message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('image', sqlalchemy_utils.types.url.URLType(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chat_message_id'), 'chat_message', ['id'], unique=False)
    op.create_table('wallet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('private_key', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('balance', sa.DECIMAL(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('asset_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['asset_id'], ['asset.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('address'),
    sa.UniqueConstraint('private_key')
    )
    op.create_index(op.f('ix_wallet_id'), 'wallet', ['id'], unique=False)
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('image', sqlalchemy_utils.types.url.URLType(), nullable=True),
    sa.Column('price', sa.DECIMAL(), nullable=True),
    sa.Column('in_order', sa.Boolean(), nullable=True),
    sa.Column('wallet_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['wallet_id'], ['wallet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_product_id'), 'product', ['id'], unique=False)
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('refund_id', sa.Integer(), nullable=True),
    sa.Column('transaction_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['refund_id'], ['transaction.id'], ),
    sa.ForeignKeyConstraint(['transaction_id'], ['transaction.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_id'), 'order', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_order_id'), table_name='order')
    op.drop_table('order')
    op.drop_index(op.f('ix_product_id'), table_name='product')
    op.drop_table('product')
    op.drop_index(op.f('ix_wallet_id'), table_name='wallet')
    op.drop_table('wallet')
    op.drop_index(op.f('ix_chat_message_id'), table_name='chat_message')
    op.drop_table('chat_message')
    op.drop_index(op.f('ix_asset_id'), table_name='asset')
    op.drop_table('asset')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_transaction_id'), table_name='transaction')
    op.drop_table('transaction')
    op.drop_index(op.f('ix_blockchain_id'), table_name='blockchain')
    op.drop_table('blockchain')
    # ### end Alembic commands ###