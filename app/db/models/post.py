from ..database import Base 
from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP,ForeignKey,ForeignKeyConstraint
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
    votes = Column(Integer,server_default="0",nullable = False)
    owner = relationship("User")