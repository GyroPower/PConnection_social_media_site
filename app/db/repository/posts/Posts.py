from sqlalchemy.orm import Session

from app.db.models.post import Post
from app.db.models.users import User
from app.schemas.Posts import Post_Base


def get_posts_with_more_interaction(db: Session):

    post = (
        db.query(Post)
        .join(User, Post.owner_id == User.id)
        .order_by(Post.create_at.desc())
    )

    return post


def create_post(post, db: Session, user_id: int):

    post_create = Post(
        content=post["content"], media=post["media_dir"], owner_id=user_id
    )

    db.add(post_create)
    db.commit()
    db.refresh(post_create)

    return post


def get_posts_own_by_user(db: Session, owner_id):
    return (
        db.query(Post).filter(Post.owner_id == owner_id).order_by(Post.create_at.desc())
    )
