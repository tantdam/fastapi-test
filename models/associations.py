# app/models/associations.py

from sqlalchemy import Table, Column, ForeignKey
from db import Base

player_former_clubs = Table(
    "player_former_clubs",
    Base.metadata,
    Column("player_id", ForeignKey("player.id"), primary_key=True),
    Column("club_id", ForeignKey("club.id"), primary_key=True)
)
