from jose import JWTError,jwt
from datetime import datetime, timedelta
from . import schemas,database,models
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

#SECRET_KEY
#ALGORITHM
#EXPERIATION_TIME

SECRET_KEY = settings.secret_key

ALGORITHM = settings.algorithm
ACCES_TOKEN_EXPIRE_MINUTES = settings.acces_token_expire_minutes 

def create_acces_toke(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encode_jwt
#verify if the token given is authorized and the user can acces to the data related of 
#the id given in the token
def verify_acces_token(token:str, credentials_exception):
    try:
        #decode expects a list of algorithms
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])

        id :str = payload.get("user_id")

        #make sure there is a id 
        if id is None:
            raise credentials_exception

        token_data = schemas.Token_data(id=id)
    #if the given token is not authorized, if it was manipulate, it will raise an error
    #explaining the credentials are no valid
    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth2_schema),db: Session = Depends(database.get_db)):
    credenrials_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"Could not validate credentials",headers={"WWW-Authenticate": "Bearer"})

    token = verify_acces_token(token,credenrials_exceptions)
    user= db.query(models.User).filter(models.User.id==token.id).first()

    return user