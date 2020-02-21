from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from ldap3.utils.log import set_library_log_detail_level, PROTOCOL

from .utils import (
    Flog, register_blueprint, jsonify_error,
    jsonify_jwt_error, set_oracle_client_info)

from .config import DefaultConfig, DefaultLogging

__all__ = ['create_app']

__version__ = '0.1.0'
__authors__ = ['Maksim Avramenko']

db = SQLAlchemy()
jwt = JWTManager()
log = Flog()


def create_app(config=DefaultConfig):
    """
    Create application

    :param config: объект или имя файла с конфигурацией
    :type config: object or str
    """

    app = Flask(__name__)
    app.config.from_object(config)

    log.init_app(app, log_config=DefaultLogging, jobbed=True)
    app.logger.info(f'astportal v {__version__}')

    app.register_error_handler(Exception, jsonify_error)

    set_library_log_detail_level(PROTOCOL)  # ldap3 loglevel

    db.init_app(app)
    CORS(app, resources=r'/*')

    jwt.init_app(app)
    jsonify_jwt_error(jwt)

    for blueprint in app.config['MODULES']:
        with app.app_context():
            register_blueprint(app, blueprint, package='src')

    dialect = app.config['SQLALCHEMY_DATABASE_URI']
    if not app.debug and dialect.startswith('oracle'):
        with app.app_context():
            set_oracle_client_info(db, 'Kitchen')

    return app
