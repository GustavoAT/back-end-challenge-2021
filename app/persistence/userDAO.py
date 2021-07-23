"""Data Access Object for User.

    CRUD operations on database.
    """
from sqlalchemy.orm import Session
from . import models, pdmodels
from .security.hash import create_salt, get_hashed_password




def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: pdmodels.UserCreate):
    salt = create_salt()
    user.login_password = get_hashed_password(user.login_password, salt)
    db_user = models.User(**user.dict(), login_salt=salt)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user():
    pass


def delete_user():
    pass