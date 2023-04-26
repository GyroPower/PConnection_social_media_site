from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional


class Token(BaseModel):
    acces_token : str 
    token_type:str
    owner_id:str

class Token_data(BaseModel):
    id: Optional[str] = None