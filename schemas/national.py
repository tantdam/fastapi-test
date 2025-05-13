from typing import Optional

from pydantic import BaseModel

class NationalCreate(BaseModel):
    name: str

class NationalRead(NationalCreate):
    id: int

    class Config:
        from_attributes = True

class NationalUpdate(BaseModel):
    name: Optional[str] = None
