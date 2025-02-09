"""Add column blog_id in comment table

Revision ID: 7b12b6b0af09
Revises: 
Create Date: 2025-02-09 23:42:06.071525

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b12b6b0af09'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('commentaire', sa.Column('blog_id', sa.String(), nullable=True))


def downgrade() -> None:
    pass
