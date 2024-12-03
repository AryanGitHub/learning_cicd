from .database import Base , engine
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint, Column, Integer, String, TIMESTAMP , ForeignKey

class resource(Base):
    __tablename__ = "resources_post"
    post_id = Column(Integer ,primary_key=True)
    title = Column(String , nullable=False)
    description = Column(String , nullable=True)
    http_link = Column(String , nullable=False)
    votes = Column(Integer , nullable=False , default=0)
    created_at = Column(TIMESTAMP , nullable=False ,server_default=text('now()'))
    # modified_at : int ## fix this too
    author_id = Column(Integer , ForeignKey("users.user_id" , ondelete="CASCADE") , nullable=False )
    # tags : dict = {} not_working
    author = relationship("user")


class user(Base):
    __tablename__ = "users"
    user_id = Column(Integer , primary_key=True)
    username = Column(String , nullable=False , unique=True)
    email = Column(String , unique=True , nullable=False)
    password_hashed = Column(String , nullable=False)
    created_at = Column(TIMESTAMP, nullable=False , server_default=text("now()"))


class vote(Base):
    __tablename__ = "votes"
    post_id = Column(Integer ,ForeignKey(column="resources_post.post_id" , ondelete="CASCADE") , primary_key=True)
    user_id = Column(Integer ,ForeignKey(column="users.user_id"           , ondelete="CASCADE") , primary_key=True )
    vote    = Column(Integer, nullable=False)
    __table_args__ = (
        CheckConstraint('vote >= -1 AND vote <= 1 AND vote != 0', name='ck_vote_limit'),
    )


#Base.metadata.create_all(engine)
