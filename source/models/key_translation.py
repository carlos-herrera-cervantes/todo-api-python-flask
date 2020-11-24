from enum import Enum

class KeyTranslation(Enum):
    HEALT_MESSAGE = 'HealtMessage'
    USER_NOT_FOUND = 'UserNotFound'
    USER_NOT_VALID = 'UserNotValid'
    TODO_NOT_FOUND = 'TodoNotFound'
    TODO_NOT_VALID = 'TodoNotValid'
    WRONG_CREDENTIALS = 'WrongCredentials'
    INVALID_TOKEN = 'InvalidToken'
    MISSING_PAGINATE_PARAMS = 'MissingPaginateParams'
    INVALID_PAGINATION = 'InvalidPagination'
    INVALID_PERMISSIONS = 'InvalidPermissions'