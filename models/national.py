from sqlalchemy.orm import mapped_column, Mapped

from db import Base

class National(Base):
    __tablename__ = "national_team"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()