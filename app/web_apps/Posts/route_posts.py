import psycopg2
import base64
import shutil

from fastapi import APIRouter, File, Form
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi import UploadFile
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from app.core.oauth2 import get_current_user_by_token
from app.db.repository.users.Users import get_user_id
from app.db.database import get_db
from app.db.repository.posts.Posts import create_post
from app.db.repository.posts.Posts import get_posts_with_more_interaction
from app.schemas.Posts import Post_create
from app.schemas.Users import User_response
from app.web_apps.Posts.form import post_form

router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def home(request: Request, db: Session = Depends(get_db), msg: str = None):
    token = request.cookies.get("access_token")

    user = None
    posts = get_posts_with_more_interaction(db=db)
    try:

        current_user = get_current_user_by_token(token=token, db=db)

        if current_user:
            user: User_response = current_user

    finally:
        
        for post in posts.all():
            user = get_user_id(post.owner_id,db)
            post.__dict__.update({"username":user.username})
            if post.media:
                image = base64.b64encode(post.media)
                post.media = image.decode()
        
        return templates.TemplateResponse(
            name="main/home_page.html",
            context={"request": request, "posts": posts.all(), "user": user,"image":image},
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
        
        
        post_create = {"content":form.__dict__.get("content"),"media_dir":media}
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
