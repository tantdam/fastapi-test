from sqlalchemy import Column, String, Integer, Enum
import enum
from sqlalchemy.orm import Mapped

from db import Base

class RoleEnum(enum.Enum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = Column(String, unique=True)
    role: Mapped[RoleEnum] = Column(Enum(RoleEnum), default=RoleEnum.user)
    hashed_password: Mapped[str] = Column(String)