from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter

from app.core import oauth2

from app.db import database
from app.schemas.Users import User_response
from app.db.models.vote import Vote
from app.db.models.users import User
from app.db.models.post import Post
from app.schemas.Votes import Vote
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/votes",
    tags= ["votes"]
)

@router.post("/{id}")
def do_vote(id:int,current_user:User_response = Depends(oauth2.get_current_user),
db:Session=Depends(database.get_db)):
    post:Vote = db.query(Post).filter(Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")

    vote_query = db.query(Vote).filter(Vote.post_id == id,Vote.user_id == current_user.id)
    regist = vote_query.first()

    if not regist:
        data = Vote(user_id = current_user.id,post_id=post.id)
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