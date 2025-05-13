from typing import Optional

from sqlalchemy.orm import Session

from models.national import National
from schemas import NationalCreate, NationalUpdate


def create_national(db: Session, national: NationalCreate) -> National:
    db_national = National(**national.model_dump())
    db.add(db_national)
    db.commit()
    db.refresh(db_national)
    return db_national

def read_national(db: Session, national_id: int) -> Optional[National]:
    return db.query(National).filter(National.id == national_id).first()

def update_national(db: Session, national_id: int, national: NationalUpdate) -> bool:
    existing_national = read_national(db, national_id)
    if existing_national is None: return False
    for key, value in national.model_dump().items():
        if value:
            setattr(existing_national, key, value)
    db.commit()
    db.refresh(existing_national)
    return True

def delete_national(db: Session, national_id: int) -> bool:
    existing_national = read_national(db, national_id)
    if existing_national is None: return False
    db.delete(existing_national)
    db.commit()
    return True