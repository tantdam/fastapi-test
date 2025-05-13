from pydantic import BaseModel
from typing import Optional, List


class PlayerCreate(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    age: int
    current_club: int
    national_team: int
    position: str
    previous_clubs: Optional[List[int]] = []

class PlayerRead(PlayerCreate):
    id: int

    class Config:
        from_attributes = True

class PlayerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    age: Optional[int] = None
    current_club: Optional[int] = None
    national_team: Optional[int] = None
    position: Optional[str] = None
    previous_clubs: Optional[List[int]] = []
