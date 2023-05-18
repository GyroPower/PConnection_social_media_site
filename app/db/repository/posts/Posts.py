import os
import pickle

from PIL import Image
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

    if post["media"]:

        img = Image.open(post["media"].file)

        img.save(post["media_dir_save"])

    post_create = Post(
        content=post["content"], media_dir=post["media_dir"], owner_id=user_id
    )
    db.add(post_create)
    db.commit()
    db.refresh(post_create)

    return post


def get_posts_own_by_user(db: Session, owner_id):
    return (
        db.query(Post).filter(Post.owner_id == owner_id).order_by(Post.create_at.desc())
    )


def r_get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def r_update_post(post, db: Session, user_id: int, post_id: int):

    post_query = (
        db.query(Post).filter(Post.id == post_id).filter(Post.owner_id == user_id)
    )
    post_old = post_query.first()

    print(post_old.media_dir)

    posts_with_same_media = (
        db.query(Post)
        .filter(Post.media_dir == post_old.media_dir, Post.id != post_old.id)
        .all()
    )

    if post["media"]:
        if post_old.media_dir != None and len(posts_with_same_media) == 0:
            os.remove("media/" + post_old.media_dir)

        img = Image.open(post["media"].file)
        img.save(post["media_dir_save"])
    else:
        post["media_dir"] = post_old.media_dir

    post_query.update(
        {Post.content: post["content"], Post.media_dir: post["media_dir"]},
        synchronize_session=False,
    )

    db.commit()
    return post_query.first()
