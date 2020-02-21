"""
Идентификатор запроса
=====================

"""

from werkzeug.local import LocalProxy
from flask import has_request_context, _request_ctx_stack


def get_correlation_id():
    if has_request_context() and hasattr(_request_ctx_stack.top, '_cid'):
        return _request_ctx_stack.top._cid
    return None


current_cid = LocalProxy(get_correlation_id)
"""Прокси к идентификатору текущего запроса (``request._cid``)"""
