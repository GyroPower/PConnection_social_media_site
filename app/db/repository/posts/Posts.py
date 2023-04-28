from sqlalchemy.orm import Session

from app.db.models.post import Post
from app.schemas.Posts import Post_Base


def get_posts_with_more_interaction(db: Session):

    post = db.query(Post)

    return post


def create_post(post: Post_Base, db: Session, user_id: int):

    post_create = Post(**post, owner_id=user_id)

    db.add(post_create)
    db.commit()
    db.refresh(post_create)

    return post
