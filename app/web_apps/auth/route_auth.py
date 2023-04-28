from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .form import form_login_user
from app.db.database import get_db
from app.routers.apis.auth import login_user

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(include_in_schema=False)


@router.get("/login/")
def login(request: Request):

    return templates.TemplateResponse(
        name="users/login.html", context={"request": request}
    )


@router.post("/login/")
async def login(request: Request, db: Session = Depends(get_db)):
    form = form_login_user(request)

    await form.load_data()

    if await form.is_valid():
        try:

            form.__dict__.update(msg="Login successfully :)")
            response = responses.RedirectResponse(
                "/?msg=Login-success", status_code=status.HTTP_302_FOUND
            )
            login_user(user_credentials=form, response=response, db=db)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Invalid email or password")
            return templates.TemplateResponse(
                name="users/login.html", context=form.__dict__
            )
    return templates.TemplateResponse(name="users/login.html", context=form.__dict__)
