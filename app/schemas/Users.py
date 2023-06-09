from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr


class User_base(BaseModel):
    email: EmailStr
    username: str = ""
    password: str
    description: str = ""
    # phone_number:str


class User_response(BaseModel):
    id: int
    username: str
    email: EmailStr
    description: str
    create_at: datetime

    class Config:
        orm_mode = True


class User_login(BaseModel):
    email = EmailStr
    password = str


class User_verify(BaseModel):
    id: int
    email: EmailStr
    password: str


class User_change_email(BaseModel):
    email: EmailStr

class User_change_password(BaseModel):
    password: str 