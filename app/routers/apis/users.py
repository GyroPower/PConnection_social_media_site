from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from sqlalchemy.orm import Session

from ...db.database import get_db
from app.core import Hashing
from app.db.repository.users.Users import create_user
from app.db.repository.users.Users import get_users
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


@router.get("/search")
def search_users(username: str, db: Session = Depends(get_db)):

    users: User_response = get_users(username, db)


@router.get("/{id}", response_model=User_response)
def get_user_info(id: int, db: Session = Depends(get_db)):

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found"
    )
