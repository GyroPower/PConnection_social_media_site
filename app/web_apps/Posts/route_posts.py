from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.oauth2 import get_current_user_by_token
from app.db.database import get_db
from app.db.repository.posts.Posts import create_post
from app.db.repository.posts.Posts import get_posts_with_more_interaction
from app.web_apps.Posts.form import post_form

router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def home(request: Request, db: Session = Depends(get_db), msg: str = None):
    token = request.cookies.get("access_token")

    msg = None
    posts = get_posts_with_more_interaction(db=db)
    try:

        current_user = get_current_user_by_token(token=token, db=db)

        if current_user:
            msg = current_user.email

    finally:
        return templates.TemplateResponse(
            name="main/home_page.html",
            context={"request": request, "posts": posts.all(), "msg": msg},
        )


@router.get("/create-post")
def create(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return responses.RedirectResponse("/login/", status_code=status.HTTP_302_FOUND)

    current_user = get_current_user_by_token(token=token, db=db)

    if current_user:

        return templates.TemplateResponse(
            name="posts/create_post.html",
            context={"request": request, "user": current_user},
        )
    else:
        return responses.RedirectResponse("/login/", status_code=status.HTTP_302_FOUND)
