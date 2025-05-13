from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import crud.user
from db import get_db
from schemas.user import UserCreate, UserRead, Token
from crud import user as crud_user
from models.user import User
from core.security import create_access_token, verify_password

from starlette import status
from jose import jwt, JWTError
from constants import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud_user.get_user(db, username)
    if user is None:
        raise credentials_exception

    return user

def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


@router.get("/", response_model=UserRead)
def read_root(db: Session = Depends(get_db)):
    users = crud.user.get_all_users(db)
    return users

@router.post("/register", response_model=UserRead)
def register(new_user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, new_user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return crud_user.create_user(db, new_user)

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, form_data.username)
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}
