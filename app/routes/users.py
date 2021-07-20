from fastapi import APIRouter


router = APIRouter()

@router.get('/users')
async def get_users():
    return {'message': 'here the list of users'}


@router.post('/users')
async def create_user():
    return {'message': 'user created'}


@router.get('/users/{id}')
async def get_user(id: int):
    return {'username': 'user', 'id': id}


@router.put('/users/{id}')
async def update_user(id: int):
    return {'message': 'user edited', 'id': id}


@router.post('/users/{id}/delete')
async def delete_user(id: int):
    return {'message': 'user deleted', 'id': id}