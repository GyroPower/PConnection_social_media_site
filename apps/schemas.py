from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional


class User_base(BaseModel):
    email: EmailStr
    password: str
    phone_number:str


class User_response(BaseModel):
    id: int
    email: EmailStr
    create_at: datetime

    class Config:
        orm_mode = True

class Post_Base(BaseModel):
    title : str
    content : str 
    published : bool = True
    
class Post_create(Post_Base):
    pass 

class Post_response(Post_Base):
    
    create_at: datetime
    owner_id:int
    id: int
    owner: User_response
    class Config:
        orm_mode = True
    

class Token(BaseModel):
    acces_token : str 
    token_type:str
    owner_id:str

class Token_data(BaseModel):
    id: Optional[str] = None

    

    