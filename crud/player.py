from typing import Optional

from sqlalchemy.orm import Session
from schemas import PlayerCreate, PlayerUpdate
from models.player import Player


def create_player(db: Session, player: PlayerCreate) -> Player:
    db_player = Player(**player.model_dump())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def read_player(db: Session, player_id: int) -> Optional[Player]:
    return db.query(Player).filter(Player.id == player_id).first()

def update_player(db: Session, player_id: int, player: PlayerUpdate) -> Optional[Player]:
    existing_player = read_player(db, player_id)
    if not existing_player:
        return None
    for key, value in player.model_dump().items():
        if value:  # Update only new values
            setattr(existing_player, key, value)
    db.commit()
    db.refresh(existing_player)
    return existing_player

def delete_player(db: Session, player_id: int) -> bool:
    existing_player = db.query(Player).filter(Player.id == player_id).first()
    if not existing_player:
        return False
    db.delete(existing_player)
    db.commit()
    return True