from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import oauth2,database,models,schemas
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/votes",
    tags= ["votes"]
)

@router.post("/")
def votes(vote:schemas.vote,current_user:int = Depends(oauth2.get_current_user),
db:Session=Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {vote.post_id} not found")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id)
    regist = vote_query.first()

    print(current_user.id)
    if vote.liked == 1:
        if not regist:
            
            data = models.Vote(user_id = current_user.id,post_id=vote.post_id)

            db.add(data)
            db.commit() 
            db.refresh(data)
        
            return {"message":"Successfully added vote"}
        else:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail=f"Alredy liked this post")


    elif vote.liked == 0:


        if not regist:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail=f"Alredy unliked post")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"Successfully deleted vote"}
