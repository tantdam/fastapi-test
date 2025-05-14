from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from api.auth import get_current_user, require_admin
from models.club import Club
from models.user import User
from schemas import ClubRead, ClubCreate, ClubUpdate
from db import get_db
from crud.club import read_club, create_club

router = APIRouter(prefix="/club", tags=["club"])

@router.get('/{club_id}', response_model=ClubRead)
def _read_club(club_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> Club:
    db_club = read_club(db, club_id)
    if not db_club:
        raise HTTPException(status_code=404, detail="Club not found")
    return db_club

@router.post('/', response_model=ClubRead)
def _create_club(club: ClubCreate, db: Session = Depends(get_db), user: User = Depends(require_admin)) -> ClubRead:
    return create_club(db, club)

@router.put('/{club_id}', response_model=ClubRead)
def _update_club(club_id: int, club: ClubUpdate, db: Session = Depends(get_db), user: User = Depends(require_admin)) -> Club:
    db_club = read_club(db, club_id)
    if not db_club:
        raise HTTPException(status_code=404, detail="Club not found")
    for key, value in club.model_dump().items():
        setattr(db_club, key, value)
    return db_club

@router.delete('/{club_id}')
def _delete_club(club_id: int, db: Session = Depends(get_db), user: User = Depends(require_admin)) -> bool:
    db_club = read_club(db, club_id)
    if not db_club:
        raise HTTPException(status_code=404, detail="Club not found")
    db.delete(db_club)
    db.commit()
    return True