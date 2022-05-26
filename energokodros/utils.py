import os
from distutils.util import strtobool

from dotenv import load_dotenv

if not load_dotenv('../.env', override=True):
    raise EnvironmentError('Failed to find or load .env file')


def __get_from_env(key: str) -> str:
    if value := os.getenv(key, default=None):
        return value
    raise EnvironmentError(f'{key} was not found in environment')


def __get_bool_from_env(key: str) -> bool:
    try:
        return strtobool(__get_from_env(key))
    except ValueError:
        raise EnvironmentError(f'{key} boolean value has incorrect format')
