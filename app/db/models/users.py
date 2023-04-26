from ..database import Base 
from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP,ForeignKey,ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from app.db.repository.utils import random_username

random = random_username


class User(Base):

    __tablename__ = "users"
    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    username = Column(String,nullable=True)
    create_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('NOW()'))
