from typing import Optional

from pydantic import BaseModel

class ClubCreate(BaseModel):
    name: str
    city: str
    country: str
    league: str
    
class ClubRead(ClubCreate):
    id: int

    class Config:
        from_attributes = True

class ClubUpdate(BaseModel):
    club_name: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    league: Optional[str] = None