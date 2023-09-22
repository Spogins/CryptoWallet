"""migration

Revision ID: 22140d47825f
Revises: 7f437c661ec1
Create Date: 2023-09-18 13:57:28.449570

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '22140d47825f'
down_revision: Union[str, None] = '7f437c661ec1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_status_id', table_name='status')
    op.drop_table('status')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('status',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('status', postgresql.ENUM('SUCCESS', 'FAILURE', 'PENDING', 'FAILED', name='transactionstatus'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='status_pkey')
    )
    op.create_index('ix_status_id', 'status', ['id'], unique=False)
    # ### end Alembic commands ###