"""create vote table

Revision ID: 30ee25bf5006
Revises: c588180c869b
Create Date: 2024-11-26 21:24:45.939413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '30ee25bf5006'
down_revision: Union[str, None] = 'c588180c869b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("votes" , 
                sa.Column("post_id",sa.Integer() ,primary_key=True),
                sa.Column("user_id", sa.Integer() ,primary_key=True),
                sa.Column("vote", sa.Integer() ,nullable=False )
                )
    op.create_foreign_key('vote_post_fk', source_table="votes", referent_table="resources_post", local_cols=[
                          'post_id'], remote_cols=['post_id'], ondelete="CASCADE")
    op.create_foreign_key('vote_user_fk', source_table="votes", referent_table="users", local_cols=[
                          'user_id'], remote_cols=['user_id'], ondelete="CASCADE")
    op.create_check_constraint(
        'ck_vote_limit',  # Name of the constraint
        'votes',         # Name of the table
        'vote >= -1 AND vote <= 1 AND vote != 0'      # The condition for the CHECK constraint
    )
    pass

def downgrade() -> None:
    op.drop_constraint("vote_post_fk" , table_name="votes")
    op.drop_constraint("vote_user_fk" , table_name="votes")
    op.drop_constraint(
        'ck_vote_limit',
        'votes',
        type_='check'
    )
    op.drop_table("votes")
    pass
