from fastapi import APIRouter

from app.routers.apis.auth import router as auth
from app.routers.apis.posts import router as posts
from app.routers.apis.users import router as users
from app.routers.apis.votes import router as votes

api_route = APIRouter()
#
api_route.include_router(router=auth, prefix="/login-r", tags=["auth"])
api_route.include_router(router=posts, prefix="/jobs")
api_route.include_router(router=users)
api_route.include_router(router=votes)
