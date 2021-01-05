from click import group
from flask import current_app
from flask.cli import FlaskGroup

from .utils.job import ContextJob

from . import create_app, db


@group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass


@cli.command()
def periodic():
    """Start rq scheduler"""
    from rq_scheduler import Scheduler
    Scheduler(
        interval=60,
        job_class=ContextJob,
        connection=current_app.redis).run(burst=False)
