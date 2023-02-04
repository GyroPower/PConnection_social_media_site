from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#this variable is for connect with our database with sqlalchemy
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:16062016JustifyMy@localhost/FastAPI'
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
