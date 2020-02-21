from os import path, environ, urandom


class DefaultConfig(object):
    DEBUG = True
    MODULES = [
        'auth'
    ]
    LOG_ACCESS = True
    LOG_TO_FILES = False
    LOG_PATH = environ.get('LOG_PATH', default='logs')
    LOG_LEVEL = environ.get('LOG_LEVEL', default='DEBUG')

    JWT_HEADER_TYPE = 'JWT'
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY', default=urandom(64))

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get(
        'DATABASE_URL',
        default='')
    environ["NLS_LANG"] = "Russian.AL32UTF8"


DefaultLogging = {
    'handlers': {
        'ldap': {
            'class': 'logging.StreamHandler',
            'formatter': 'app_format'
        }
    },
    'loggers': {
        'ldap3': {
            'handlers': ['ldap']
        }
    }
}
