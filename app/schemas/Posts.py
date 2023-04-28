from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr

from .Users import User_response


class Post_Base(BaseModel):
    content: str
    media: str


class Post_create(Post_Base):
    pass


class Post_response(Post_Base):

    create_at: datetime
    owner_id: int
    id: int
    owner: User_response
    votes: int

    class Config:
        orm_mode = True
