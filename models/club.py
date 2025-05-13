from __future__ import annotations
from typing import List

from sqlalchemy.orm import relationship, Mapped, mapped_column

from db import Base
from models.associations import player_former_clubs

class Club(Base):
    __tablename__ = "club"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    city: Mapped[str] = mapped_column()
    country: Mapped[str] = mapped_column()
    league: Mapped[str] = mapped_column()

    previous_players: Mapped[List["Player"]] = relationship(
        "Player",
        secondary=player_former_clubs,
        back_populates="previous_clubs",
        lazy="joined"
    )
