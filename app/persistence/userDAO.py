"""Data Access Object for User.

    CRUD operations on database.
    """
from sqlalchemy.orm import Session
from sqlalchemy import update
from . import models, pdmodels
from .security.hash import create_salt, get_hashed_password




def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_unique_data(db: Session, user: pdmodels.UserCreate):
    query_user = db.query(models.User).filter(
        models.User.email==user.email,
        models.User.login_username==user.login_username,
        models.User.login_uuid==user.login_uuid
    )
    db_user = query_user.first()
    return db_user


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
    db.execute(update_statement)
    db.commit()
    return get_user(db, user_id)


def upsert_user(db: Session, user: pdmodels.UserCreate):
    if user.login_salt == None or user.login_salt == '':
        user.login_salt = create_salt()
    user.login_password = get_hashed_password(user.login_password, user.login_salt)
    db_user = get_user_by_unique_data(db, user)
    if db_user:
        update_user(db, db_user.id, user)
    else:
        db_user = models.User(**user.dict())
        db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False