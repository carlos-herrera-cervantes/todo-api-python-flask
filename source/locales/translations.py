from settings import *
from models.key_translation import KeyTranslation

messages = [
    {
        'key': KeyTranslation.HEALT_MESSAGE.value,
        'localized_strings': {
            'en': 'Server up',
            'es': 'Servidor ejecutándose'
        }
    },
    {
        'key': KeyTranslation.USER_NOT_FOUND.value,
        'localized_strings': {
            'en': 'User not found',
            'es': 'Usuario no encontrado'
        }
    },
    {
        'key': KeyTranslation.USER_NOT_VALID.value,
        'localized_strings': {
            'en': 'User not valid',
            'es': 'El usuario no es válido'
        }
    },
    {
        'key': KeyTranslation.TODO_NOT_FOUND.value,
        'localized_strings': {
            'en': 'ToDo not found',
            'es': 'Tarea no encontrada'
        }
    },
    {
        'key': KeyTranslation.TODO_NOT_VALID.value,
        'localized_strings': {
            'en': 'ToDo not valid',
            'es': 'La tarea no es válida'
        }
    },
    {
        'key': KeyTranslation.WRONG_CREDENTIALS.value,
        'localized_strings': {
            'en': 'Wrong credentials',
            'es': 'Las credenciales son incorrectas'
        }
    },
    {
        'key': KeyTranslation.INVALID_TOKEN.value,
        'localized_strings': {
            'en': 'Invalid json web token',
            'es': 'El token no es válido'
        }
    },
    {
        'key': KeyTranslation.MISSING_PAGINATE_PARAMS.value,
        'localized_strings': {
            'en': 'page or page_size parameter is missing',
            'es': 'Falta el parámetro page o page_size'
        }
    },
    {
        'key': KeyTranslation.INVALID_PAGINATION.value,
        'localized_strings': {
            'en': 'The value of page must be greater than 0 / The value of page_size must be greater than 0 and less than 100',
            'es': 'El valor de page debe ser mayor a 0 / El valor de page_size debe ser mayor a 0 y menor a 100'
        }
    },
    {
        'key': KeyTranslation.INVALID_PERMISSIONS.value,
        'localized_strings': {
            'en': 'You do not have sufficient permissions to do this operation',
            'es': 'No tienes suficientes permisos para realizar esta acción'
        }
    }
]

def get_text(headers, key):
    """
    Return the text by language
    Parameters
    ----------
    headers: dict
        Headers of request
    key: str
        The identifier to get the text
    """
    language = headers.get('Accept-Language', 'en')
    text = list(filter(lambda obj: obj['key'] == key, messages)).pop()
    return text['localized_strings'][language]