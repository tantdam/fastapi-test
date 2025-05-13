from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from api.auth import get_current_user, require_admin
from crud.national import create_national, read_national
from db import get_db
from models.national import National
from models.user import User
from schemas import NationalRead, NationalCreate, NationalUpdate

router = APIRouter(prefix="/national", tags=["national"])

@router.post('/', response_model=NationalRead)
def _create_national(national: NationalCreate, db: Session = Depends(get_db), user: User = Depends(require_admin)) -> National:
    return create_national(db, national)

@router.get('/{national_id}', response_model=NationalRead)
def _read_national(national_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> National:
    print(national_id)
    db_national = read_national(db, national_id)
    if not db_national:
        raise HTTPException(status_code=404, detail="National not found")
    return db_national

@router.put('/{national_id}', response_model=NationalRead)
def _update_national(national_id: int, national: NationalUpdate, db: Session = Depends(get_db), user: User = Depends(require_admin)) -> National:
    db_national = read_national(db, national_id)
    if not db_national:
        raise HTTPException(status_code=404, detail="National not found")
    for key, value in national.model_dump().items():
        setattr(db_national, key, value)
    return db_national

@router.delete('/{national_id}')
def _delete_national(national_id: int, db: Session = Depends(get_db), user: User = Depends(require_admin)) -> bool:
    db_national = read_national(db, national_id)
    if not db_national:
        raise HTTPException(status_code=404, detail="National not found")
    db.delete(db_national)
    db.commit()
    return True