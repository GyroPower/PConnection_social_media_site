from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import schemas,models,utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.User_response)
def create_user(user_created: schemas.User_base,db:Session = Depends(get_db)):
    #hash the password - user_created.password

    hash_pwd = utils.password_hash(user_created.password)
    user_created.password = hash_pwd

    user = models.User(**user_created.dict())

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get("/{id}",response_model=schemas.User_response)
def get_user(id:int,db:Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if user is not None:
        return user 

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id: {id} not found")


