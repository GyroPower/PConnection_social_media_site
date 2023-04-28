from fastapi import APIRouter

from app.web_apps.auth.route_auth import router as auth_app
from app.web_apps.Posts.route_posts import router as posts_app
from app.web_apps.Users.route_users import router as users_app

api_router = APIRouter(prefix="", include_in_schema=False)

api_router.include_router(router=posts_app, prefix="")
api_router.include_router(router=auth_app, prefix="")
api_router.include_router(router=users_app, prefix="")
