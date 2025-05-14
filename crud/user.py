from typing import List

from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserUpdate
from core.security import hash_password

def create_user(db: Session, user: UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = User(username=user.username, hashed_password=hashed_pw, role=user.role)
    print(db_user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_all_users(db: Session):
    _q: List[User] = db.query(User).all()
    print(_q[0].username, _q[0].hashed_password, _q[0].role)
    return _q

def update_user(db: Session, user: UserUpdate):
    ...

def delete_user(db: Session, username: str):
    db_user = get_user(db, username)
    if not db_user: return False
    db.delete(db_user)
    db.commit()
    return True