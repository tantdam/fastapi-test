from bson import ObjectId
from pydantic import BaseModel, Field
from mongoutils import MyObjectId


class NationalCreate(BaseModel):
    name: str

class NationalRead(NationalCreate):
    id: MyObjectId = Field(alias="_id")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

class NationalUpdate(NationalRead):
    pass

class NationalDelete(NationalRead):
    pass