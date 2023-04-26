from typing import Optional 
from sqlalchemy.orm import Session 
from app.db.models.users import User
from app.schemas.Users import User_base
from app.schemas.Users import User_response
from app.core.Hashing import password_hash

def create_user(new_user:User_base,db:Session):
    new_user.password = password_hash(new_user.password)
    
    db.add(new_user)
    db.commit()
    db.refresh()
    return new_user 

def get_user_by_email(email:str,db:Session):
    
    return db.query(User).filter(User.email==email).first()
    
def get_users(username:str,db:Session):
    
    return db.query(User).filter(User.username.contains(username))

def get_user_id(id:int, db:Session):
    
    return db.query(User).filter(User.id==id).first()