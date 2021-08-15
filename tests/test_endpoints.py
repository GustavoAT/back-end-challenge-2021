from typing import List
from fastapi.testclient import TestClient
from app.main import app




client = TestClient(app)

def test_main():
    '''Test root of API'''
    response = client.get('/')
    assert response.status_code == 200
    assert response.json()['message'] == 'REST Back-end Challenge 20201209 Running'
    

def test_get_users():
    '''Test the /users endpoint'''
    response = client.get('/users/')
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_user():
    '''Test the /users/:user_id endpoint'''
    response = client.get('/users/')
    response_list = response.json()
    if len(response_list) > 0:
        user_id = response_list[0]['id']
        response = client.get(f'/users/{user_id}')
        assert response.status_code == 200


def test_create_update_delete_user():
    '''Test creation, updating and deletion of an user'''
    user_data = {
        "gender": "male",
        "name_first": "J",
        "name_last": "D",
        "email": "jon.doe@example.com",
        "login_uuid": "20c83553-1551-4e76-2234-4181ea561139",
        "login_username": "goodusername",
        "login_password": "mypassisnotsafe",
        "dob_date": "2000-04-01T15:52:08",
        "imported_t": "2021-08-06T21:20:00"
    }
    response = client.post('/users/', json=user_data)
    assert response.status_code == 200
    user_id = response.json()['id']
    user_data['name_last'] = 'Doe'
    response = client.put(f'/users/{user_id}', json=user_data)
    assert response.status_code == 200
    assert response.json()['name_last'] == 'Doe'
    response = client.delete(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json()['message'] == f'Usuário de id {user_id} excluído'