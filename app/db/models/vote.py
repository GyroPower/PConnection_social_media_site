from ..database import Base 
from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP,ForeignKey,ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)