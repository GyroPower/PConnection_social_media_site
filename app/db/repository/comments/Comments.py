from sqlalchemy.orm import Session

from app.db.models.comments import Comments


def comment_post(comment, post_id: int, user_id: int, db: Session):

    new_comment = Comments(
        content=comment["content"], owner_id=user_id, post_owner_id=post_id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def get_comments_for_a_post(post_id: int, db: Session):

    comments = (
        db.query(Comments)
        .filter(Comments.post_owner_id == post_id)
        .order_by(Comments.create_at.desc())
    )

    return comments.all()
