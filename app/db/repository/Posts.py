from app.db.models.post import Post
from sqlalchemy.orm import Session 

def get_posts_with_more_interaction(db:Session):
    
    post = db.query(Post)
    
    return post