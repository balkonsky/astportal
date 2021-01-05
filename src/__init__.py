from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_security import SQLAlchemySessionUserDatastore, Security
from ldap3.utils.log import set_library_log_detail_level, PROTOCOL

from .utils import (
    Flog, register_blueprint, jsonify_error,
    jsonify_jwt_error)
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
    with app.app_context():
        from .models import User, Role
        db.create_all()
        db.session.commit()

    CORS(app, resources=r'/*')

    jwt.init_app(app)
    jsonify_jwt_error(jwt)

    migrate = Migrate(app, db)
    manager = Manager(migrate)
    manager.add_command('db', MigrateCommand)

    for blueprint in app.config['MODULES']:
        with app.app_context():
            register_blueprint(app, blueprint, package='src')

    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)
    # with app.app_context():
    #     user_datastore.create_user(id=1, email='mavramenko@humans.net', password='mavramenko')
    #     db.session.commit()

    return app
