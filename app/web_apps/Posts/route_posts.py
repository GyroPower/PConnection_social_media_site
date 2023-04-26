from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from fastapi import Depends
from app.core.oauth2 import get_current_user
from fastapi.security.utils import get_authorization_scheme_param
from app.db.repository.Posts import get_posts_with_more_interaction

router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def home(request:Request,db:Session=Depends(get_db)):
    token = request.cookies.get("acces_token")
    print(token)
    msg= None 
    posts = get_posts_with_more_interaction(db=db)
    if not token:
        msg = "no user"
    else:
        
        current_user = get_current_user(token=token)
    
    return templates.TemplateResponse(
        name="main/home_page.html",context={"request":request,"posts":posts.all()}
    )