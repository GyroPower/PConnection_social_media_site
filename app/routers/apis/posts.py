from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from sqlalchemy.orm import Session

from ...db.database import get_db
from app.core.oauth2 import get_current_user
from app.db.models.post import Post
from app.schemas.Posts import Post_create
from app.schemas.Posts import Post_response

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/own", response_model=List[Post_response])
def gets_posts(
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    title: Optional[str] = "",
):

    posts = (
        db.query(Post)
        .filter(Post.owner_id == current_user.id)
        .filter(Post.title.contains(title))
        .limit(limit)
        .offset(skip)
        .all()
    )
    print(posts)

    return posts


@router.get("/{id}", response_model=Post_response)
async def gets_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
    title: Optional[str] = "",
):

    # cursor.execute("""SELECT * FROM posts where id=(%s)""",(str(id)))
    # post = cursor.fetchone()
    post = (
        db.query(Post).filter(Post.id == id).filter(Post.title.contains(title)).first()
    )
    # with filter we pass the field what we want to filter and with first we say we want the
    # firts one who have the same coincidence

    if post is not None:
        return post

    # response.status_code = status.HTTP_404_NOT_FOUND

    # return {"message": f"post with id: {id} not found"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found"
    )


@router.get("/", response_model=List[Post_response])
async def gets_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
    title: Optional[str] = "",
):

    posts = (
        db.query(Post)
        .filter(Post.published == True)
        .filter(Post.title.contains(title))
        .offset(skip)
        .limit(limit)
        .all()
    )

    return posts


# Body it's goin to extract all the fields of the json recived and convert into
# a python dict and store it into message variable

# To change a status code in the decorator we pass by parameter the status code
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post_response)
async def create_post(
    new_post: Post_create,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    # with .dict we can convert a pydamic instance to a dictionary and use it to send a json
    # cursor.execute("""INSERT INTO posts (title,content,published)
    # VALUES (%s,%s,%s) RETURNING *""",(new_post.title,new_post.content,new_post.published))
    # conn.commit()
    # data = cursor.fetchone()

    pass


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):

    # cursor.execute("""DELETE FROM posts where id = %s""",(str(id)))

    # post = cursor.rowcount

    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()

    if post is not None:
        if post.owner_id == current_user.id:

            post_query.delete(synchronize_session=False)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unauthorized action, this post don't belong to user with id:{current_user.id}",
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found"
    )


@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=Post_response)
def update(
    id: int,
    update_post: Post_create,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""",
    # (update_post.title,update_post.content,str(id)))

    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()
    print(post.id, post.title)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unauthorized,this post don't belong to te current user",
        )

    post_query.update(update_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
