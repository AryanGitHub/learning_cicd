"""create user table

Revision ID: c588180c869b
Revises: f7cb24fbd7e9
Create Date: 2024-11-26 21:06:11.634487

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c588180c869b'
down_revision: Union[str, None] = 'f7cb24fbd7e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users" , 
                sa.Column("user_id",sa.Integer() ,primary_key=True),
                sa.Column("username", sa.String() ,nullable=False , unique=True),
                sa.Column("email", sa.String() ,nullable=False , unique=True),
                sa.Column("password_hashed", sa.String() ,nullable=False),
                sa.Column("created_at" , sa.TIMESTAMP() ,nullable=False , server_default=sa.text('now()'))
                )
    op.create_foreign_key('post_user_fk', source_table="resources_post", referent_table="users", local_cols=[
                          'author_id'], remote_cols=['user_id'], ondelete="CASCADE")
    pass

def downgrade() -> None:
    op.drop_constraint("post_user_fk" , table_name="resources_post")
    op.drop_table("users")
    pass
