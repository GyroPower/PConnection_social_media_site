import base64

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi import responses
from fastapi import status
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings_core
from app.core.Hashing import password_hash
from app.core.Hashing import verify_password
from app.db.database import get_db
from app.db.repository.posts.Posts import get_posts_own_by_user
from app.db.repository.users.Users import create_user
from app.db.repository.users.Users import get_current_user
from app.db.repository.users.Users import get_user_id
from app.db.repository.users.Users import r_change_password
from app.db.repository.users.Users import r_update_email
from app.db.repository.users.Users import r_update_user
from app.routers.apis.auth import set_cookie_after_signup
from app.schemas.Users import User_base
from app.schemas.Users import User_change_email
from app.schemas.Users import User_change_password
from app.schemas.Users import User_response
from app.web_apps.Users.form import change_email
from app.web_apps.Users.form import change_password_form
from app.web_apps.Users.form import create_user_form
from app.web_apps.Users.form import update_user

router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="app/templates")


@router.get("/signup/")
def sigup(request: Request):

    return templates.TemplateResponse(
        name="users/register.html", context={"request": request}
    )


@router.post("/signup/")
async def sigup(request: Request, db: Session = Depends(get_db)):

    form = create_user_form(request)

    await form.load_data()

    if await form.is_valid():
        try:

            user = User_base(
                email=form.__dict__.get("email"),
                username=form.__dict__.get("username"),
                password=form.__dict__.get("password"),
            )

            user_created = create_user(user, db)

            """directory = f"{user_created.id}"
            path = os.path.join(settings_core.dir_media+"media/",directory)
            os.mkdir(path)"""

            response = responses.RedirectResponse(
                "/?msg=Login-Success", status_code=status.HTTP_302_FOUND
            )
            set_cookie_after_signup(user_created, response, db)
            return response

        except IntegrityError:
            form.__dict__.get("errors").append("The email is alredy registered")
            return templates.TemplateResponse(
                "users/register.html", context=form.__dict__
            )

    return templates.TemplateResponse("users/register.html", context=form.__dict__)


@router.get("/user-info/{id}")
def user_info(request: Request, db: Session = Depends(get_db), id: int = None):

    current_user = None

    try:
        current_user = get_current_user(request, db)

    finally:
        user: User_response = get_user_id(id=id, db=db)
        posts = get_posts_own_by_user(db, id)

        for post in posts:

            post.username = user.username
            if post.media:
                media = base64.b64encode(post.media)
                post.media = media.decode()

        for post in posts:

            post.__dict__.update({"username": user.username})

        return templates.TemplateResponse(
            name="users/user_info.html",
            context={
                "request": request,
                "user": user,
                "current_user": current_user,
                "posts": posts,
            },
        )


@router.get("/settings/")
def settings(request: Request, db: Session = Depends(get_db)):

    try:
        current_user = current_user = get_current_user(request, db)

        return templates.TemplateResponse(
            "users/edit_user.html",
            context={"request": request, "user_info": current_user},
        )
    except HTTPException:
        return responses.RedirectResponse("/login/", status_code=status.HTTP_302_FOUND)


@router.post("/settings/")
async def settings(request: Request, db: Session = Depends(get_db)):

    form = update_user(request)
    await form.load_data()

    try:
        current_user: User_response = get_current_user(request, db)

        if await form.is_valid() == False:
            form.username = current_user.username
        current_user.__dict__.update(form.__dict__)
        user = User_response(**current_user.__dict__)

        r_update_user(user.id, user, db)

        return responses.RedirectResponse(
            f"/user-info/{user.id}", status_code=status.HTTP_302_FOUND
        )

    except HTTPException:
        return templates.TemplateResponse(
            "users/edit_user.html",
            context={"request": request, "error": "An error occurs"},
        )


@router.get("/change-email/")
def change_email_user(request: Request, db: Session = Depends(get_db)):

    try:
        current_user = get_current_user(request, db)

        return templates.TemplateResponse(
            name="users/change_email.html",
            context={"request": request, "user": current_user},
        )
    except HTTPException:
        return responses.RedirectResponse("/login/", status_code=status.HTTP_302_FOUND)


@router.post("/change-email/")
async def change_email_user(request: Request, db: Session = Depends(get_db)):

    form = change_email(request=request)
    current_user = get_current_user(request=request, db=db)

    await form.load_data()

    if await form.is_valid():
        try:

            if not verify_password(form.password, current_user.password):
                form.__dict__.get("errors").append("Incorrect password")
                form.__dict__.update({"user": current_user})

                return templates.TemplateResponse(
                    "users/change_email.html", context=form.__dict__
                )
            update_email = User_change_email(email=form.__dict__.get("new_email"))

            r_update_email(current_user.id, update_email, db)

            return responses.RedirectResponse(
                f"/user-info/{current_user.id}", status_code=status.HTTP_302_FOUND
            )
        except IntegrityError:
            return templates.TemplateResponse(
                "users/change_email.html",
                context={
                    "request": request,
                    "errors": "A user with this email alredy exists",
                    "user": current_user,
                },
            )
    form.__dict__.update({"user": current_user})
    print(form.__dict__.get("user"))
    return templates.TemplateResponse("users/change_email.html", form.__dict__)


@router.get("/change-password/")
def change_password(request: Request, db: Session = Depends(get_db)):

    try:
        current_user = get_current_user(request, db)

        return templates.TemplateResponse(
            "users/change_password.html", {"request": request}
        )
    except HTTPException:
        return responses.RedirectResponse("/login/", status_code=status.HTTP_302_FOUND)


@router.post("/change-password/")
async def change_password(request: Request, db: Session = Depends(get_db)):

    form = change_password_form(request)
    await form.load_data()

    if await form.is_valid():

        try:
            current_user = get_current_user(request, db)

            if not verify_password(form.current_password, current_user.password):
                form.__dict__.get("errors").append("Incorrect password")

                return templates.TemplateResponse(
                    "users/change_password.html", form.__dict__
                )

            hashed_pass = password_hash(form.new_password)

            new_password = User_change_password(password=hashed_pass)

            r_change_password(new_password, db, current_user.id)

            return responses.RedirectResponse(
                f"/user-info/{current_user.id}", status_code=status.HTTP_302_FOUND
            )

        except IntegrityError:

            form.__dict__.get("errors").append(
                """An error occurs in the server, try again, if
                                               the error persist contanct us """
            )
            return templates.TemplateResponse(
                "users/change_password.html", form.__dict__
            )

    return templates.TemplateResponse("users/change_password.html", form.__dict__)


@router.get("/logout")
def logout(request: Request, response: Response):

    try:

        response = responses.RedirectResponse("/", status_code=status.HTTP_302_FOUND)
        response.delete_cookie("access_token")
        return response
    except:
        return responses.RedirectResponse("/", status_code=status.HTTP_302_FOUND)
