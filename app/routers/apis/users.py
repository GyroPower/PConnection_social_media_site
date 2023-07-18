from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi import status
from sqlalchemy.orm import Session

from ...db.database import get_db
from app.core import Hashing
from app.db.repository.users.Users import create_user
from app.db.repository.users.Users import get_users
from app.db.repository.users.Users import r_get_current_user
from app.db.repository.users.Users import r_get_users_query
from app.schemas.Users import User_base
from app.schemas.Users import User_response

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User_response)
def create_user(user_created: User_base, db: Session = Depends(get_db)):
    # hash the password - user_created.password

    hash_pwd = Hashing.password_hash(user_created.password)
    user_created.password = hash_pwd
    user = create_user(user_created=user_created, db=db)
    return user


@router.get("/autocomplete")
def search_users(term: Optional[str] = None, db: Session = Depends(get_db)):

    users: User_response = r_get_users_query(db, term)

    users_usernames = []

    for user in users:
        print(user.username)
        users_usernames.append(user.username)

    return users_usernames


@router.get("/{id}", response_model=User_response)
def get_user_info(id: int, db: Session = Depends(get_db)):

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found"
    )


@router.get("/")
def current_user_in_session(request: Request, db: Session = Depends(get_db)):

    current_user: User_response = r_get_current_user(request, db)

    return {"user_id": str(current_user.id)}
