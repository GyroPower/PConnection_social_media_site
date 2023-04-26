from pydantic import BaseModel,EmailStr

class Vote(BaseModel):
    post_id : int
     