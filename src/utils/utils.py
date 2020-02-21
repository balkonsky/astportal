"""
Утилиты
=======

"""

from importlib import import_module

from flask import current_app, jsonify, request
from werkzeug.exceptions import HTTPException

__all__ = [
    'register_blueprint', 'set_oracle_client_info',
    'jsonify_error', 'jsonify_jwt_error', 'bool_query_param', 'create_table_if_not_exist']


def register_blueprint(app, blueprint, package=None, path='modules'):
    """
    Регистрация модулей (:class:`flask.Blueprint`) в приложении

    .. note:: Возможно потребуется выполнять в `контексте приложения`_,
        в зависимости от организации конкретного модуля

    .. _`контекст приложения`: http://flask.pocoo.org/docs/1.0/appcontext/

    :param app: экземпляр приложения
    :type app: :class:`flask.Flask`
    :param str blueprint: имя загружаемого модуля
    :param str package: имя пакета с модулями (по-умолчанию ``app.name``),
        более детально см. `import_module`_
    :param str path: директория с модулями внутри пакета

    .. _`import_module`:
        https://docs.python.org/3/library/importlib.html#importlib.import_module
    """
    try:
        module = import_module(
            f'.{path}.{blueprint}.controllers', package or app.name)
        app.register_blueprint(module.blueprint)
        app.logger.info(f'Module [{blueprint}] loaded')
    except ImportError as e:
        app.logger.warning(f'Skip module [{blueprint}]: {e}')
    except Exception as e:
        app.logger.error(f'Skip module [{blueprint}]: {e}', exc_info=1)


def create_table_if_not_exist(db, app, ):
    with app.app_context():
        table_name = 'JWT_USERS_PY'.lower()
        sequence_name = f'{table_name}_id_seq'
        if not db.engine.dialect.has_table(db.engine, table_name, 'gen_cfg_test_mt_85'):
            current_app.logger.debug(f'create table with name : {table_name}')
            metadata = db.MetaData(db.engine)
            db.Table(table_name, metadata,
                     db.Column(
                         'id', db.Integer, primary_key=True),
                     db.Column(
                         'username', db.String(30), index=True, unique=True, nullable=False)
                     )
            db.engine.execute(f'create sequence {sequence_name} start with 1 increment by 1 nocache nocycle')
            metadata.create_all()
        table_name = 'SYSTEM_MESSAGES_FILIALS_PY'.lower()
        sequence_name = f'{table_name}_id_seq'
        if not db.engine.dialect.has_table(db.engine, table_name, 'gen_cfg_test_mt_85'):
            current_app.logger.debug(f'create table with name : {table_name}')
            metadata = db.MetaData(db.engine)
            db.Table(table_name, metadata,
                     db.Column(
                         'alarm_id', db.Integer, primary_key=True, nullable=False),
                     db.Column(
                         'guid', db.String(128), index=True),
                     db.Column(
                         'filial_id', db.Integer
                     ),
                     db.Column('filial_name', db.String(128))
                     )
            db.engine.execute(f'create sequence {sequence_name} start with 1 increment by 1 nocache nocycle')
            metadata.create_all()
        table_name = 'SYSTEM_MESSAGES_REGIONS_PY'.lower()
        sequence_name = f'{table_name}_id_seq'
        if not db.engine.dialect.has_table(db.engine, table_name, 'gen_cfg_test_mt_85'):
            current_app.logger.debug(f'create table with name : {table_name}')
            metadata = db.MetaData(db.engine)
            db.Table(table_name, metadata,
                     db.Column('alarm_id', db.Integer, primary_key=True, nullable=False),
                     db.Column('region', db.String(128)),
                     db.Column('guid', db.String(128), index=True))
            db.engine.execute(f'create sequence {sequence_name} start with 1 increment by 1 nocache nocycle')
            metadata.create_all()
        table_name = 'SYSTEM_MESSAGES_SEGMENTS_PY'.lower()
        sequence_name = f'{table_name}_id_seq'
        if not db.engine.dialect.has_table(db.engine, table_name, 'gen_cfg_test_mt_85'):
            current_app.logger.debug(f'create table with name : {table_name}')
            metadata = db.MetaData(db.engine)
            db.Table(table_name, metadata,
                     db.Column('alarm_id', db.Integer, primary_key=True, nullable=False),
                     db.Column('segment', db.String(20)),
                     db.Column('guid', db.String(128), index=True))
            db.engine.execute(f'create sequence {sequence_name} start with 1 increment by 1 nocache nocycle')
            metadata.create_all()
        table_name = 'SYSTEM_MESSAGES_PY'.lower()
        sequence_name = f'{table_name}_id_seq'
        if not db.engine.dialect.has_table(db.engine, table_name, 'gen_cfg_test_mt_85'):
            current_app.logger.debug(f'create table with name : {table_name}')
            metadata = db.MetaData(db.engine)
            db.Table(table_name, metadata,
                     db.Column('alarm_id', db.Integer, primary_key=True, nullable=False),
                     db.Column('text', db.String(2000)),
                     db.Column('type', db.String(30)),
                     db.Column('scheduled_start_time', db.Date()),
                     db.Column('scheduled_stop_time', db.Date()),
                     db.Column('send_mode', db.Integer),
                     db.Column('send_threshold', db.Integer),
                     db.Column('send_timeout', db.Integer),
                     db.Column('service_type_attr1', db.String(30)),
                     db.Column('wait_response_timeout', db.Integer),
                     db.Column('region', db.String(30)))
            db.engine.execute(f'create sequence {sequence_name} start with 1 increment by 1 nocache nocycle')
            metadata.create_all()


def set_oracle_client_info(db, info):
    """
    Установка идентификатора клиента для сессии Oracle

    .. attention:: Работает только в `контексте приложения`_

    .. _`контексте приложения`: http://flask.pocoo.org/docs/1.0/appcontext/

    :param db: экземпляр SQLAlchemy
    :type db: :class:`flask_sqlalchemy.SQLAlchemy`
    :param str info: идентификатор (любой текст)
    """
    try:
        query = 'begin dbms_application_info.set_client_info(:info); end;'
        db.engine.execute(query, {'info': info})
        current_app.logger.info(f'Oralce client info successfully set')

    except Exception as e:
        current_app.logger.warning(f'Oralce client info set error: {e}')


def jsonify_error(error):
    """
    JSONификация ошибок/статусов HTTP

    :param error: исключение, при использовании с
        :meth:`Flask.register_error_handler` передаётся **автоматически**
    :type error: :class:`Exception` или наследники
    :return: ответ в формате JSON с ключами *status*, *message* и *error*
    :rtype: :class:`flask.wrappers.Response`
    """

    if not isinstance(error, HTTPException):
        current_app.logger.critical(error, exc_info=1)
        return jsonify(status=500, error='Internal', message='None'), 500

    body = {
        'status': error.code,
        'message': error.description,
        'error': error.name
    }

    if error.code == 405:
        body['allowed'] = error.valid_methods

    return jsonify(body), error.code


def jsonify_jwt_error(jwt):
    """
    Приведение ошибок авторизации JWT к общему виду :func:`jsonify_error`

    :param jwt: экземпляр JWTManager
    :type jwt: :class:`flask_jwt_extended.JWTManager`
    """

    def unauth(msg):
        return jsonify(status=401, error='Unauthorized', message=msg), 401

    jwt.invalid_token_loader(lambda msg: unauth(f'Invalid token: {msg}'))
    jwt.revoked_token_loader(lambda: unauth('Token has been revoked'))
    jwt.expired_token_loader(lambda: unauth('Token has expired'))
    jwt.unauthorized_loader(lambda msg: unauth(msg))
    jwt.user_loader_error_loader(lambda msg: unauth('Unknown user'))


def bool_query_param(key):
    """Приведение значения ключа из query string к булеву типу"""
    value = request.args.get(key, None)
    if value in ['False', 'false', '0', 0]:
        return False
    elif value:
        return True
