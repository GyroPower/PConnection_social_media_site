from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from sqlalchemy.orm import Session

from app.core import oauth2
from app.db import database
from app.db.models.post import Post
from app.db.models.users import User
from app.db.models.vote import Votes
from app.schemas.Users import User_response
from app.schemas.Votes import Vote

router = APIRouter(prefix="/votes", tags=["votes"])


@router.post("/{id}")
def do_vote(
    id: int,
    current_user: User_response = Depends(oauth2.get_current_user),
    db: Session = Depends(database.get_db),
):
    post = db.query(Post).filter(Post.id == id)

    current_post = post.first()
    if not current_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    vote_query = db.query(Votes).filter(
        Votes.post_id == id, Votes.user_id == current_user.id
    )
    regist = vote_query.first()

    if not regist:
        data = Votes(user_id=current_user.id, post_id=current_post.id)
        db.add(data)
        db.commit()
        up_post = post.first()
        up_post.votes += 1
        new_up_post = {"votes": up_post.votes}
        post.update(new_up_post)

        db.commit()
        return {"vote": up_post.votes}
    else:
        down_post = post.first()
        down_post.votes -= 1
        new_down_post = {"votes": down_post.votes}
        post.update(new_down_post)
        db.commit()
        vote_query.delete()
        db.commit()
        return {"vote": down_post.votes}
