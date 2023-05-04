from datetime import datetime
from datetime import timedelta

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt
from jose import JWTError
from sqlalchemy.orm import Session

from .config import settings_core
from app.core.utils import OAuth2PasswordBearerWithCookie
from app.db.database import get_db
from app.db.models.users import User
from app.schemas import Tokens

oauth2_schema = OAuth2PasswordBearerWithCookie(tokenUrl="/token")

# SECRET_KEY
# ALGORITHM
# EXPERIATION_TIME

SECRET_KEY = settings_core.secret_key

ALGORITHM = settings_core.algorithm
ACCES_TOKEN_EXPIRE_MINUTES = settings_core.acces_token_expire_minutes


def create_acces_toke(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


# verify if the token given is authorized and the user can acces to the data related of
# the id given in the token
def verify_acces_token(token: str, credentials_exception):
    try:
        # decode expects a list of algorithms
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        # make sure there is a id
        if id is None:
            raise credentials_exception

        token_data = Tokens.Token_data(id=id)
    # if the given token is not authorized, if it was manipulate, it will raise an error
    # explaining the credentials are no valid
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_schema), db: Session = Depends(get_db)
):
    credenrials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_acces_token(token, credenrials_exceptions)
    user = db.query(User).filter(User.id == token.id).first()

    return user


def get_current_user_by_token(token: str, db: Session):
    credenrials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    scheme, param = get_authorization_scheme_param(token)
    if not token or scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not authenticate"
        )
    user_id = verify_acces_token(
        token=param, credentials_exception=credenrials_exceptions
    )

    return db.query(User).filter(User.id == user_id.id).first()
