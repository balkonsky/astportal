from os import path, environ, urandom


class DefaultConfig(object):
    DEBUG = True
    MODULES = [
        'auth',
        'dashboard'
    ]
    LOG_ACCESS = True
    LOG_TO_FILES = False
    LOG_PATH = environ.get('LOG_PATH', default='logs')
    LOG_LEVEL = environ.get('LOG_LEVEL', default='DEBUG')

    JWT_HEADER_TYPE = 'JWT'
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY', default=urandom(64))

    SECRET_KEY = environ.get('SECRET_KEY', urandom(64))

    SECURITY_PASSWORD_SALT = environ.get('SECURITY_PASSWORD_SALT', 'n$|epitBlxw1u4@sB{45a2DlYn')
    SECURITY_PASSWORD_HASH = environ.get('SECURITY_PASSWORD_HASH', 'sha512_crypt')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = environ.get(
        'DATABASE_URL',
        default='mysql+pymysql://astportal:astportal@localhost/astportal')


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
