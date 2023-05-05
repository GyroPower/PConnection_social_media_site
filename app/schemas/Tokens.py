from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr


class Token(BaseModel):
    acces_token: str
    token_type: str
    owner_id: str


class Token_data(BaseModel):
    id: Optional[str] = None
