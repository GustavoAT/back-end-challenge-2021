"""Get users from randomuser site.

    Documentation incomplete.
"""
import sys
import requests
from pydantic import parse_obj_as
from ..persistence.models import Pag
from ..persistence.pdmodels import UserCreate
from ..persistence.database import SessionLocal
from ..persistence.userDAO import upsert_user
from ..persistence.pagDAO import get_first_pag, create_pag
from datetime import datetime





RANDOMUSER_URL = 'https://randomuser.me/api/'
RANDOMUSER_NESTED_LEVELS = 2

def get_users(n_users: int = 10, seed: str = None, page: int = None):
    params = {'nat': 'BR,CA,ES,GB,NZ,US'}
    if seed:
        params['seed'] = seed
    if page:
        params['page'] = page
    if n_users > 1:
        params['results'] = n_users
    result = requests.get(RANDOMUSER_URL, params=params)
    return result


def save_random_users(n_users: int = 10):
    result = get_users(n_users)
    if result.status_code == 200:
        save_users(result)


def save_random_users_paginated():
    with SessionLocal() as db:
        pagination = get_first_pag(db)
        total = pagination.actual_page * pagination.step
        step = pagination.step
        if total >= pagination.total_records:
            page = 1
        else:
            page = pagination.actual_page + 1
            total = page * step
            difference = total - pagination.total_records
            if difference > 0:
                step -= difference
        result = get_users(step, pagination.seed, page)
        if result.status_code == 200:
            pagination.actual_page = page
            pagination.date = datetime.now()
            db.commit()
            save_users(result)


def save_users(request_result):
    users_list = request_result.json()['results']
    users_list = [
        flatten_many_levels(d, RANDOMUSER_NESTED_LEVELS) for d in users_list
    ]
    users_list = [add_imported_time(d) for d in users_list]
    users = parse_obj_as(list[UserCreate], users_list)
    with SessionLocal() as db:
        for user in users:
            upsert_user(db, user)


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


def init_pagination(step: int, total: int):
    pagination = Pag()
    pagination.actual_page = 0
    pagination.step = step
    pagination.total_records = total
    pagination.date = datetime.now()
    rec = get_users(1)
    pagination.seed = rec.json()['info']['seed']
    with SessionLocal() as db:
        create_pag(db, pagination)




if __name__ == '__main__':
    command = sys.argv[1]
    if command == 'initpag':
        if len(sys.argv) > 3:
            try:
                step = int(sys.argv[2])
                total = int(sys.argv[3])
                init_pagination(step, total)
                print('Usuarios importados')
            except TypeError:
                print('Valores de passo e total devem ser inteiros positivos')
        else:
            print('Argumentos ausentes para esse comando')
    if command == 'save':
        try:
            number_users = int(sys.argv[2])
            save_random_users(number_users)
            print(f'{number_users} usuarios inseridos ou atualizados no banco')
        except TypeError:
            print('Insira um valor inteiro positivo como argumento')
    if command == 'savenextpage':
        save_random_users_paginated()

    