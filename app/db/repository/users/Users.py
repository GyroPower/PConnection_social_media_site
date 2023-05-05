from typing import Optional

from fastapi import Request
from sqlalchemy.orm import Session

from app.core.Hashing import password_hash
from app.core.oauth2 import get_current_user_by_token
from app.db.models.users import User
from app.db.repository.utils import random_username
from app.schemas.Users import User_base
from app.schemas.Users import User_change_email
from app.schemas.Users import User_response
from app.schemas.Users import User_change_password


def create_user(new_user: User_base, db: Session):
    new_user.password = password_hash(new_user.password)

    if new_user.username == "":
        new_user.username = random_username(new_user.email)

    user = User(**new_user.__dict__)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(email: str, db: Session):

    return db.query(User).filter(User.email == email).first()


def get_users(username: str, db: Session):

    return db.query(User).filter(User.username.contains(username))


def get_user_id(id: int, db: Session):

    return db.query(User).filter(User.id == id).first()


def r_update_user(id: int, updated_info: User_response, db: Session):
    user = db.query(User).filter(User.id == id)

    user.update(updated_info.dict(), synchronize_session=False)
    db.commit()
    return user.first()


def get_current_user(request: Request, db: Session):

    token = request.cookies.get("access_token")
    
    return get_current_user_by_token(token=token, db=db)


def r_update_email(id: int, updated_email: User_change_email, db: Session):

    user = db.query(User).filter(User.id == id)
    user.update(updated_email.dict())
    db.commit()
    return user.first()


def r_change_password(change_pass:User_change_password,db:Session,id:int):
    
    user = db.query(User).filter(User.id == id)
    user.update(change_pass.dict())
    db.commit() 
    