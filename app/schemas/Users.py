from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional


class User_base(BaseModel):
    email: EmailStr
    password: str
    #phone_number:str


class User_response(BaseModel):
    id: int
    email: EmailStr
    create_at: datetime

    class Config:
        orm_mode = True
class User_verify(BaseModel):
    id:int 
    email:EmailStr
    password:str