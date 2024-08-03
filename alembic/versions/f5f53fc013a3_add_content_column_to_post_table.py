"""add content column to post table

Revision ID: f5f53fc013a3
Revises: 298eb168e87b
Create Date: 2024-08-03 18:11:54.325187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5f53fc013a3'
down_revision: Union[str, None] = '298eb168e87b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False ))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
