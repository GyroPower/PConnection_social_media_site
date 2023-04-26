from fastapi import APIRouter
from app.web_apps.Posts.route_posts import router as posts_app 

api_router = APIRouter(prefix="",include_in_schema=False)

api_router.include_router(router=posts_app,prefix="")