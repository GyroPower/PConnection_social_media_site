import base64
import os
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
from PIL import Image
from sqlalchemy.orm import Session

from app.core.config import settings_core
from app.core.oauth2 import get_current_user_by_token
from app.db.database import get_db
from app.db.repository.posts.Posts import create_post
from app.db.repository.posts.Posts import get_posts_with_more_interaction
from app.db.repository.posts.Posts import r_get_post
from app.db.repository.posts.Posts import r_update_post
from app.db.repository.users.Users import get_user_id
from app.db.repository.users.Users import r_get_current_user
from app.db.repository.utils import see_image_type
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

        return templates.TemplateResponse(
            name="main/home_page.html",
            context={
                "request": request,
                "posts": posts.all(),
                "current_user": current_user,
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
        media_dir = None
        media_dir_save = None
        if form.__dict__.get("media").filename != "":
            media_type = str(form.__dict__.get("media").filename)

            media_type = media_type.replace(" ", "-")

            media_dir_save = settings_core.dir_media + f"{current_user.id}"

            if not os.path.exists(media_dir_save):
                os.mkdir(media_dir_save)

            media_dir_save = media_dir_save + f"/{media_type}"

            media_dir = f"{current_user.id}" + f"/{media_type}"

            media = form.__dict__.get("media")

        post_create = {
            "content": form.__dict__.get("content"),
            "media_dir": media_dir,
            "media_dir_save": media_dir_save,
            "media": media,
        }

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


@router.get("/edit-post/{post_id}")
def edit_post(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = r_get_post(db, post_id)

    current_user = r_get_current_user(request, db)

    if current_user.id != post.owner_id:
        return responses.RedirectResponse("/", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse(
        "posts/edit_post.html", context={"request": request, "post": post}
    )


@router.post("/edit-post/{id}")
async def edit_post(request: Request, id: int, db: Session = Depends(get_db)):
    form = post_form(request)

    await form.load_data()
    post = r_get_post(db, id)

    if await form.validate_data():
        current_user: User_response = r_get_current_user(request, db)
        media = None
        media_dir = None
        media_dir_save = None

        if form.__dict__.get("media").filename != "":
            media_type = str(form.__dict__.get("media").filename)

            media_type = media_type.replace(" ", "-")

            media_dir_save = settings_core.dir_media + f"{current_user.id}"

            if not os.path.exists(media_dir_save):
                os.mkdir(media_dir_save)

            media_dir_save = media_dir_save + f"/{media_type}"

            media_dir = f"{current_user.id}" + f"/{media_type}"

            media = form.__dict__.get("media")

        post_update = {
            "content": form.content,
            "media": media,
            "media_dir": media_dir,
            "media_dir_save": media_dir_save,
            "media": media,
        }
        r_update_post(post_update, db, current_user.id, id)

        return responses.RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    else:
        form.__dict__.update({"post": post})
        return templates.TemplateResponse("posts/edit_post.html", form.__dict__)
