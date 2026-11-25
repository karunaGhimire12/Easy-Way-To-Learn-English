"""restructure vocabulary tables

Revision ID: 655164edbe26
Revises: 522c73dc0aa3
Create Date: 2026-11-24 17:43:18.049269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '655164edbe26'
down_revision: Union[str, Sequence[str], None] = '522c73dc0aa3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    with op.batch_alter_table('vocabulary', schema=None) as batch_op:
        batch_op.drop_column('synonyms')
        batch_op.drop_column('antonyms')
        batch_op.drop_column('example_sentence')
        batch_op.drop_column('meaning')


"""restructure vocabulary tables

Revision ID: 655164edbe26
Revises: 522c73dc0aa3
Create Date: 2026-11-24 17:43:18.049269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '655164edbe26'
down_revision: Union[str, Sequence[str], None] = '522c73dc0aa3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def downgrade() -> None:
    """Downgrade schema."""

    with op.batch_alter_table('vocabulary', schema=None) as batch_op:
        batch_op.add_column(sa.Column('meaning', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('synonyms', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('antonyms', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('example_sentence', sa.VARCHAR(), nullable=True))

