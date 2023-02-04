from .database import Base 
from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable = False)
    published = Column(Boolean,server_default="TRUE",nullable=False)
    create_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('NOW()'))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

    owner = relationship("User")

class User(Base):

    __tablename__ = "users"
    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    create_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('NOW()'))

