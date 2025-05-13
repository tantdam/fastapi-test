from __future__ import annotations
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base
from models.associations import player_former_clubs
from models.club import Club

class Player(Base):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    middle_name: Mapped[str] = mapped_column(nullable=True)

    age: Mapped[int] = mapped_column()
    current_club: Mapped[int] = mapped_column(ForeignKey('club.id'))
    national_team: Mapped[int] = mapped_column(ForeignKey('national_team.id'))
    position: Mapped[str] = mapped_column()

    previous_clubs: Mapped[List["Club"]] = relationship(
        "Club",
        secondary=player_former_clubs,
        back_populates="previous_players",
        lazy="joined"
    )
