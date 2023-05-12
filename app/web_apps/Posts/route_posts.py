import base64
import shutil
from typing import Optional

import psycopg2
from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi import UploadFile
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.oauth2 import get_current_user_by_token
from app.db.database import get_db
from app.db.repository.posts.Posts import create_post
from app.db.repository.posts.Posts import get_posts_with_more_interaction
from app.db.repository.posts.Posts import r_get_post
from app.db.repository.users.Users import get_current_user
from app.db.repository.users.Users import get_user_id
from app.schemas.Posts import Post_create
from app.schemas.Users import User_response
from app.web_apps.Posts.form import post_form

router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def home(request: Request, db: Session = Depends(get_db), msg: str = None):
    token = request.cookies.get("access_token")

    current_user = None
    posts = get_posts_with_more_interaction(db=db)
    try:

        current_user = get_current_user_by_token(token=token, db=db)

        if current_user:
            user: User_response = current_user

    finally:
        users = []
        for post in posts:
            user = get_user_id(post.owner_id, db)
            post.username = user.username

            if post.media:
                image = base64.b64encode(post.media)
                post.media = image.decode()

        return templates.TemplateResponse(
            name="main/home_page.html",
            context={
                "request": request,
                "posts": posts.all(),
                "current_user": current_user,
                "image": image,
            },
        )


@router.get("/create-post/")
def create(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return responses.RedirectResponse("/login/", status_code=status.HTTP_302_FOUND)

    try:
        current_user = get_current_user_by_token(token=token, db=db)

        return templates.TemplateResponse(
            name="posts/create_post.html", context={"request": request}
        )
    except HTTPException:
        return responses.RedirectResponse("/login/", status_code=status.HTTP_302_FOUND)


@router.post("/create-post/")
async def create(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")

    form = post_form(request)

    await form.load_data()

    try:

        current_user: User_response = get_current_user_by_token(token=token, db=db)

        if not await form.validate_data():
            return templates.TemplateResponse(
                name="posts/create_post.html",
                context={
                    "request": request,
                    "error": "Shut have a text o media file in the post",
                },
            )

        media = None
        if form.__dict__.get("media"):
            media = await form.__dict__.get("media").read()

        post_create = {"content": form.__dict__.get("content"), "media_dir": media}
        create_post(post_create, db=db, user_id=current_user.id)

        return responses.RedirectResponse("/", status_code=status.HTTP_302_FOUND)

    except HTTPException:
        return templates.TemplateResponse(
            name="posts/create_post.html",
            context={
                "request": request,
                "error": "Error to validate credential of user",
            },
        )


@router.get("/boopstrap")
def example(request: Request):

    return templates.TemplateResponse(
        name="votes/boopstrap.html", context={"request": request}
    )


@router.get("/edit-post/{id}")
def edit_post(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = r_get_post(db, post_id)

    current_user = get_current_user(request, db)

    if current_user.id == post.owner_id:
        return responses.RedirectResponse("/", status_code=status.HTTP_302_FOUND)


@router.get("/test")
def test(request: Request):
    return templates.TemplateResponse("votes/test.html", context={"request": request})


@router.post("/edit-post/{id}")
async def edit_post(request: Request, id: int, db: Session = Depends(get_db)):
    form = post_form(request)

    await form.load_data()

    try:
        current_user: User_response = get_current_user(request, db)

        post_update = Post_create(form.content, form.media)

    except:
        pass
