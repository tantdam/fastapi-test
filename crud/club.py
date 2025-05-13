from typing import Optional

from sqlalchemy.orm import Session

from models.club import Club
from schemas import ClubCreate, ClubUpdate


def create_club(db: Session, club: ClubCreate) -> Club:
    print(club)
    db_club = Club(**club.model_dump())
    db.add(db_club)
    db.commit()
    db.refresh(db_club)
    return db_club

def read_club(db: Session, club_id: int) -> Optional[Club]:
    return db.query(Club).filter(Club.id == club_id).first()

def update_club(db: Session, club_id: int, club: ClubUpdate) -> bool:
    existing_club = read_club(db, club_id)
    if not existing_club: return False
    for key, value in club.model_dump().items():
        if value:
            setattr(existing_club, key, value)
    db.commit()
    db.refresh(existing_club)
    return True

def delete_club(db: Session, club_id: int) -> bool:
    existing_club = read_club(db, club_id)
    if not existing_club: return False
    db.delete(existing_club)
    db.commit()
    return True