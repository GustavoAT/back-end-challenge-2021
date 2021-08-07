from typing import List
from fastapi import APIRouter
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from ..persistence.database import SessionLocal
from ..persistence import pdmodels, userDAO


router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/users/', response_model=List[pdmodels.User])
async def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = userDAO.get_users(db, skip, limit)
    return users


@router.post('/users/', response_model=pdmodels.User)
async def create_user(user: pdmodels.UserCreate, db: Session = Depends(get_db)):
    db_user = userDAO.get_user_by_unique_data(db, user)
    if db_user:
        raise HTTPException(status_code=400, detail='e-mail, login ou uuid já cadastrado')
    return userDAO.create_user(db, user)


@router.get('/users/{user_id}', response_model=pdmodels.User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = userDAO.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    return db_user


@router.put('/users/{user_id}')
async def update_user(user_id: int, user: pdmodels.UserBase, db: Session = Depends(get_db)):
    db_user = userDAO.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    return userDAO.update_user(db, user_id, user)


@router.delete('/users/{user_id}')
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = userDAO.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    return {'message': f'Usuário de id {user_id} excluído'}