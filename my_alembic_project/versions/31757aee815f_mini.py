"""mini

Revision ID: 31757aee815f
Revises: 13ba05b807e5
Create Date: 2023-12-18 21:12:24.409669

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31757aee815f'
down_revision: Union[str, None] = '13ba05b807e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('coments', sa.Column('news_id', sa.Integer(), nullable=True))
    op.add_column('coments', sa.Column('games_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'coments', 'games', ['games_id'], ['id'])
    op.create_foreign_key(None, 'coments', 'news', ['news_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'coments', type_='foreignkey')
    op.drop_constraint(None, 'coments', type_='foreignkey')
    op.drop_column('coments', 'games_id')
    op.drop_column('coments', 'news_id')
    # ### end Alembic commands ###