"""create post table

Revision ID: f7cb24fbd7e9
Revises: 
Create Date: 2024-11-26 20:26:38.011108

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7cb24fbd7e9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("resources_post" , 
                    sa.Column("post_id",sa.Integer() ,primary_key=True , nullable=False),
                    sa.Column("title", sa.String() ,nullable=False),
                    sa.Column("description", sa.String() ,nullable=True),
                    sa.Column("http_link", sa.String() ,nullable=True),
                    sa.Column("votes", sa.Integer() ,nullable=False , default=0),
                    sa.Column("created_at" , sa.TIMESTAMP() ,nullable=False , server_default=sa.text('now()')),
                    sa.Column("author_id" , sa.Integer() ,nullable=False)
                    )

    pass


def downgrade() -> None:
    op.drop_table("resources_post")
    pass
