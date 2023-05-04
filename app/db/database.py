from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..core.config import settings_core

#this variable is for connect with our database with sqlalchemy
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings_core.database_username}:{settings_core.database_password}@{settings_core.database_hostname}:{settings_core.database_port}/{settings_core.database_name}'
#we need to create an engine to connect with the database we want 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#to talk with a database we need to create a session 

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db 
    finally:
        db.close() 
