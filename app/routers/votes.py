from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import oauth2,database,models,schemas
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/votes",
    tags= ["votes"]
)

@router.post("/{id}")
def do_vote(id:int,current_user:int = Depends(oauth2.get_current_user),
db:Session=Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == id,models.Vote.user_id == current_user.id)
    regist = vote_query.first()

    if not regist:
        data = models.Vote(user_id = current_user.id,post_id=post.id)
        db.add(data)
        db.commit()
        post.votes +=1
        db.add(post)
        db.commit()
        return {"msg":"Liked"}
    else:
        post.votes -=1
        db.add(post)
        db.commit()
        vote_query.delete()
        db.commit()
        return {"msg":"Unliked"}