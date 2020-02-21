"""
Декораторы
==========

.. attention:: Работают только в `контексте запроса`_

.. _`контексте запроса`: http://flask.pocoo.org/docs/1.0/reqcontext/

"""

from functools import wraps

from flask import current_app, request, abort, g
from cerberus import Validator


__all__ = ['json_required', 'validation_required']


def json_required(func):
    """
    Проверка тела запроса пишущих HTTP-методов на JSON

    Проверяет тело для методов **POST**, **PUT**, **PATCH**, **DELETE**
    """

    @wraps(func)
    def decorator(*args, **kwargs):
        methods = ['POST', 'PUT', 'PATCH', 'DELETE']

        if request.method in methods:
            if not request.is_json:
                return abort(400, 'Invalid request')

            body = request.get_json()

            if isinstance(body, dict) and ('password' in body):
                body = body.copy()  # sic!
                body['password'] = '***'

            current_app.logger.debug(f'Request {request.path}: {body}')

        return func(*args, **kwargs)

    return decorator


def validation_required(schema):
    """
    Валидация тела запроса по *schema*

    Правила написания *schema* - см. Cerberus_

    .. note:: Тело должно быть валидным JSON, предварительно
        следует использовать :func:`json_required`

    :param dict schema: валидная схема данных, см. `Validation Schema`_
    :raises BadRequest (400): если тело запроса не прошло валидацию

    .. _Cerberus: http://docs.python-cerberus.org
    .. _`Validation Schema`:
        http://docs.python-cerberus.org/en/stable/schemas.html
    """
    def wrapper(func):

        @wraps(func)
        def decorator(*args, **kwargs):

            body = request.get_json()

            if not isinstance(body, dict):
                return abort(400, 'Request body must be an object')

            validator = Validator(schema)
            normalized = validator.normalized(body)

            if not validator.validate(normalized):
                return abort(400, validator.errors)

            g.body = normalized  # !

            return func(*args, **kwargs)

        return decorator

    return wrapper
