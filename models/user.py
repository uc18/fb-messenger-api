from typing import Any
from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str 
    cookies: Any