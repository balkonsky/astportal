"""
Логирование
===========

Access-лог и Correlation ID для Flask, контекстные лог-фильтры

Используется стандартная библиотека Python - logging_

.. _logging: https://docs.python.org/3/library/logging.html

"""

import time
import uuid
import logging

from flask import current_app, request, _request_ctx_stack
from flask_jwt_extended import current_user

from .cid import current_cid


class Flog(object):
    """
    Flog - кастомный логгер для Flask

    Добавляет в приложение access-лог (``flask.access``)
    и correlation id (``request._cid``)
    """

    def __init__(self, app=None, **kwargs):
        if app is not None:
            self.init_app(app)

    def init_app(self, app, **kwargs):
        self.audit = logging.getLogger('flask.audit')
        self.job = logging.getLogger('flask.job')

        app.config.setdefault(
            'REQUEST_ID_HEADERS',
            ['X-Request-ID', 'X-Correlation-ID'])

        logger = logging.getLogger('flask.access')

        @app.before_request
        def start_request():
            _request_ctx_stack.top._start_time = time.time()
            _request_ctx_stack.top._cid = None

            for header in current_app.config['REQUEST_ID_HEADERS']:
                value = request.headers.get(header)
                if value:
                    _request_ctx_stack.top._cid = value
                    break

            if not _request_ctx_stack.top._cid:
                _request_ctx_stack.top._cid = str(uuid.uuid4())

        @app.after_request
        def stop_request(response):
            query_string = request.environ['QUERY_STRING']
            if len(query_string) > 0:
                query_string = f'?{query_string}'

            client_ip = request.headers.get('NS-Client-IP')
            if not client_ip:
                client_ip = request.environ['REMOTE_ADDR']

            properties = {
                'method': request.method,
                'path': request.path + query_string,
                'proto': request.environ['SERVER_PROTOCOL'],
                'ua': request.environ['HTTP_USER_AGENT'],
                'ip': client_ip,
                'status': response.status_code,
                'size': response.headers.get('Content-Length', 0),
                'elapsed': time.time() - _request_ctx_stack.top._start_time,
            }

            logger.info('', extra=properties)
            return response


class AuthContext(logging.Filter):
    def filter(self, record):
        """
        .. warning:: Не используйте в логах ``sqlalchemy``!

        Добавляет текущего пользователя в формат лога - ``user``

        * record.user - имя пользователя
        """
        record.user = str(current_user or 'anonymous')
        return True


class RequestContext(logging.Filter):
    def filter(self, record):
        """
        Добавляет идентификатор текущего запроса в формат лога - ``cid``

        * record.cid - correlation id
        """
        record.cid = str(current_cid or 'app')
        return True


class JobContext(logging.Filter):
    def filter(self, record):
        """
        .. attention:: Использовать совместно с :class:`utils.job.ContextJob`

        Добавляет в формат лога свойства джобы *cid* и *user*

        * record.cid - correlation id
        * record.user - владелец джобы
        """
        try:
            from rq import get_current_job
        except ImportError:
            record.cid = None
            record.user = None
        else:
            job = get_current_job()
            record.cid = getattr(job, 'cid', None)
            record.user = getattr(job, 'owner', None)

        return True
