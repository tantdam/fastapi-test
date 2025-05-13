from typing import Optional

from pydantic import BaseModel
from models.user import RoleEnum

class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[RoleEnum] = RoleEnum.user

class UserRead(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class UserUpdate(UserCreate):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str
