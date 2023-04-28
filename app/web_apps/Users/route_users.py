from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.repository.users.Users import create_user
from app.routers.apis.auth import set_cookie_after_signup
from app.schemas.Users import User_base
from app.web_apps.Users.form import create_user_form

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
