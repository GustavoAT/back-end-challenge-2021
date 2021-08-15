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
    """Get users from randomuser API

    Args:
        n_users (int, optional): Number of results. Defaults to 10.
        seed (str, optional): Seed to find the same users again. Defaults to
        None.
        page (int, optional): Page of results. Defaults to None.

    Returns:
        Response
    """
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
    """Save new random users on the database

    Get a number of users from randomuser API and save them on the
    database.

    Args:
        n_users (int, optional): Number os users to get. Defaults to 10.
    """
    result = get_users(n_users)
    if result.status_code == 200:
        save_users(result)


def save_random_users_paginated():
    """Save random users on the database folowing a pagination rule

    The pagination rule should be previously saved on the database.
    The actual page is retrieved and next page is requested to
    randomuser API. Case all pages from pagination rule is done,
    next page would be 1.

    Returns:
        int: Page number saved
    """
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
            return page
        return None


def save_users(request_result):
    """Save users on the database

    Args:
        request_result (Response): response object from randomuser API
    """
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
    """Make second level from nested dictionary equal to the first level

    Flatten a dictionary by find inner dictionaries and unpack it.
    The inner keys are concated to outer key.

    Args:
        target (dict): dictionary to be flatten

    Returns:
        dict: one level flatten dict
    """
    flat_dict = {}
    for key in target:
        if type(target[key]) == dict:
            for key2, value in target[key].items():
                flat_dict[key + '_' + key2] = value
        else:
            flat_dict[key] = target[key]
    return flat_dict


def flatten_many_levels(target: dict, levels: int = 2):
    """Make nested levels on a dictionary equal to the first

    Args:
        target (dict): dictionary to be flatten
        levels (int, optional): nested levels on the dictionary. Defaults to 2.

    Returns:
        dict: n levels flatten dict
    """
    flat_dict = target
    for _ in range(levels):
        flat_dict = flatten_one_level(flat_dict)
    return flat_dict


def add_imported_time(target: dict):
    '''Add imported time to a dict'''
    target['imported_t'] = datetime.now()
    return target


def init_pagination(step: int, total: int):
    """Create a pagination rule on the database

    Args:
        step (int): Records per page
        total (int): Total records to request
    """
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
                print(
                    f'Paginação configurada para {total} ' +
                    f'usuarios de {step} em {step}'
                )
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
        r = save_random_users_paginated()
        if r:
            print(f'Página {r} salva')
        else:
            print(
                'Erro no salvamento, não foi possível ' +
                'obter usuários do randomuser'
            )
