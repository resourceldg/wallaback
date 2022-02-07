from typing import Optional
from pydantic import BaseModel
 
class User(BaseModel):
    id: Optional[str]
    name: Optional[str]
    email: str
    password: str
    jwtToken:Optional[str]
