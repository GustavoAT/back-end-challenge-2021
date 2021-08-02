"""Data Access Object for User.

    CRUD operations on database.
    """
from sqlalchemy.orm import Session
from sqlalchemy import update
from . import models, pdmodels
from .security.hash import create_salt, get_hashed_password




def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.User).slice(skip, limit).all()


def create_user(db: Session, user: pdmodels.UserCreate):
    if user.login_salt == None or user.login_salt == '':
        user.login_salt = create_salt()
    user.login_password = get_hashed_password(user.login_password, user.login_salt)
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: pdmodels.UserBase):
    update_statement = update(models.User).where(models.User.id == user_id).\
        values(**user.dict()).execution_options(synchronize_session='fetch')
    result = db.execute(update_statement)
    return result


def upsert_user(db: Session, user: pdmodels.UserCreate):
    if user.login_salt == None or user.login_salt == '':
        user.login_salt = create_salt()
    user.login_password = get_hashed_password(user.login_password, user.login_salt)
    query_user = db.query(models.User).filter(
        models.User.email==user.email,
        models.User.login_username==user.login_username,
        models.User.login_uuid==user.login_uuid
    )
    db_user = query_user.first()
    if db_user:
        query_user.update(**user.dict())
    else:
        db_user = models.User(**user.dict())
        db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    db.delete(db_user)
    db.commit()