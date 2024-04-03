from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True)
  username = Column(String, nullable=False)
  email = Column(String, unique=True, index=True)
  password = Column(String, nullable=False)
  is_active = Column(Boolean, server_default="TRUE")
  created_at= Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

#items = relationship("Item", back_populates="owner")

#sqlalchemy will check if a table called posts&users exists in the db if yes it will not create them otherwise it will create them but it can not modify existing tables
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE")
    created_at= Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class Vote(Base):
   __tablename__="votes"
   user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
   post_id=Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)