"""Get users from randomuser site.

    Documentation incomplete.
"""
import sys
import requests
from pydantic import parse_obj_as
from ..persistence.pdmodels import UserCreate
from ..persistence.database import SessionLocal
from ..persistence.userDAO import create_user
from datetime import datetime





RANDOMUSER_URL = 'https://randomuser.me/api/'
RANDOMUSER_NESTED_LEVELS = 2

def get_users(n_users: int = 10):
    params = {'nat': 'BR'}
    if n_users > 1:
        params['results'] = n_users
    result = requests.get(RANDOMUSER_URL, params=params)
    return result


def save_random_users(n_users: int = 10):
    result = get_users(n_users)
    if result.status_code == 200:
        users_list = result.json()['results']
        users_list = [
            flatten_many_levels(d, RANDOMUSER_NESTED_LEVELS) for d in users_list
        ]
        users_list = [add_imported_time(d) for d in users_list]
        users = parse_obj_as(list[UserCreate], users_list)
        with SessionLocal() as db:
            for user in users:
                create_user(db, user)


def flatten_one_level(target: dict):
    flat_dict = {}
    for key in target:
        if type(target[key]) == dict:
            for key2, value in target[key].items():
                flat_dict[key + '_' + key2] = value
        else:
            flat_dict[key] = target[key]
    return flat_dict


def flatten_many_levels(target: dict, levels: int = 2):
    flat_dict = target
    for _ in range(levels):
        flat_dict = flatten_one_level(flat_dict)
    return flat_dict


def add_imported_time(target: dict):
    target['imported_t'] = datetime.now()
    return target




if __name__ == '__main__':
    try:
        number_users = int(sys.argv[1])
        save_random_users(number_users)
        print(f'{number_users} usuarios inseridos no banco')
    except TypeError:
        print('Insira um valor inteiro positivo como argumento')
    