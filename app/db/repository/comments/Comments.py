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
