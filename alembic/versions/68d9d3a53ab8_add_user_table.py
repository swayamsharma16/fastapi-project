"""add user table

Revision ID: 68d9d3a53ab8
Revises: f5f53fc013a3
Create Date: 2024-08-03 23:02:34.961907

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68d9d3a53ab8'
down_revision: Union[str, None] = 'f5f53fc013a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
         sa.Column('id', sa.Integer()),
         sa.Column('email', sa.String(), nullable=False),
         sa.Column('password',sa.String(), nullable=False),
         sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                   server_default=sa.text('now()'), nullable=False),
         sa.PrimaryKeyConstraint('id'),
         sa.UniqueConstraint('email')

        )

    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
