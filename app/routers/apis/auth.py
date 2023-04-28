from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...db.database import get_db
from app.core import Hashing
from app.core.oauth2 import create_acces_toke
from app.db.repository.users.Users import get_user_by_email
from app.schemas.Tokens import Token
from app.schemas.Users import User_login
from app.schemas.Users import User_verify

router = APIRouter(tags=["Authentication"])


@router.post("/token", response_model=Token)
def login_user(
    response: Response,
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user: User_verify = get_user_by_email(user_credentials.username, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )

    if not Hashing.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )

    # create a token
    acces_token = create_acces_toke(data={"user_id": user.id})
    # return token
    response.set_cookie(
        key="access_token", value=f"bearer {acces_token}", httponly=True
    )
    return {"acces_token": acces_token, "token_type": "bearer"}


def set_cookie_after_signup(
    user: User_login, response: Response, db: Session = Depends(get_db)
):
    user_v: User_verify = get_user_by_email(email=user.email, db=db)

    # create a token
    acces_token = create_acces_toke(data={"user_id": user_v.id})
    # return token
    response.set_cookie(
        key="access_token", value=f"bearer {acces_token}", httponly=True
    )
    return {"acces_token": acces_token, "token_type": "bearer"}
