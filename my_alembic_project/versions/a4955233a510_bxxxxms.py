"""Bxxxxms

Revision ID: a4955233a510
Revises: 1af533194a9c
Create Date: 2023-12-14 22:16:16.157437

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4955233a510'
down_revision: Union[str, None] = '1af533194a9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
