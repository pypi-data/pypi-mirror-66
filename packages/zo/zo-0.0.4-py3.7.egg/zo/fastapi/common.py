import time
from fastapi import Query
from .model import PageArgs
from .error import abort_if
from ..aa import timestamp_int, g_random_str, get_env
from ..db import conn


async def common_page_args(
        q: str = None,
        page: int = Query(1, ge=1, le=1000),
        page_size: int = Query(10, description='range: 1~100', ge=1, le=100)):
    return PageArgs(**{'q': q, 'page': page, 'page_size': page_size})


async def check_reset_key(key: int = 0):
    abort_if(abs(time.time() - key) > 60, f'reset_key_error: valid key = {timestamp_int() + 60}')


async def check_token(key: int = 0):
    abort_if(abs(time.time() - key) > 60, f'reset_key_error: valid key = {timestamp_int() + 60}')


async def get_new_id(key, name='id', decimals=8):
    db = conn()
    return str(db.zincr(name, key, decimals=decimals))


async def generate_user_token(username, prefix='z'):
    db = conn()
    env = get_env()
    token = g_random_str(f'{prefix}_{username}', 128)
    for key in db.keys(f'{prefix}_{username}_'):  # del old token
        db.delete(key)
    db.setx(token, username, env.token_user_expire)
    return token
