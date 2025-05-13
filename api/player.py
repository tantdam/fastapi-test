from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from api.auth import get_current_user, require_admin
from models.player import Player
from schemas import PlayerRead, PlayerCreate, PlayerUpdate
from db import get_db

from crud.player import create_player, read_player, update_player, delete_player
from models.user import User

router = APIRouter(prefix="/player", tags=["Players"])

@router.post('/', response_model=PlayerRead)
async def _create_player(player: PlayerCreate, db: Session = Depends(get_db), user: User = Depends(require_admin)) -> Player:
    return create_player(db, player)

@router.get('/{player_id}', response_model=PlayerRead)
async def _read_player(player_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> Player:
    player = read_player(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.put('/{player_id}', response_model=PlayerRead)
async def _update_player(player_id: int, player: PlayerUpdate, db: Session = Depends(get_db), user: User = Depends(require_admin)) -> Player:
    updated = update_player(db, player_id, player)
    if not updated:
        raise HTTPException(status_code=404, detail="Update failed")
    return updated

@router.delete('/{player_id}')
async def _delete_player(player_id: int, db: Session = Depends(get_db), user: User = Depends(require_admin)) -> bool:
    deleted = delete_player(db, player_id)
    if not deleted: raise HTTPException(status_code=404, detail="Delete failed")
    return True