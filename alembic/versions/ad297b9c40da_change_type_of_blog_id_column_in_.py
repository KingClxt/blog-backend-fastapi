"""change type of blog_id column in comment table

Revision ID: ad297b9c40da
Revises: 7b12b6b0af09
Create Date: 2025-02-10 00:08:36.127032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad297b9c40da'
down_revision: Union[str, None] = '7b12b6b0af09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('ALTER TABLE commentaire ALTER COLUMN blog_id TYPE INTEGER USING blog_id::integer')


def downgrade() -> None:
    op.alter_column('commentaire', 'blog_id', type_=sa.String())
