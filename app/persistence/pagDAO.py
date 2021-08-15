from sqlalchemy.orm import Session
from .models import Pag


def get_pag(db: Session, pag_id: int):
    return db.query(Pag).filter(Pag.id == pag_id).first()


def get_first_pag(db: Session):
    return db.query(Pag).first()


def create_pag(db: Session, pagination: Pag):
    db.add(pagination)
    db.commit()
    db.refresh(pagination)
    return pagination


def update_pag(db: Session, pagination: Pag):
    db_pag = db.query(Pag).filter(Pag.id == pagination.id).first()
    db_pag.seed = pagination.seed
    db_pag.actual_page = pagination.actual_page
    db_pag.step = pagination.step
    db_pag.total_records = pagination.total_records
    db_pag.date = pagination.date
    db.commit()
    db.refresh(db_pag)
    return db_pag


def delete_pag(db: Session, pag_id: int):
    db_pag = get_pag(db, pag_id)
    if db_pag:
        db.delete(db_pag)
        db.commit()
