"""
Джобы
=====

Кастомный функционал над библиотекой rq_

.. _rq: https://python-rq.org/

"""

from rq.job import Job
from flask_jwt_extended import current_user

from .cid import current_cid


class ContextJob(Job):
    """
    Контекстная джоба - в атрибуты добавляет владельца и идентификатор запроса,
    в рамках которого она была создана
    """

    @classmethod
    def create(cls, *args, meta=None, **kwargs):
        """
        Перегруженный метод

        Добавляет из контекста ключи ``cid`` и ``owner`` в метаинформацию джобы
        при её создании
        """
        metadata = dict(
            cid=str(current_cid or '-'),
            owner=str(current_user or 'application'))
        job = super().create(*args, **kwargs, meta=metadata)
        return job

    @classmethod
    def fetch(cls, *args, **kwargs):
        """
        Перегруженный метод

        Получает из метаинформации джобы значения ключей ``cid`` и ``owner``
        и устанавливает их в качестве атрибутов джобы
        """
        job = super().fetch(*args, **kwargs)
        job.cid = job.meta['cid'] if 'cid' in job.meta else '-'
        job.owner = job.meta['owner'] if 'owner' in job.meta else 'application'
        return job
